#!/usr/bin/env python3
import os
import sys
import fcntl
import struct
import socket
import json
import uuid
import select

# CONSTANTS
TUNSETIFF = 0x400454ca
IFF_TUN = 0x0001
IFF_NO_PI = 0x1000

# PATHS & CONFIG DIRECTORY
CONFIG_DIR = "cnulp"
IDENTITY_FILE = os.path.join(CONFIG_DIR, "my_personality.json")
WHITELIST_FILE = os.path.join(CONFIG_DIR, "whitelist.json")
SITES_FILE = os.path.join(CONFIG_DIR, "sites.json")

def EnsureConfigDir():
    # CREATING FOLDER CNULP IF THIS NOT FOUND
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        real_user = os.environ.get("SUDO_USER")
        if real_user:
            import shutil
            try:
                shutil.chown(CONFIG_DIR, user=real_user, group=real_user)
            except Exception as e:
                print(f"CHOWN DIR ERROR: {e}")

def GetOrCreateIdentity():
    EnsureConfigDir()
    if not os.path.exists(IDENTITY_FILE):
        print(f"{IDENTITY_FILE} not found. Creating...")
        print("VIRTUAL_IP = 10.0.0.1/24. (Default IP. Modify in cnulp/my_personality.json)")
        my_uuid = str(uuid.uuid4())
        default_cfg = {
            "my_uuid": my_uuid,
            "virtual_ip": "10.0.0.1/24"
        }
        with open(IDENTITY_FILE, "w", encoding="utf-8") as f:
            json.dump(default_cfg, f, indent=4)
            
        real_user = os.environ.get("SUDO_USER")
        if real_user:
            import shutil
            try:
                shutil.chown(IDENTITY_FILE, user=real_user, group=real_user)
            except Exception as e:
                print(f"CHOWN ERROR: {e}")
        try:
            os.chmod(IDENTITY_FILE, 0o666)
        except Exception as e:
            print(f"CHMOD ERROR: {e}")
            
        print(f'Created UUID: {my_uuid} with IP: 10.0.0.1/24 in {IDENTITY_FILE}')
        return my_uuid, "10.0.0.1/24"

    with open(IDENTITY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        my_uuid = data.get("my_uuid")
        virtual_ip = data.get("virtual_ip", "10.0.0.1/24")
        return my_uuid, virtual_ip

def LoadWhiteList():
    peoples = {}
    if os.path.exists(WHITELIST_FILE):
        with open(WHITELIST_FILE, "r", encoding="utf-8") as f:
            print(f"D-line: opening {WHITELIST_FILE} in READ mode.")
            data = json.load(f)
            for person in data.get("friends", []):
                short_id = uuid.UUID(person["uuid"]).int & 0xFFFFFFFF
                peoples[person["uuid"]] = {
                    "real_ip": person["ip"],
                    "short_id": short_id,
                    "name": person["name"]
                }
    return peoples

def load_sites():
    sites_map = {}
    if os.path.exists(SITES_FILE):
        with open(SITES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            sites_list = data.get("sites", data) if isinstance(data, dict) else data
            for s in sites_list:
                owner_uuid = s.get("owner_uuid")
                short_id = uuid.UUID(owner_uuid).int & 0xFFFFFFFF if owner_uuid else 0
                sites_map[s["site"]] = {
                    "name": s["name"],
                    "short_id": short_id,
                    "owner_uuid": owner_uuid
                }
    return sites_map

def OpenInterface(dev_name, ip_addr="10.0.0.1/24"):
    try:
        print(f"Initialization interface {dev_name}!")
        try:
            tun = open("/dev/net/tun", 'r+b', buffering=0)
        except PermissionError as pe:
            print(f"Crashed! PermissionError: {pe}")
            sys.exit(1)
            
        ifr = struct.pack('16sH', dev_name.encode('utf-8'), IFF_TUN | IFF_NO_PI)
        fcntl.ioctl(tun, TUNSETIFF, ifr)
        print(f"Interface {dev_name} created and opened.")
        
        try:
            import psutil
            stats = psutil.net_if_stats()
            if dev_name in stats and not stats[dev_name].isup:
                import subprocess
                subprocess.run(["sudo", "ip", "link", "set", dev_name, "up", "mtu", "1400"], check=True)
                print(f"Interface {dev_name} UPped with MTU 1400!")
        except ImportError:
            pass
            
        import subprocess
        subprocess.run(["sudo", "ip", "addr", "add", ip_addr, "dev", dev_name], check=True)
        print(f"OK! Net started with IP: {ip_addr}")
        return tun
    except Exception as e:
        print(f'Fatal error: {e}')
        sys.exit(1)

def start():
    my_uuid, virtual_ip = GetOrCreateIdentity()
    friends = LoadWhiteList()
    sites = load_sites()
    
    tun = OpenInterface('aengine0', ip_addr=virtual_ip)
    
    rx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rx_socket.bind(("0.0.0.0", 63048))
    rx_socket.setblocking(False)
    
    tx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tx_socket.setblocking(False)
    
    print(":: Warn: standard port CnUlP: 63048.")
    print("!! + RX socket bound to 0.0.0.0:63048")
    print("!! + TX socket ready.")
    print("[+] Dynamic routes auto-learning active.\n")
    
    inputs = [tun, rx_socket]
    dynamic_routes = {}
    
    try:
        while True:
            readable, _, _ = select.select(inputs, [], [])
            for s in readable:
                if s is tun:
                    try:
                        packet = tun.read(2048)
                    except OSError:
                        print("cnulp has error:")
                        break
                    if not packet or len(packet) < 20:
                        continue
                    if (packet[0] >> 4) != 4:
                        continue
                        
                    dst_ip = socket.inet_ntoa(packet[16:20])
                    if dst_ip.startswith(('224.', '239.', '255.255.255.255')):
                        continue
                        
                    real_desk_ip = None
                    owner_id = 0
                    
                    if dst_ip in dynamic_routes:
                        real_desk_ip = dynamic_routes[dst_ip]
                    elif dst_ip in sites:
                        site_data = sites[dst_ip]
                        owner_uuid = site_data["owner_uuid"]
                        if owner_uuid in friends:
                            real_desk_ip = friends[owner_uuid]["real_ip"]
                            owner_id = site_data["short_id"]
                        else:
                            print(f"[!!] Owner UUID {owner_uuid} NOT in whitelist!")
                            continue
                    else:
                        continue
                        
                    if real_desk_ip:
                        custom_header = struct.pack('<BI', 0x24, owner_id)
                        encapsulated_packet = custom_header + packet
                        tx_socket.sendto(encapsulated_packet, (real_desk_ip, 63048))
                        
                elif s is rx_socket:
                    try:
                        packet, addr = rx_socket.recvfrom(2048)
                    except OSError:
                        continue 
                    if len(packet) > 5 and packet[0] == 0x24:
                        ip_packet = packet[5:]
                        if len(ip_packet) < 20 or (ip_packet[0] >> 4) != 4:
                            print(f"[!] Dropped from {addr}: invalid IP")
                            continue  
                            
                        src_ip = socket.inet_ntoa(ip_packet[12:16])
                        real_ip = addr[0]
                        
                        if dynamic_routes.get(src_ip) != real_ip:
                            dynamic_routes[src_ip] = real_ip
                            print(f"[*] Route learned: Virtual {src_ip} <---> Real {real_ip}")
                            
                        try:
                            tun.write(ip_packet)
                        except OSError as e:
                            print(f"[!!] TUN write failed: {e}")
                            
    except KeyboardInterrupt:
        print("\n[-] Stopping network service...")
    finally:
        tun.close()
        rx_socket.close()
        tx_socket.close()
        print("[-] Closed.")

if __name__ == "__main__":
    import traceback
    try:
        start()
    except Exception as e:
        print("\n[!] CRASH DETECTED:")
        traceback.print_exc()
        sys.exit(1)

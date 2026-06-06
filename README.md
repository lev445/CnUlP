## CnUlP net - try it. now. 

## What is this?
- **You can use this net how engine, with the help of settings you can get what you want**
- **Portable net, where you setting YOUR net in configs.**

## How this working?
We have files:
- `whitelist.json`
- `sites.json`
- `my_personality.json`

So, what is this **files**?
Configs. Let's go through the first setup!

## What i am need?
You MUST to be download:
- Python3
- Ruby 
- This program support only unix-like (for example: linux) or unix-similar (for example: free-bsd)

## Whitelist.json
whitelist.json (JSON).
Format type:
Warning: type another user data.
Warning: another user MUST to be download this app.

```json
{
    "ip": "192.x.x.x",
    "uuid": "uuid-from-my_personality.json",
    "name": "yabloko"
}
```

**line** "ip": local IP.
**line** "uuid": UUID from my_personality.json
**line** "name": name.

After: start file: ruby main.rb
Type "start" and wait. After your sudo, ask your pass, type. After, press ^C to exit.
You have YOUR UUID. Check, open file: "nano my_personality.json"

- - -
On another computer, repeat the same action, but this time with your UUID, IP, etc.

## Sites.json 
In this file, you can setting your first site.
The owner can be anyone. Please, after setting this file, check. Are you sure you are the owner?
Format: 

```json
{
    "site": "10.0.0.1",
    "name": "grusha",
    "owner_uuid": "owner-uuid-here"
}
```

line "site": site IP. By standards CnUlP, using 10.0.0.x 
line "name": site name. 
line "owner_uuid": who owner of this site? (From my_personality.json.)

## This end of first configuration. Start, and try type in terminal:
ping 10.0.0.x 

## Documentation
For full documentation, open this folder: "doc".

## License 
GPL-3 License.


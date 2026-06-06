1105;9u## In this article, you'll learn about setup, how to configure the configuration for the first time, and all the configuration parameters. Let's get started.

## First setup.
You can **find** information about the initial installation in the `README.md` file. 

## All configuration parameters.

- `whitelist.json`
File in: your_folder/whitelist.json (root folder)

**template:**

```json
{
    "friends": [
        {
            "ip": "192.168.100.2",
            "uuid": "4a727ed3-b5c3-4973-a422-c5e62b728c4c",
            "name": "teto pear =d"
        }
    ]
}

```
parameter: "ip": IP of your peer, who want to connect with you. 
parameter: "uuid": your uuid from file my_personality.json.
parameter: "name": your name.

- `sites.json`
File in: your_folder/sites.json (root folder)

**template:**

```json
{
    "sites": [
        {
            "site": "10.0.0.5",
            "name": "RULE 34 OFFICIAL SITE",
            "owner_uuid": "cc4c4a62-fedd-42b9-971d-d73c3ac6eafe"
        }
    ]
}

```
parameter: "site": site ip.
parameter: "name": your site name.
parameter: "owner_uuid": who owner of site? (in uuid, from my_personality.json.)

- `my_personality.json`
File in: your_folder/my_personality.json (root folder)

**template**

```json
{
    "my_uuid": "42c56892-0ba7-47fe-8881-27a83e1cce72",
    "virtual_ip": "10.0.0.1/24"
}

```

parameter: "my_uuid": DO NOT change this parameter. This parameter generated with first start program. 
parameter: "virtual_ip": your ip in network CnUlP


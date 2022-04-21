# Dracoon-Automation-Scripts
Some scripts to automate daily work.


## Install
In `src` directory execute the following commands

```sh
python3 -m venv dasenv
source dasenv/bin/activate
pip3 install -r requirements.txt
```

## Requirements General

1. Create an App in Dracoon and select Grant Type "password". And copy Client ID (appID) and Client Secret (secret) into your config file (default: das.cfg)
2. Create a local user for automation

### Requirements create_home_folder.py

1. automation user needs group manager privilege
2. create a home folder and copy its node id to "homeRootRoomNode" in your config file
3. automation user needs room administrator privilege for home folder
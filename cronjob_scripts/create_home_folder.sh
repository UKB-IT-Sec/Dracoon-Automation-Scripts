#!/usr/bin/env bash

cd ~/git/Dracoon-Automation-Scripts/src || exit 1

source dasenv/bin/activate || exit 1

python3 create_home_folders.py -c ukb.cfg -s || exit 1

exit 0

#! /usr/bin/env python3
'''
    DAS - Dracoon Automation Scripts
    Copyright (C) 2022 Universitaetsklinikum Bonn AoeR

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import argparse
import logging
import configparser
import sys
import asyncio

from pathlib import Path
from helper.dracoon_auth import connect_to_cloud, disconnect
from helper.logging import setup_logging
from helper.groups import list_groups, list_users_of_group,\
    get_user_ids_of_group

PROGRAM_NAME = 'Create Home Folders'
PROGRAM_VERSION = '0.0.1'
PROGRAM_DESCRIPTION = 'create home folders'


def _setup_argparser():
    parser = argparse.ArgumentParser(description='{} - {}'.format(PROGRAM_NAME, PROGRAM_DESCRIPTION))
    parser.add_argument('-c', '--config_file', default='./das.cfg', help='load a config file')
    parser.add_argument('-L', '--log_level', help='define the log level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default=None)
    parser.add_argument('-V', '--version', action='version', version='{} {}'.format(PROGRAM_NAME, PROGRAM_VERSION))
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='print debug messages')
    return parser.parse_args()


def _load_config(config_file):
    config = configparser.ConfigParser()
    config_file = Path(config_file)
    if not config_file.exists():
        sys.exit('config file not found: {}'.format(config_file))
    config.read(config_file)
    if args.log_level is not None:
        config['Logging']['logLevel'] = args.log_level
    return config


async def _create_home_folders(conf):
    cloud = await connect_to_cloud(config)

    user_ids = await get_user_ids_of_group(cloud, config['userManagement']['userGroupId'])
    print(user_ids)
    
    await disconnect(cloud)

if __name__ == '__main__':
    args = _setup_argparser()
    config = _load_config(args.config_file)
    setup_logging(args, config)
    
    asyncio.run(_create_home_folders(config))

    sys.exit()

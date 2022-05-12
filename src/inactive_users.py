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
import sys
import asyncio

from datetime import datetime, timezone

from helper.dracoon_auth import connect_to_cloud, disconnect
from helper.logging import setup_logging
from helper.config import load_config

PROGRAM_NAME = 'Inactive Users'
PROGRAM_VERSION = '0.0.1'
PROGRAM_DESCRIPTION = 'list inactive users'


def _setup_argparser():
    parser = argparse.ArgumentParser(description='{} - {}'.format(PROGRAM_NAME, PROGRAM_DESCRIPTION))
    parser.add_argument('-c', '--config_file', default='./das.cfg', help='load a config file')
    parser.add_argument('-L', '--log_level', help='define the log level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default=None)
    parser.add_argument('-V', '--version', action='version', version='{} {}'.format(PROGRAM_NAME, PROGRAM_VERSION))
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='print debug messages')
    parser.add_argument('-D', '--day_threshold', help='inactivity of this many days [default: 365]', default='365')
    return parser.parse_args()

def is_inactive(last_login_date, day_threshold):
    try:
        if (datetime.now(timezone.utc) - last_login_date).days > day_threshold:
            return True
    except TypeError:
        return True
    return False


async def _list_inactive_users(config):
    cloud = await connect_to_cloud(config)
    
    all_users = await cloud.users.get_users()
    
    inactive_users = list()
    
    for user in all_users.items:
        if is_inactive(user.lastLoginSuccessAt, 365):
            inactive_users.append('{}: {}'.format(user.lastLoginSuccessAt, user.userName))
            
    await disconnect(cloud)
    
    inactive_users.sort()
    logging.info('{} inactive users found'.format(len(inactive_users)))
    for user in inactive_users:
        print(user)


if __name__ == '__main__':
    args = _setup_argparser()
    config = load_config(args.config_file, log_level_overwrite=args.log_level)
    setup_logging(args, config)

    asyncio.run(_list_inactive_users(config))

    sys.exit()

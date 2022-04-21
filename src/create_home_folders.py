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

from helper.dracoon_auth import connect_to_cloud, disconnect
from helper.logging import setup_logging
from helper.rooms import get_users_without_personal_rooms, create_personal_rooms
from helper.config import load_config

PROGRAM_NAME = 'Create Home Folders'
PROGRAM_VERSION = '0.0.2'
PROGRAM_DESCRIPTION = 'create home folders'


def _setup_argparser():
    parser = argparse.ArgumentParser(description='{} - {}'.format(PROGRAM_NAME, PROGRAM_DESCRIPTION))
    parser.add_argument('-c', '--config_file', default='./das.cfg', help='load a config file')
    parser.add_argument('-L', '--log_level', help='define the log level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default=None)
    parser.add_argument('-V', '--version', action='version', version='{} {}'.format(PROGRAM_NAME, PROGRAM_VERSION))
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='print debug messages')
    return parser.parse_args()


async def _create_home_folders(conf):
    cloud = await connect_to_cloud(config)

    users = await cloud.groups.get_group_users(int(config['userManagement']['userGroupId']))
    users_without_rooms = await get_users_without_personal_rooms(cloud, config['userManagement']['homeRootRoomNode'], users)

    logging.info('{} of {} users need new rooms'.format(len(users_without_rooms), len(users.items)))

    await create_personal_rooms(cloud, config['userManagement']['homeRootRoomNode'], users_without_rooms)

    await disconnect(cloud)


if __name__ == '__main__':
    args = _setup_argparser()
    config = load_config(args.config_file, log_level_overwrite=args.log_level)
    setup_logging(args, config)

    asyncio.run(_create_home_folders(config))

    sys.exit()

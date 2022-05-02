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
import logging
import asyncio  # noqa: F401
import sys
from dracoon import DRACOON, OAuth2ConnectionType


async def connect_to_cloud(config):
    logging.info('connecting: {}'.format(config['basic']['dracoonCloudInstance']))
    cloud = DRACOON(base_url=config['basic']['dracoonCloudInstance'], client_id=config['basic']['appID'], client_secret=config['basic']['secret'])
    try:
        await cloud.connect(OAuth2ConnectionType.password_flow, config['basic']['user'], config['basic']['password'])
    except Exception as err:
        logging.critical('Could not connect to {}: {}'.format(config['basic']['dracoonCloudInstance'], err))
        sys.exit('critical error')
    return cloud


async def disconnect(cloud):
    logging.info('disconnecting: {}'.format(cloud.settings.dracoon.base_url))
    try:
        await cloud.logout()
    except Exception as err:
        logging.warning('Clean logout failed: {}'.format(err))

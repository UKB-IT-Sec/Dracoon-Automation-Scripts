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
from helper.normalizer import normalize_username

TEN_GB = 1024*1024*1024*10


async def get_room_names(cloud, root_room_id):
    rooms = await cloud.nodes.get_nodes(room_manager=True, parent_id=int(root_room_id))
    room_names = set()
    for room in rooms.items:
        room_names.add(room.name)
    return room_names


async def get_users_without_personal_rooms(cloud, root_room_id, users):
    rooms = await get_room_names(cloud, root_room_id)
    users_without_room = list()
    for user in users.items:
        if normalize_username(user.userInfo.userName) not in rooms:
            users_without_room.append(user)
            logging.debug('{} ({}) has no room'.format(user.userInfo.userName, user.userInfo.id))
    return users_without_room


async def create_mail_attachment_folder(cloud, personal_room_id):
    folder_definition = cloud.nodes.make_folder(name='Outlook', parent_id=personal_room_id)
    await cloud.nodes.create_folder(folder_definition)


async def create_personal_rooms(cloud, root_room_id, users, quota=TEN_GB, recycle_bin_period=30):
    for user in users:
        room_definition = cloud.nodes.make_room(
            name=normalize_username(user.userInfo.userName),
            admin_ids=[cloud.user_info.id, user.userInfo.id],
            inherit_perms=False,
            parent_id=root_room_id,
            quota=quota,
            recycle_bin_period=recycle_bin_period)
        logging.debug(room_definition)
        logging.info('creating room for {}'.format(user.userInfo.userName))
        user_room = await cloud.nodes.create_room(room_definition)
        await create_mail_attachment_folder(cloud, user_room.id)

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


async def get_room_names(cloud, root_room_id):
    try:
        rooms = await cloud.nodes.get_nodes(room_manager=True, parent_id=int(root_room_id))
    except Exception as err:
        logging.critical('Could not get rooms in {}: {}'.format(root_room_id, err))
        sys.exit('critical error')
    room_names = set()
    for room in rooms.items:
        room_names.add(room.name)
    return room_names

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
import asyncio


async def list_groups(cloud):
    groups = await cloud.groups.get_groups()
    for item in groups.items:
        print('{} : {}'.format(item.id, item.name))


async def list_users_of_group(cloud, group_id):
    users = await cloud.groups.get_group_users(group_id)
    for item in users.items:
        print('{} : {}'.format(item.userInfo.id, item.userInfo.userName))

async def get_user_ids_of_group(cloud, group_id):
    users = await cloud.groups.get_group_users(group_id)
    user_ids = list()
    for user in users.items:
        user_ids.append(user.userInfo.id)
    return user_ids

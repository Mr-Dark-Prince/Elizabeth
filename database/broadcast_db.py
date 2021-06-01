# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from database import db_x

broadcast_db = db_x["BROADCAST_DB"]


async def add_broadcast_chat(chat_id):
    await broadcast_db.insert_one({"chat_id": chat_id})


async def rmbroadcast_chat(chat_id):
    await broadcast_db.delete_one({"chat_id": chat_id})


async def get_all_broadcast_chats():
    lol = [la async for la in broadcast_db.find({})]
    return lol


async def is_broadcast_chat_in_db(chat_id):
    k = await broadcast_db.find_one({"chat_id": chat_id})
    if k:
        return True
    else:
        return False

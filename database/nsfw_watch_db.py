# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from database import db_x

nsfw = db_x["NSFW_WATCH"]


async def add_chat(chat_id):
    await nsfw.insert_one({"chat_id": chat_id})


async def rm_chat(chat_id):
    await nsfw.delete_one({"chat_id": chat_id})


async def get_all_nsfw_chats():
    lol = [kek async for kek in nsfw.find({})]
    return lol


async def is_chat_in_db(chat_id):
    k = await nsfw.find_one({"chat_id": chat_id})
    if k:
        return True
    else:
        return False

# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from database import db_x

notes = db_x["NOTES"]


async def add_note(keyword, chat_id, message_id):
    stark = await notes.find_one({"keyword": keyword})
    if stark:
        await notes.update_one(
            {"keyword": keyword},
            {"$set": {"chat_id": chat_id, "msg_id": message_id}},
        )
    else:
        await notes.insert_one(
            {"keyword": keyword, "chat_id": chat_id, "msg_id": message_id}
        )


async def del_note(keyword, chat_id):
    await notes.delete_one({"keyword": keyword, "chat_id": chat_id})


async def del_notes(chat_id):
    await notes.delete_many({"chat_id": chat_id})


async def note_info(keyword, chat_id):
    r = await notes.find_one({"keyword": keyword, "chat_id": chat_id})
    if r:
        return r
    else:
        return False


async def all_note(chat_id):
    r = [u async for u in notes.find({"chat_id": chat_id})]
    if r:
        return r
    else:
        return False

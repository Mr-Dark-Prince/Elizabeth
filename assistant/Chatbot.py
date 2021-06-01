# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters

from database.chatbot_db import (
    add_blacklisted_user,
    is_user_blacklisted,
    rm_blacklisted_user,
)
from database.chatbot_msg_db import add_msg_in_db, get_user_id_frm_msg_id
from main_startup.__main__ import Friday, bot


async def my_id_(f, client, message):
    me = Friday.me.id
    if message.from_user.id == me:
        return bool(True)
    else:
        return bool(False)


owner_f = filters.create(func=my_id_, name="owner_f")

other_cmd_list = [
    "start",
    "help",
    "alive",
    "promote",
    "demote",
    "users",
    "id",
    "info",
    "ping",
    "tts",
    "tr",
    "broadcast",
    "block",
    "unblock",
]


@bot.on_message(
    filters.private & filters.incoming & ~owner_f & ~filters.command(other_cmd_list)
)
async def chat_bot(client, message):
    if await is_user_blacklisted(message.chat.id):
        return
    my_id = Friday.me.id
    owo = await message.forward(my_id)
    await add_msg_in_db(owo.message_id, message.from_user.id, message.message_id)


@bot.on_message(
    filters.private
    & filters.incoming
    & owner_f
    & ~filters.edited
    & ~filters.command(other_cmd_list)
)
async def reply_handler(client, message):
    if not message.reply_to_message:
        return
    msg_ = await get_user_id_frm_msg_id(message.reply_to_message.message_id)
    if not msg_:
        return
    try:
        await message.copy(msg_["sender_id"], reply_to_message_id=msg_["um_id"])
    except BaseException as e:
        await message.reply_text(
            f"Unable To Reply Message To This User \nTraceBack : {e}"
        )


@bot.on_message(
    filters.private & filters.incoming & owner_f & filters.command(["block"])
)
async def rip_blocked(client, message):
    if not message.reply_to_message:
        await message.reply_text("`Please Reply To A User!`")
        return
    msg_ = await get_user_id_frm_msg_id(message.reply_to_message.message_id)
    if not msg_:
        return
    if await is_user_blacklisted(msg_["sender_id"]):
        await message.reply_text("`This User is Already Blacklisted 😥`")
        return
    await add_blacklisted_user(msg_["sender_id"])
    await message.reply_text("`Sucessfully Blocked This User!`")


@bot.on_message(
    filters.private & filters.incoming & owner_f & filters.command(["unblock"])
)
async def rip_unblocked(client, message):
    if not message.reply_to_message:
        await message.reply_text("`Please Reply To A User!`")
        return
    msg_ = await get_user_id_frm_msg_id(message.reply_to_message.message_id)
    if not msg_:
        return
    if not await is_user_blacklisted(msg_["sender_id"]):
        await message.reply_text("`This User is Not Blacklisted 😥`")
        return
    await rm_blacklisted_user(msg_["sender_id"])
    await message.reply_text("`Sucessfully Un-Blocked This User!`")

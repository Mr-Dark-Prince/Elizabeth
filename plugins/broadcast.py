# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import logging

from database.broadcast_db import (
    add_broadcast_chat,
    get_all_broadcast_chats,
    is_broadcast_chat_in_db,
    rmbroadcast_chat,
)
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text


@friday_on_cmd(
    ["badd"],
    cmd_help={
        "help": "Add Group/Channel For Broadcast!. Give input as 'all' to add all.",
        "example": "{ch}badd @fridaysupportofficial",
    },
)
async def badd(client, message):
    pablo = await edit_or_reply(message, "`Processing..`")
    bd = get_text(message)
    if not bd:
        await pablo.edit("`Check Help Menu On How To Use This Command!`")
        return
    sed = 0
    oks = 0
    zxz = ["channel", "supergroup"]
    nd = ["creator", "administrator"]
    if bd.lower() == "all":
        await pablo.edit("`Adding All Channel TO DB.`")
        async for dialog in client.iter_dialogs():
            if dialog.chat.type in zxz:
                x = await client.get_chat_member(dialog.chat.id, message.from_user.id)
                if x.status in nd:
                    if not await is_broadcast_chat_in_db(dialog.chat.id):
                        await add_broadcast_chat(dialog.chat.id)
                        oks += 1
                    else:
                        sed += 1
        await pablo.edit(
            f"Successfully Added {oks} Groups/Channels to DB.\nTotal Groups/Channels in dB {oks+sed} "
        )
    else:
        chnl_id = await get_final_id(bd, client)
        if not chnl_id:
            await pablo.edit("`Invalid Channel Id/Username`")
            return
        if await is_broadcast_chat_in_db(chnl_id):
            await pablo.edit("`This Channel is Already In dB!`")
            return
        await add_broadcast_chat(chnl_id)
        await pablo.edit(f"`Successfully Added {bd} in dB!`")


@friday_on_cmd(
    ["brm"],
    cmd_help={
        "help": "Remove Group/Channel From Broadcast dB!. Give input as 'all' to Remove all.",
        "example": "{ch}brm @fridaysupportofficial",
    },
)
async def brm(client, message):
    pablo = await edit_or_reply(message, "`Processing..`")
    bd = get_text(message)
    Jill = 0
    if not bd:
        await pablo.edit("`Check Help Menu On How To Use This Command!`")
        return
    if bd.lower() == "all":
        await pablo.edit("`Removing All Channel From DB.`")
        all = await get_all_broadcast_chats()
        for chnnl in all:
            await rmbroadcast_chat(chnnl["chat_id"])
            Jill += 1
        await pablo.edit(f"Successfully Removed {Jill} Groups/Channels from dB")
    else:
        chnl_id = await get_final_id(bd, client)
        if not chnl_id:
            await pablo.edit("`Invalid Channel Id/Username`")
            return
        if not await is_broadcast_chat_in_db(chnl_id):
            await pablo.edit("`This Channel is Not In dB!`")
            return
        await add_broadcast_chat(chnl_id)
        await pablo.edit(f"`Successfully Added {bd} in dB!`")


@friday_on_cmd(
    ["broadcast"],
    cmd_help={
        "help": "Broadcast Message In All Groups/Channels which are added in dB.",
        "example": "{ch}broadcast (replying to broadcast message)",
    },
)
async def broadcast(client, message):
    pablo = await edit_or_reply(
        message, "**Fine. Broadcasting in Progress. Kindly Wait !**"
    )
    leat = await get_all_broadcast_chats()
    S = 0
    F = 0
    if len(leat) == 0:
        await pablo.edit("No Channel Or Group Found On Database. Please Check Again")
        return
    if not message.reply_to_message:
        await pablo.edit("Reply To A Message To Broadcast")
        return
    for lolol in leat:
        try:
            await client.copy_message(
                chat_id=lolol["chat_id"],
                from_chat_id=message.chat.id,
                message_id=message.reply_to_message.message_id,
            )
            S += 1
        except Exception as e:
            logging.error(f"[Broadcast] {e}")
            F += 1
    await pablo.edit(
        f"Successfully Broadcasted Message in {S} groups/channels. Failed in {F}"
    )


async def get_final_id(query, client):
    is_int = True
    try:
        in_t = int(query)
    except:
        is_int = False
    chnnl = in_t if is_int else str(query)
    try:
        return (await client.get_chat(chnnl)).id
    except:
        return None

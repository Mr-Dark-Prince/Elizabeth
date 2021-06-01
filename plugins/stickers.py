# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import datetime
import math
import os
import zipfile
from collections import defaultdict
from io import BytesIO

from PIL import Image
from pyrogram import emoji
from pyrogram.errors import StickersetInvalid, YouBlockedUser
from pyrogram.raw.functions.messages import GetStickerSet
from pyrogram.raw.types import InputStickerSetShortName

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from main_startup.helper_func.plugin_helpers import convert_to_image


@friday_on_cmd(
    ["packinfo"],
    cmd_help={
        "help": "Get Sticker Pack Info!",
        "example": "{ch}packinfo (reply to sticker)",
    },
)
async def packinfo(client, message):
    pablo = await edit_or_reply(message, "`Processing...`")
    if not message.reply_to_message:
        await pablo.edit("Please Reply To Sticker...")
        return
    if not message.reply_to_message.sticker:
        await pablo.edit("Please Reply To Sticker...")
        return
    if not message.reply_to_message.sticker.set_name:
        await pablo.edit("`Seems Like A Stray Sticker!`")
        return
    stickerset = await client.send(
        GetStickerSet(
            stickerset=InputStickerSetShortName(
                short_name=message.reply_to_message.sticker.set_name
            )
        )
    )
    emojis = []
    for stucker in stickerset.packs:
        if stucker.emoticon not in emojis:
            emojis.append(stucker.emoticon)
    output = f"""**Sticker Pack Title **: `{stickerset.set.title}`
**Sticker Pack Short Name **: `{stickerset.set.short_name}`
**Stickers Count **: `{stickerset.set.count}`
**Archived **: `{stickerset.set.archived}`
**Official **: `{stickerset.set.official}`
**Masks **: `{stickerset.set.masks}`
**Animated **: `{stickerset.set.animated}`
**Emojis In Pack **: `{' '.join(emojis)}`
"""
    await pablo.edit(output)


@friday_on_cmd(
    ["kang"],
    cmd_help={
        "help": "Get Sticker Pack Info!",
        "example": "{ch}packinfo (reply to sticker)",
    },
)
async def packinfo(client, message):
    pablo = await edit_or_reply(message, "`Using Megic To Kang This Sticker...`")
    if not message.reply_to_message:
        await pablo.edit("Please Reply To Sticker...")
        return
    Hell = get_text(message)
    name = ""
    pack = 1
    nm = message.from_user.username
    if nm:
        nam = message.from_user.username
        name = nam[1:]
    else:
        name = message.from_user.first_name
    packname = f"@{nm} Kang Pack {pack}"
    packshortname = f"FRIDAY_{message.from_user.id}_{pack}"
    non = [None, "None"]
    emoji = "😁"
    try:
        Hell = Hell.strip()
        if not Hell.isalpha():
            if not Hell.isnumeric():
                emoji = Hell
        else:
            emoji = "😁"
    except:
        emoji = "😁"
    exist = None
    is_anim = False
    if message.reply_to_message.sticker:
        if not Hell:
            emoji = message.reply_to_message.sticker.emoji or "😁"
        is_anim = message.reply_to_message.sticker.is_animated
        if is_anim:
            packshortname += "_animated"
            packname += " Animated"
        if message.reply_to_message.sticker.mime_type == "application/x-tgsticker":
            file_name = await message.reply_to_message.download("AnimatedSticker.tgs")
        else:
            cool = await convert_to_image(message, client)
            if not cool:
                await pablo.edit("`Reply to a valid media first.`")
                return
            file_name = resize_image(cool)
    elif message.reply_to_message.document:
        if message.reply_to_message.document.mime_type == "application/x-tgsticker":
            is_anim = True
            packshortname += "_animated"
            packname += " Animated"
            file_name = await message.reply_to_message.download("AnimatedSticker.tgs")
    else:
        cool = await convert_to_image(message, client)
        if not cool:
            await pablo.edit("`Reply to a valid media first.`")
            return
        file_name = resize_image(cool)
    try:
        exist = await client.send(
            GetStickerSet(stickerset=InputStickerSetShortName(short_name=packshortname))
        )
    except StickersetInvalid:
        pass
    if exist:
        try:
            await client.send_message("stickers", "/addsticker")
        except YouBlockedUser:
            await pablo.edit("`Please Unblock @Stickers`")
            await client.unblock_user("stickers")
        await client.send_message("stickers", packshortname)
        await asyncio.sleep(0.2)
        limit = "50" if is_anim else "120"
        messi = (await client.get_history("stickers", 1))[0]
        while limit in messi.text:
            pack += 1
            prev_pack = int(pack) - 1
            await pablo.edit(f"Kang Pack Vol __{prev_pack}__ is Full! Switching To Vol __{pack}__ Kang Pack")
            packname = f"@{nm} Kang Pack {pack}"
            packshortname = f"FRIDAY_{message.from_user.id}_{pack}"
            if is_anim:
                packshortname += "_animated"
                packname += " Animated"
            await client.send_message("stickers", packshortname)
            await asyncio.sleep(0.2)
            messi = (await client.get_history("stickers", 1))[0]
            if messi.text == "Invalid pack selected.":
                if is_anim:
                    await client.send_message("stickers", "/newanimated")
                else:
                    await client.send_message("stickers", "/newpack")
                await asyncio.sleep(0.5)
                await client.send_message("stickers", packname)
                await asyncio.sleep(0.2)
                await client.send_document("stickers", file_name)
                await asyncio.sleep(1)
                await client.send_message("stickers", emoji)
                await asyncio.sleep(0.5)
                await client.send_message("stickers", "/publish")
                if is_anim:
                    await client.send_message("stickers", f"<{packname}>")
                await client.send_message("stickers", "/skip")
                await asyncio.sleep(0.5)
                await client.send_message("stickers", packshortname)
                await pablo.edit(
                    f"Sticker Added To Your Pack With Emoji - {emoji}. You Can Find It [Here](https://t.me/addstickers/{packshortname})"
                )
                return
        await client.send_document("stickers", file_name)
        await asyncio.sleep(1)
        await client.send_message("stickers", emoji)
        await asyncio.sleep(0.5)
        await client.send_message("stickers", "/done")
        await pablo.edit(
            f"`Sticker Added To Your Pack With Emoji - {emoji}. You Can Find It` [Here](https://t.me/addstickers/{packshortname})"
        )
    else:
        if is_anim:
            await client.send_message("stickers", "/newanimated")
        else:
            await client.send_message("stickers", "/newpack")
        await client.send_message("stickers", packname)
        await asyncio.sleep(0.2)
        await client.send_document("stickers", file_name)
        await asyncio.sleep(1)
        await client.send_message("stickers", emoji)
        await asyncio.sleep(0.5)
        await client.send_message("stickers", "/publish")
        await asyncio.sleep(0.5)
        if is_anim:
            await client.send_message("stickers", f"<{packname}>")
        await client.send_message("stickers", "/skip")
        await asyncio.sleep(0.5)
        await client.send_message("stickers", packshortname)
        await pablo.edit(
            f"`Sticker Added To Your Pack With Emoji - {emoji}. You Can Find It` [Here](https://t.me/addstickers/{packshortname})"
        )
        if os.path.exists(file_name):
            os.remove(file_name)


def resize_image(image):
    im = Image.open(image)
    maxsize = (512, 512)
    if (im.width and im.height) < 512:
        size1 = im.width
        size2 = im.height
        if im.width > im.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        im = im.resize(sizenew)
    else:
        im.thumbnail(maxsize)
    file_name = "Sticker_FridayUB.png"
    im.save(file_name, "PNG")
    if os.path.exists(image):
        os.remove(image)
    return file_name

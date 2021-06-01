# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import os
import time
from datetime import datetime

import gtts
import requests
from google_trans_new import google_translator
from googletrans import LANGUAGES
from gtts import gTTS
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from langdetect import detect
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.bot_users import add_user, check_user, get_all_users
from main_startup import bot, start_time
from main_startup.config_var import Config
from main_startup.helper_func.assistant_helpers import (
    _check_admin,
    _check_owner_or_sudos,
)
from main_startup.helper_func.basic_helpers import get_all_pros, get_readable_time


@bot.on_message(filters.command(["start"]) & filters.incoming)
async def start(client, message):
    all_user_s = await get_all_pros()
    starkbot = client.me
    bot_name = starkbot.first_name
    bot_username = starkbot.username
    firstname = message.from_user.first_name
    user_id = message.from_user.id
    starttext = f"`Hello, {firstname} ! Nice To Meet You, Well I Am {bot_name}, An Powerfull Assistant Bot To Talk And Do Many Things For My Master!`. \n\nPowered By [Friday Userbot](t.me/FridayOT)"
    mypic = Config.ASSISTANT_START_PIC
    if user_id not in all_user_s:
        await client.send_photo(
            message.chat.id,
            mypic,
            starttext,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Help Me ❓", url="t.me/Fridayot")]]
            ),
        )
        kok = await check_user(user_id)
        if not kok:
            await add_user(user_id)
    else:
        message87 = f"Hi Master, It's Me {bot_name}, Your Assistant ! \nWhat You Wanna Do today ?"
        await client.send_photo(
            message.chat.id,
            mypic,
            message87,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Add Me to Group 👥",
                            url=f"t.me/{bot_username}?startgroup=true",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Commands For Assistant", callback_data="cmdgiv"
                        )
                    ],
                ]
            ),
        )


@bot.on_callback_query(filters.regex("cmdgiv"))
async def cmdgiv(client, cb):
    grabon = "Hello Here Are Some Commands \n➤ /start - Check if I am Alive \n➤ /ping - Pong! \n➤ /tr (lang-code) \n➤ /tts (lang-code) \n➤ /promote - Promote a user \n➤ /broadcast - Sends Message To all Users In Bot \n➤ /id - Shows ID of User And Chat \n➤ /info - Shows INFO of User \n➤ /users - Get List Of Users In dB. "
    await cb.edit_message_text(grabon)


@bot.on_message(filters.command(["alive"]) & filters.incoming)
@_check_owner_or_sudos
async def alive(client, message):
    lol = client.me
    await message.reply(
        f"`Yo ! {message.from_user.first_name} , I am Alive. Need Help ? How Are You? 🤟`"
    )


@bot.on_message(filters.command(["help"]) & filters.incoming)
@_check_owner_or_sudos
async def fuckinhelp(client, message):
    grabon = "Hello Here Are Some Commands \n➤ /start - Check if I am Alive \n➤ /ping - Pong! \n➤ /tr (lang-code) \n➤ /tts (lang-code) \n➤ /promote - Promote a user \n➤ /demote - Demote a user \n➤ /broadcast - Sends Message To all Users In Bot \n➤ /id - Shows ID of User And Chat \n➤ /info - Shows INFO of User \n➤ /users - Get List Of Users In dB. "
    await message.reply(grabon)


@bot.on_message(filters.regex("users") & filters.incoming & filters.private)
@_check_owner_or_sudos
async def user_s(client, message):
    users_list = "List Of Total Users In Bot. \n\n"
    total_users = await get_all_users()
    for starked in total_users:
        users_list += ("==> {} \n").format(int(starked.get("user_id")))
    with open("users.txt", "w") as f:
        f.write(users_list)
    await message.reply_document("users.txt", caption="Users In Your dB")


@bot.on_message(filters.command(["promote"]) & filters.group)
@_check_admin
async def promote_me(client, message):
    pablo = await message.reply("Processing...")
    if not message.reply_to_message:
        await pablo.edit("Please Reply To A User")
        return
    lol = client.me
    user_s = await message.chat.get_member(lol.id)
    if user_s.status in ("creator", "administrator"):
        pass
    else:
        await pablo.edit("`I Don't Have Enough Permissions To Promote!`")
        return
    text_to_return = message.text
    try:
        title = message.text.split(None, 1)[1]
    except IndexError:
        title = None
    await pablo.edit("`Promoting This User!`")
    try:
        await client.promote_chat_member(
            message.chat.id, message.reply_to_message.from_user.id
        )
    except:
        await pablo.edit("`I Don't Have Enough Permissions To Promote!`")
        return
    await pablo.edit("`Promoted The User Successfully!`")
    if title:
        await client.set_administrator_title(
            message.chat.id, message.reply_to_message.from_user.id, title
        )


@bot.on_message(filters.command(["demote"]) & filters.group)
@_check_admin
async def demote_you(client, message):
    pablo = await message.reply("Processing...")
    if not message.reply_to_message:
        await pablo.edit("Please Reply To A User")
        return
    lol = client.me
    user_s = await message.chat.get_member(lol.id)
    if user_s.status in ("creator", "administrator"):
        pass
    else:
        await pablo.edit("`I Don't Have Enough Permissions To Demote!`")
        return
    await pablo.edit("`Demoting The User!`")
    try:
        await client.promote_chat_member(
            message.chat.id,
            message.reply_to_message.from_user.id,
            is_anonymous=False,
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=False,
            can_restrict_members=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        )
    except:
        await pablo.edit("`I Don't Have Enough Permissions To Demote!`")
        return
    await pablo.edit("`Demoted The User Successfully!`")


@bot.on_message(filters.command(["id"]) & filters.incoming)
async def id(client, message):
    if message.reply_to_message is None:
        await message.reply(f"This chat's ID is: {message.chat.id}")
    else:
        test = f"Replied User's ID is: {message.reply_to_message.from_user.id}\n\nThis chat's ID is: {message.chat.id}"
        await message.reply(test)


@bot.on_message(filters.command(["info"]) & filters.incoming)
async def info(client, message):
    if message.reply_to_message:
        username = message.reply_to_message.from_user.username
        id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
        user_link = message.reply_to_message.from_user.mention
    else:
        username = message.from_user.username
        id = message.from_user.id
        first_name = message.from_user.first_name
        user_link = message.from_user.mention
    if username:
        username = f"@{username}"
        text = f"""
<b>User info</b>:
ID: <code>{id}</code>
First Name: {first_name}
Username: {username}
User link: {user_link}"""
    else:
        text = f"""
<b>User info</b>:
ID: <code>{id}</code>
First Name: {first_name}
User link: {user_link}"""
    await message.reply(text, parse_mode="HTML")


@bot.on_message(filters.command(["ping"]) & filters.incoming)
@_check_owner_or_sudos
async def ping(client, message):
    uptime = get_readable_time((time.time() - start_time))
    start = datetime.now()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await client.send_message(
        message.chat.id,
        f"**█▀█ █▀█ █▄░█ █▀▀ █ \n█▀▀ █▄█ █░▀█ █▄█ ▄**\n ➲ `{ms}` \n ➲ `{uptime}`",
    )


@bot.on_message(filters.command(["tts"]) & filters.incoming)
@_check_owner_or_sudos
async def tts_(client, message):
    stime = time.time()
    text_to_return = message.text
    lol = await message.reply("Processing....")
    try:
        lang = message.text.split(None, 1)[1]
    except IndexError:
        lang = "en"
    if not message.reply_to_message:
        await lol.edit("`Reply To Text To Convert To Text!`")
        return
    text = message.reply_to_message.text
    language = lang
    kk = gtts.lang.tts_langs()
    if not kk.get(language):
        await lol.edit("`Unsupported Language!`")
        return
    await client.send_chat_action(message.chat.id, "record_audio")
    tts = gTTS(text, lang=language)
    tts.save(f"{kk.get(language)}.ogg")
    google_translator()
    dec_s = detect(text)
    etime = time.time()
    hmm_time = round(etime - stime)
    duration = 0
    metadata = extractMetadata(createParser(f"{kk.get(language)}.ogg"))
    if metadata and metadata.has("duration"):
        duration = metadata.get("duration").seconds
    owoc = f"**TTS** \n**Detected Text Language :** `{dec_s.capitalize()}` \n**Speech Text :** `{kk.get(language)}` \n**Time Taken :** `{hmm_time}s` \n__Powered By @FridayOT__"
    await message.reply_audio(
        audio=f"{kk.get(language)}.ogg", caption=owoc, duration=duration
    )
    await client.send_chat_action(message.chat.id, action="cancel")
    os.remove(f"{kk.get(language)}.ogg")
    await lol.delete()


@bot.on_message(filters.command(["tr"]) & filters.incoming)
@_check_owner_or_sudos
async def tr(client, message):
    text_to_return = message.text
    try:
        lang = message.text.split(None, 1)[1]
    except IndexError:
        lang = "en"
    if not message.reply_to_message:
        await message.reply("Reply To Text To Translate")
        return
    text = message.reply_to_message.text
    translator = google_translator()
    source_lan = detect(text)
    transl_lan = LANGUAGES[lang]
    translated = translator.translate(text, lang_tgt=lang)
    tr_text = f"""**Source ({source_lan.capitalize()})**:
`{text}`
**Translation ({transl_lan.capitalize()})**:
`{translated}`"""
    if len(tr_text) >= 4096:
        url = "https://del.dog/documents"
        r = requests.post(url, data=tr_text.encode("UTF-8")).json()
        url2 = f"https://del.dog/{r['key']}"
        tr_text = (
            f"Translated Text Was Too Big, Never Mind I Have Pasted It [Here]({url2})"
        )
    await message.reply(tr_text)


@bot.on_message(filters.command(["broadcast"]) & filters.incoming)
@_check_owner_or_sudos
async def broadcast(client, message):
    msg = None
    lol = await message.reply("`Processing!`")
    if message.reply_to_message:
        msg = True
    else:
        await lol.edit("`Please Reply Message To Broadcast!`")
        return
    if msg == None:
        await lol.edit("`Please Reply Message To Broadcast!`")
        return
    s = 0
    f = 0
    total_users = await get_all_users()
    tett = "**▶ You Received A BroadCast Message :**"
    for user in total_users:
        user_id = user.get("user_id")
        try:
            await client.send_message(user_id, tett)
            await message.reply_to_message.copy(user_id)
            s += 1
        except:
            f += 1
    if f > 0:
        await lol.edit(
            f"Successfully Broadcasted to {s} users. Failed To Broadcast To {f} users.  Maybe They Blocked The Bot"
        )
    else:
        await lol.edit(f"Successfully Broadcasted to {s} users.")

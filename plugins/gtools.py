# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.


from pyrogram import filters

from database.gbandb import gban_info, gban_list, gban_user, ungban_user
from database.gmutedb import gmute, is_gmuted, ungmute
from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd, listen
from main_startup.helper_func.basic_helpers import (
    edit_or_reply,
    edit_or_send_as_file,
    get_text,
    get_user,
    iter_chats,
)
from main_startup.helper_func.logger_s import LogIt
from plugins import devs_id


@friday_on_cmd(
    ["gmute"],
    cmd_help={
        "help": "Globally Mute The User!",
        "example": "{ch}gmute (reply to user messages OR provide his ID)",
    },
)
async def gmute_him(client, message):
    g = await edit_or_reply(message, "`Processing..`")
    text_ = get_text(message)
    user, reason = get_user(message, text_)
    if not user:
        await g.edit("`Reply To User Or Mention To Gmute Him`")
        return
    try:
        userz = await client.get_users(user)
    except:
        await g.edit(f"`404 : User Doesn't Exists In This Chat !`")
        return
    if not reason:
        reason = "Just_Gmutted!"
    if userz.id == (client.me).id:
        await g.edit("`Oh, This is So Funny Btw :/`")
        return
    if userz.id in devs_id:
        await g.edit("`Sadly, I Can't Do That!`")
        return
    if userz.id in Config.AFS:
        await g.edit("`Sudo Users Can't Be Gmutted! Remove Him And Try Again!`")
        return
    if await is_gmuted(userz.id):
        await g.edit("`Re-Gmute? Seriously? :/`")
        return
    await gmute(userz.id, reason)
    gmu = f"**#Gmutted** \n**User :** `{userz.id}` \n**Reason :** `{reason}`"
    await g.edit(gmu)
    log = LogIt(message)
    await log.log_msg(client, gmu)


@friday_on_cmd(
    ["ungmute"],
    cmd_help={
        "help": "Globally UnMute The User!",
        "example": "{ch}ungmute (reply to user message OR provide his ID)",
    },
)
async def gmute_him(client, message):
    ug = await edit_or_reply(message, "`Processing..`")
    text_ = get_text(message)
    user_ = get_user(message, text_)[0]
    if not user_:
        await ug.edit("`Reply To User Or Mention To Un-Gmute Him`")
        return
    try:
        userz = await client.get_users(user_)
    except:
        await ug.edit(f"`404 : User Doesn't Exists In This Chat !`")
        return
    if userz.id == (client.me).id:
        await ug.edit("`Oh, This is So Funny Btw :/`")
        return
    if userz.id in Config.AFS:
        await ug.edit("`Sudo Users Can't Be Un-Gmutted! Remove Him And Try Again!`")
        return
    if not await is_gmuted(userz.id):
        await ug.edit("`Un-Gmute A Non Gmutted User? Seriously? :/`")
        return
    await ungmute(userz.id)
    ugmu = f"**#Un-Gmutted** \n**User :** `{userz.id}`"
    await ug.edit(ugmu)
    log = LogIt(message)
    await log.log_msg(client, ugmu)


@friday_on_cmd(
    ["gban"],
    cmd_help={
        "help": "Globally Ban The User!",
        "example": "{ch}gban (reply to user message OR provide his ID)",
    },
)
async def gbun_him(client, message):
    gbun = await edit_or_reply(message, "`Processing..`")
    text_ = get_text(message)
    user, reason = get_user(message, text_)
    failed = 0
    if not user:
        await gbun.edit("`Reply To User Or Mention To GBan Him`")
        return
    try:
        userz = await client.get_users(user)
    except:
        await gbun.edit(f"`404 : User Doesn't Exists In This Chat !`")
        return
    if not reason:
        reason = "Private Reason!"
    if userz.id == (client.me).id:
        await gbun.edit("`Oh, This is So Funny Btw :/`")
        return
    if userz.id in devs_id:
        await g.edit("`Sadly, I Can't Do That!`")
        return
    if userz.id in Config.AFS:
        await gbun.edit("`Sudo Users Can't Be Gbanned! Remove Him And Try Again!`")
        return
    if await gban_info(userz.id):
        await gbun.edit("`Re-Gban? Seriously? :/`")
        return
    await gbun.edit("`Please, Wait Fectching Your Chats!`")
    chat_dict = await iter_chats(client)
    chat_len = len(chat_dict)
    if not chat_dict:
        gbun.edit("`You Have No Chats! So Sad`")
        return
    await gbun.edit("`Starting GBans Now!`")
    for ujwal in chat_dict:
        try:
            await client.kick_chat_member(ujwal, int(userz.id))
        except:
            failed += 1
    await gban_user(userz.id, reason)
    gbanned = f"**#GBanned** \n**User :** [{userz.first_name}](tg://user?id={userz.id}) \n**Reason :** `{reason}` \n**Affected Chats :** `{chat_len-failed}`"
    await gbun.edit(gbanned)
    log = LogIt(message)
    await log.log_msg(client, gbanned)


@friday_on_cmd(
    ["ungban"],
    cmd_help={
        "help": "Globally Unban The User!",
        "example": "{ch}ungban (reply to user messages OR provide his ID)",
    },
)
async def ungbun_him(client, message):
    ungbun = await edit_or_reply(message, "`Processing..`")
    text_ = get_text(message)
    user = get_user(message, text_)[0]
    failed = 0
    if not user:
        await ungbun.edit("`Reply To User Or Mention To Un-GBan Him`")
        return
    try:
        userz = await client.get_users(user)
    except:
        await ungbun.edit(f"`404 : User Doesn't Exists!`")
        return
    if userz.id == (client.me).id:
        await ungbun.edit("`Oh, This is So Funny Btw :/`")
        return
    if not await gban_info(userz.id):
        await ungbun.edit("`Un-Gban A Ungbanned User? Seriously? :/`")
        return
    await ungbun.edit("`Please, Wait Fectching Your Chats!`")
    chat_dict = await iter_chats(client)
    chat_len = len(chat_dict)
    if not chat_dict:
        ungbun.edit("`You Have No Chats! So Sad`")
        return
    await ungbun.edit("`Starting Un-GBans Now!`")
    for ujwal in chat_dict:
        try:
            await client.unban_chat_member(ujwal, int(userz.id))
        except:
            failed += 1
    await ungban_user(userz.id)
    ungbanned = f"**#Un_GBanned** \n**User :** [{userz.first_name}](tg://user?id={userz.id}) \n**Affected Chats :** `{chat_len-failed}`"
    await ungbun.edit(ungbanned)
    log = LogIt(message)
    await log.log_msg(client, ungbanned)


@listen(filters.incoming & ~filters.me & ~filters.user(Config.AFS))
async def watch(client, message):
    if not message:
        return
    if not message.from_user:
        return
    user = message.from_user.id
    if await is_gmuted(user):
        try:
            await message.delete()
        except:
            return
    if await gban_info(user):
        if message.chat.type != "supergroup":
            return
        try:
            me_ = await message.chat.get_member(int(client.me.id))
        except:
            return
        if not me_.can_restrict_members:
            return
        try:
            await client.kick_chat_member(message.chat.id, int(user))
        except:
            return
        await client.send_message(
            message.chat.id,
            f"**#GbanWatch** \n**Chat ID :** `{message.chat.id}` \n**User :** `{user}` \n**Reason :** `{await gban_info(user)}`",
        )
    


@friday_on_cmd(
    ["gbanlist"],
    cmd_help={
        "help": "Get List Of Globally Banned Users!",
        "example": "{ch}gbanlist (reply to user messages OR provide his ID)",
    },
)
async def give_glist(client, message):
    oof = "**#GBanList** \n\n"
    glist = await edit_or_reply(message, "`Processing..`")
    list_ = await gban_list()
    if len(list_) == 0:
        await glist.edit("`No User is Gbanned Till Now!`")
        return
    for lit in list_:
        oof += f"**User :** `{lit['user']}` \n**Reason :** `{lit['reason']}` \n\n"
    await edit_or_send_as_file(oof, glist, client, "GbanList", "Gban-List")


@friday_on_cmd(
    ["gbroadcast"],
    cmd_help={
        "help": "Send Message To All Chats, You Are In!",
        "example": "{ch}gbroadcast (replying to message)",
    },
)
async def gbroadcast(client, message):
    msg_ = await edit_or_reply(message, "`Fetching Your ChatList!`")
    failed = 0
    if not message.reply_to_message:
        await msg_.edit("`Reply To Message Boss!`")
        return
    chat_dict = await iter_chats(client)
    chat_len = len(chat_dict)
    await msg_.edit("`Now Sending To All Chats Possible!`")
    if not chat_dict:
        msg_.edit("`You Have No Chats! So Sad`")
        return
    for c in chat_dict:
        try:
            msg = await message.reply_to_message.copy(c)
        except:
            failed += 1
    await msg_.edit(
        f"`Message Sucessfully Send To {chat_len-failed} Chats! Failed In {failed} Chats.`"
    )

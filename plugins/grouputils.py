# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.


import asyncio
import os
import time
from asyncio import sleep

from pyrogram.types import ChatPermissions
import pyrogram
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import (
    edit_or_reply,
    edit_or_send_as_file,
    get_text,
    get_user,
    is_admin_or_owner,
)
from main_startup.helper_func.logger_s import LogIt
from main_startup.helper_func.plugin_helpers import (
    convert_to_image,
    convert_vid_to_vidnote,
    generate_meme,
)


@friday_on_cmd(
    ["silentpin"],
    only_if_admin=True,
    cmd_help={
        "help": "Pin Message Without Sending Notification To Members!",
        "example": "{ch}silentpin (reply to message)",
    },
)
async def spin(client, message):
    if not message.reply_to_message:
        await edit_or_reply(message, "`Reply To A Message To Pin!`")
    try:
        await client.pin_chat_message(
            message.chat.id,
            message.reply_to_message.message_id,
            disable_notification=True,
        )
    except BaseException as e:
        await edit_or_reply(
            message, f"`I Am UnAble To Pin That Message` \n**Error :** `{e}`"
        )
        return
    await edit_or_reply(message, "`I Have Pinned This Message!`")


@friday_on_cmd(
    ["pinloud", "pin"],
    only_if_admin=True,
    cmd_help={
        "help": "Pin Message With Sending Notification To Members!",
        "example": "{ch}pin (reply to messages)",
    },
)
async def lpin(client, message):
    if not message.reply_to_message:
        await edit_or_reply(message, "`Reply To A Message To Pin!`")
    try:
        await client.pin_chat_message(
            message.chat.id, message.reply_to_message.message_id
        )
    except BaseException as e:
        await edit_or_reply(
            message, f"`I Am UnAble To Pin That Message` \n**Error :** `{e}`"
        )
        return
    await edit_or_reply(message, "`Message Pinned Successfully!`")


@friday_on_cmd(
    ["unpin", "rmpins"],
    only_if_admin=True,
    cmd_help={"help": "Unpin All Pinned Messages!", "example": "{ch}rmpins"},
)
async def dpins(client, message):
    await client.unpin_all_chat_messages(message.chat.id)
    await edit_or_reply(message, "`All Pinned Messages Unpinned Successfully!`")


@friday_on_cmd(
    ["adminlist", "admins"],
    cmd_help={"help": "Get Adminlist Of Chat!", "example": "{ch}adminlist"},
)
async def midhunadmin(client, message):
    mentions = ""
    starky = get_text(message) if get_text(message) else message.chat.id
    pablo = await edit_or_reply(message, "`Searching For Admins!`")
    try:
        X = await client.get_chat_members(starky, filter="administrators")
        ujwal = await client.get_chat(starky)
    except BaseException as e:
        await pablo.edit(f"Couldn't Fetch Chat Admins, \n\n**TraceBack :** `{e}`")
        return
    for midhun in X:
        if not midhun.user.is_deleted:
            link = f'✱ <a href="tg://user?id={midhun.user.id}">{midhun.user.first_name}</a>'
            userid = f"<code>{midhun.user.id}</code>"
            mentions += f"\n{link} {userid}"
    holy = ujwal.username if ujwal.username else ujwal.id
    messag = f"""
<b>Admins in {ujwal.title} | {holy}</b>

{mentions}
"""
    await edit_or_send_as_file(
        messag,
        pablo,
        client,
        f"`AdminList Of {holy}!`",
        "admin-lookup-result",
        "html",
    )


@friday_on_cmd(
    ["botlist", "bot"],
    group_only=True,
    cmd_help={"help": "Get List Of Bots In Chat!", "example": "{ch}botlist"},
)
async def bothub(client, message):
    buts = "**Bot List** \n\n"
    nos = 0
    starky = get_text(message) if get_text(message) else message.chat.id
    pablo = await edit_or_reply(message, "`Searching For Bots!`")
    try:
        bots = await client.get_chat_members(starky, filter="bots")
    except BaseException as e:
        await pablo.edit(f"Couldn't Fetch Chat Admins, \n**TraceBack :** `{e}`")
        return
    for ujwal in bots:
        nos += 1
        buts += f"{nos}〉 [{ujwal.user.first_name}](tg://user?id={ujwal.user.id}) \n"
    await pablo.edit(buts)


@friday_on_cmd(
    ["zombies", "delusers"],
    cmd_help={
        "help": "Remove Deleted Accounts In The Group/Channel!",
        "example": "{ch}zombies",
    },
)
async def ujwalzombie(client, message):
    pablo = await edit_or_reply(message, "`Searching For Zombies 🧟 .....`")
    if len(message.text.split()) == 1:
        dm = 0
        da = 0
        dc = 0
        async for member in client.iter_chat_members(message.chat.id):
            if member.user.is_deleted:
                await sleep(1)
                if member.status == "member":
                    dm += 1
                elif member.status == "administrator":
                    da += 1
                elif member.status == "creator":
                    dc += 1
        text = "**Zombies Report!** \n\n"
        if dm > 0:
            text += f"**Total Zombies (Members) :** `{dm}` \n"
        if da > 0:
            text += f"\n**Total Zombies (Admins) :** `{da}` \n"
        if dc > 0:
            text += "\n__This Group Owner Deleted His Account :/__ \n"
        d = dm + da + dc
        if d > 0:
            text += (
                "\n\nClean These Deleted Accounts By Using `.zombies clean` Command!"
            )
            await pablo.edit(text)
        else:
            await pablo.edit("No Zombies Found. Group is Clean 😊")
        return
    sgname = message.text.split(None, 1)[1]
    if sgname.lower().strip() == "clean":
        me = client.me
        lol = await is_admin_or_owner(message, me.id)
        if not lol:
            await pablo.edit("`I am not an admin here!`")
            return
        s = 0
        f = 0
        async for member in client.iter_chat_members(message.chat.id):
            if member.user.is_deleted:
                try:
                    await client.kick_chat_member(message.chat.id, member.user.id)
                    s += 1
                except:
                    f += 1
        text = ""
        if s > 0:
            text += f"Successfully Removed {s} Zombies"
        if f > 0:
            text += (
                f"\nFailed to remove {f} zombies as they are either admins or creator"
            )
        await pablo.edit(text)


@friday_on_cmd(
    ["ban", "bun"],
    only_if_admin=True,
    group_only=True,
    cmd_help={
        "help": "Ban Replied User or provide his ID!",
        "example": "{ch}ban (reply to user message OR provide his ID)",
    },
)
async def ban_world(client, message):
    bun = await edit_or_reply(message, "`Trying To Ban User!`")
    me_m = client.me
    me_ = await message.chat.get_member(int(me_m.id))
    if not me_.can_restrict_members:
        await bun.edit("`Boss, You Don't Have Ban Permission!`")
        return
    text_ = get_text(message)
    userk, reason = get_user(message, text_)
    if not userk:
        await bun.edit("`Bruh, Please Reply To User / Give Me Username of ID To Ban!`")
        return
    try:
        user_ = await client.get_users(userk)
    except:
        await bun.edit(f"`404 : User Doesn't Exists In This Chat !`")
        return
    userz = user_.id
    if not reason:
        reason = "Not Specified!"
    if userz == me_m.id:
        await bun.edit("`🙄 Nice Idea, Lets Leave This Chat!`")
        return
    try:
        user_ = await client.get_users(userz)
    except:
        await bun.edit(f"`404 : User Doesn't Exists In This Chat !`")
        return
    try:
        await client.kick_chat_member(message.chat.id, int(user_.id))
    except BaseException as e:
        await bun.edit(f"`I Am Un-able To Ban That User` \n**Error :** `{e}`")
        return
    b = f"**#Banned** \n**User :** [{user_.first_name}](tg://user?id={user_.id}) \n**Chat :** `{message.chat.title}` \n**Reason :** `{reason}`"
    await bun.edit(b)
    log = LogIt(message)
    await log.log_msg(client, b)


@friday_on_cmd(
    ["unban", "unbun"],
    only_if_admin=True,
    group_only=True,
    cmd_help={
        "help": "UnBan Replied User or provide his ID!",
        "example": "{ch}unban (reply to user message OR Provide his id)",
    },
)
async def unban_world(client, message):
    unbun = await edit_or_reply(message, "`Trying To Un-Ban User!`")
    me_m = client.me
    me_ = await message.chat.get_member(int(me_m.id))
    if not me_.can_restrict_members:
        await unbun.edit("`Boss, You Don't Have Un-Ban Permission!`")
        return
    text_ = get_text(message)
    userm, reason = get_user(message, text_)
    if not userm:
        await unbun.edit(
            "`Bruh, Please Reply To User / Give Me Username of ID To UnBan!`"
        )
        return
    try:
        user_ = await client.get_users(userm)
    except:
        await unbun.edit(f"`404 : User Doesn't Exists In This Chat !`")
        return
    userz = user_.id
    if not reason:
        reason = "Not Specified!"
    if userz == me_m.id:
        await unbun.edit("`🙄 Nice Idea, Lets Un-Ban Myself!`")
        return
    try:
        await client.unban_chat_member(message.chat.id, int(user_.id))
    except BaseException as e:
        await unbun.edit(f"`I Un-Able To Un-Ban That User` \n**Error :** `{e}`")
    ub = f"**#UnBanned** \n**User :** [{user_.first_name}](tg://user?id={user_.id}) \n**Chat :** `{message.chat.title}` \n**Reason :** `{reason}`"
    await unbun.edit(ub)
    log = LogIt(message)
    await log.log_msg(client, ub)


@friday_on_cmd(
    ["promote", "prumote"],
    only_if_admin=True,
    group_only=True,
    cmd_help={
        "help": "Promote Replied user or provide his ID!",
        "example": "{ch}promote (reply to user message OR provide his ID)",
    },
)
async def ujwal_mote(client, message):
    pablo = await edit_or_reply(message, "`Trying To Promote User!`")
    me_m = client.me
    me_ = await message.chat.get_member(int(me_m.id))
    if not me_.can_promote_members:
        await pablo.edit("`Boss, You Don't Have Promote Permission!`")
        return
    asplit = get_text(message)
    userl, Res = get_user(message, asplit)
    if not userl:
        await pablo.edit(
            "`Bruh, Please Reply To User / Give Me Username of ID To Promote!`"
        )
        return
    try:
        user = await client.get_users(userl)
    except:
        await pablo.edit(f"`404 : User Doesn't Exists In This Chat !`")
        return
    userz = user.id
    if not Res:
        Res = "Admeme"
    if userz == me_m.id:
        await pablo.edit("`🙄 Nice Idea, Lets Self Promote!`")
        return
    try:
        await client.promote_chat_member(
            message.chat.id,
            user.id,
            can_change_info=me_.can_change_info,
            can_delete_messages=me_.can_delete_messages,
            can_restrict_members=me_.can_restrict_members,
            can_invite_users=me_.can_invite_users,
            can_pin_messages=me_.can_pin_messages,
            can_promote_members=me_.can_promote_members,
        )
    except BaseException as e:
        await pablo.edit(f"`I Am Un-Able To Promote This User` \n**Error :** `{e}`")
        return
    p = f"**#Promote** \n**User :** [{user.first_name}](tg://user?id={user.id}) \n**Chat :** `{message.chat.title}` \n**Title :** `{Res}`"
    await pablo.edit(p)
    log = LogIt(message)
    await log.log_msg(client, p)
    try:
        if Res:
            await client.set_administrator_title(message.chat.id, user.id, Res)
    except:
        pass


@friday_on_cmd(
    ["demote", "demute"],
    only_if_admin=True,
    group_only=True,
    cmd_help={
        "help": "Demote Replied user or provide his ID!",
        "example": "{ch}demote (reply to user message OR provide his ID)",
    },
)
async def ujwal_demote(client, message):
    pablo = await edit_or_reply(message, "`Trying To Demote User!`")
    me_m = client.me
    await message.chat.get_member(int(me_m.id))
    asplit = get_text(message)
    usero = get_user(message, asplit)[0]
    if not usero:
        await pablo.edit(
            "`Bruh, Please Reply To User / Give Me Username of ID To Demote!`"
        )
        return
    try:
        user = await client.get_users(usero)
    except:
        await pablo.edit(f"`404 : User Doesn't Exists In This Chat !`")
        return
    userz = user.id
    if userz == me_m.id:
        await pablo.edit("`🙄 Nice Idea, Lets Self Demote!`")
        return
    try:
        await client.promote_chat_member(
            message.chat.id,
            user.id,
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
    except BaseException as e:
        await pablo.edit(f"`I Wasn't Able To Demote That User` \n**Error :** `{e}`")
        return
    d = f"**#Demote** \n**User :** [{user.first_name}](tg://user?id={user.id}) \n**Chat :** `{message.chat.title}`"
    await pablo.edit(d)
    log = LogIt(message)
    await log.log_msg(client, d)


@friday_on_cmd(
    ["mute"],
    only_if_admin=True,
    group_only=True,
    cmd_help={
        "help": "Mute Replied user or provide his ID!",
        "example": "{ch}mute (reply to user message OR provide his ID)",
    },
)
async def ujwal_mute(client, message):
    pablo = await edit_or_reply(message, "`Trying To Mute User!`")
    me_m = client.me
    me_ = await message.chat.get_member(int(me_m.id))
    if not me_.can_restrict_members:
        await pablo.edit("`Boss, You Don't Have Mute Permission!`")
        return
    asplit = get_text(message)
    userf = get_user(message, asplit)[0]
    if not userf:
        await pablo.edit(
            "`Bruh, Please Reply To User / Give Me Username of ID To Mute!`"
        )
        return
    try:
        user = await client.get_users(userf)
    except:
        await pablo.edit(f"`404 : User Doesn't Exists In This Chat !`")
        return
    userz = user.id
    if userz == me_m.id:
        await pablo.edit("`🙄 Nice Idea, Lets Self Mute!`")
        return
    try:
        await client.restrict_chat_member(
            message.chat.id, user.id, ChatPermissions(can_send_messages=False)
        )
    except BaseException as e:
        await pablo.edit(f"`I Am UnAble To Mute That User` \n**Error :** `{e}`")
        return
    m = f"**#Muted** \n**User :** [{user.first_name}](tg://user?id={user.id}) \n**Chat :** `{message.chat.title}`"
    await pablo.edit(m)
    log = LogIt(message)
    await log.log_msg(client, m)


@friday_on_cmd(
    ["unmute"],
    only_if_admin=True,
    group_only=True,
    cmd_help={
        "help": "Unmute Replied user or provide his ID!",
        "example": "{ch}Unmute (reply to user message OR provide his ID)",
    },
)
async def ujwal_unmute(client, message):
    pablo = await edit_or_reply(message, "`Trying To Un-Mute User!`")
    me_m = client.me
    me_ = await message.chat.get_member(int(me_m.id))
    if not me_.can_restrict_members:
        await pablo.edit("`Boss, You Don't Have Un-Mute Permission!`")
        return
    asplit = get_text(message)
    userf = get_user(message, asplit)[0]
    if not userf:
        await pablo.edit(
            "`Bruh, Please Reply To User / Give Me Username of ID To Unmute!`"
        )
        return
    try:
        user = await client.get_users(userf)
    except:
        await pablo.edit(f"`404 : User Doesn't Exists In This Chat !`")
        return
    userz = user.id
    if userz == me_m.id:
        await pablo.edit("`🙄 Nice Idea, Lets Self Un-Mute!`")
        return
    try:
        await client.restrict_chat_member(
            message.chat.id, user.id, ChatPermissions(can_send_messages=True)
        )
    except BaseException as e:
        await pablo.edit(f"`I Am UnAble To UN-Mute That User` \n**Error :** `{e}`")
        return
    um = f"**#Un_Muted** \n**User :** [{user.first_name}](tg://user?id={user.id}) \n**Chat :** `{message.chat.title}`"
    await pablo.edit(um)
    log = LogIt(message)
    await log.log_msg(client, um)


@friday_on_cmd(
    ["chatinfo", "grpinfo"],
    group_only=True,
    cmd_help={"help": "Get Info Of The Chat!", "example": "{ch}chatinfo"},
)
async def owo_chat_info(client, message):
    s = await edit_or_reply(message, "`Trying To Get ChatInfo!`")
    ujwal = await client.get_chat(message.chat.id)
    peer = await client.resolve_peer(message.chat.id)
    online_ = await client.send(pyrogram.raw.functions.messages.GetOnlines(peer=peer))
    msg = "**Chat Info** \n\n"
    msg += f"**Chat-ID :** __{ujwal.id}__ \n"
    msg += f"**Verified :** __{ujwal.is_verified}__ \n"
    msg += f"**Is Scam :** __{ujwal.is_scam}__ \n"
    msg += f"**Chat Title :** __{ujwal.title}__ \n"
    msg += f"**Users Online :** __{online_.onlines}__ \n"
    if ujwal.photo:
        msg += f"**Chat DC :** __{ujwal.dc_id}__ \n"
    if ujwal.username:
        msg += f"**Chat Username :** __{ujwal.username}__ \n"
    if ujwal.description:
        msg += f"**Chat Description :** __{ujwal.description}__ \n"
    msg += f"**Chat Members Count :** __{ujwal.members_count}__ \n"
    if ujwal.photo:
        kek = await client.download_media(ujwal.photo.big_file_id)
        await client.send_photo(message.chat.id, photo=kek, caption=msg)
        await s.delete()
    else:
        await s.edit(msg)


@friday_on_cmd(
    ["purge"],
    only_if_admin=True,
    cmd_help={
        "help": "Purge All Messages Till Replied Message!",
        "example": "{ch}purge (reply to message)",
    },
)
async def purge(client, message):
    start_time = time.time()
    message_ids = []
    purge_len = 0
    event = await edit_or_reply(message, "`Starting To Purge Messages!`")
    me_m = client.me
    if message.chat.type in ["supergroup", "channel"]:
        me_ = await message.chat.get_member(int(me_m.id))
        if not me_.can_delete_messages:
            await event.edit("`I Need Delete Permission To Do This!`")
            return
    if not message.reply_to_message:
        await event.edit("`Reply To Message To Purge!`")
        return
    async for msg in client.iter_history(
        chat_id=message.chat.id,
        offset_id=message.reply_to_message.message_id,
        reverse=True,
    ):
        if msg.message_id != message.message_id:
            purge_len += 1
            message_ids.append(msg.message_id)
            if len(message_ids) >= 100:
                await client.delete_messages(
                    chat_id=message.chat.id, message_ids=message_ids, revoke=True
                )
                message_ids.clear()
    if message_ids:
        await client.delete_messages(
            chat_id=message.chat.id, message_ids=message_ids, revoke=True
        )
    end_time = time.time()
    u_time = round(end_time - start_time)
    await event.edit(
        f"**>> Flash Purge Done!** \n**>> Total Message Purged :** `{purge_len}` \n**>> Time Taken :** `{u_time}`",
    )
    await asyncio.sleep(3)
    await event.delete()


@friday_on_cmd(
    ["del"],
    cmd_help={
        "help": "Delete Replied Message!",
        "example": "{ch}del (reply to message)",
    },
)
async def delmsgs(client, message):
    if not message.reply_to_message:
        await message.delete()
        return
    await client.delete_messages(
        chat_id=message.chat.id,
        message_ids=[message.reply_to_message.message_id],
        revoke=True,
    )
    await message.delete()


@friday_on_cmd(
    ["setgrppic", "gpic"],
    cmd_help={
        "help": "Set Custom Group Pic, For Lazy Peoples!",
        "example": "{ch}setgrppic (reply to image)",
    },
)
async def magic_grps(client, message):
    msg_ = await edit_or_reply(message, "`Please Wait!`")
    if not message.reply_to_message:
        await msg_.edit("`Reply To Image Please?`")
        return
    me_ = await message.chat.get_member(int(client.me.id))
    if not me_.can_change_info:
        await msg_.edit("`I Need Delete Permission To Do This!`")
        return
    cool = await convert_to_image(message, client)
    if not cool:
        await msg_.edit("`Reply to a valid media first.`")
        return
    if not os.path.exists(cool):
        await msg_.edit("`Invalid Media!`")
        return
    try:
        await client.set_chat_photo(message.chat.id, photo=cool)
    except BaseException as e:
        await msg_.edit(f"`Unable To Set Group Photo! TraceBack : {e}")
        return
    await msg_.edit("`Done! Sucessfully Set This Pic As Chat Pic Of This Chat!")

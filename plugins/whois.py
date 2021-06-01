# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import os

from database.gbandb import gban_info, gban_list, gban_user, ungban_user
from database.gmutedb import gmute, is_gmuted, ungmute
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import (
    edit_or_reply,
    edit_or_send_as_file,
    get_text,
    get_user,
    is_admin_or_owner,
)
from plugins import devs_id


@friday_on_cmd(
    ["get_id"],
    cmd_help={"help": "Get Current Chat ID!", "example": "{ch}get_id"},
)
async def wew_id(client, message):
    t_xt = f"Chat ID : `{message.chat.id}`"
    pablo = await edit_or_reply(message, t_xt)


@friday_on_cmd(
    ["info", "whois"],
    cmd_help={"help": "Get Info About A User", "example": "{ch}info @chsaiujwal"},
)
async def whois(client, message):
    user_photo = None
    msg_ = await edit_or_reply(message, "`Hang On!`")
    text_ = get_text(message)
    userk = get_user(message, text_)[0]
    if not userk:
        await msg_.edit("`Mention A User Boss!`")
        return
    try:
        user_ = await client.get_users(userk)
    except:
        await msg_.edit(f"`404 : Unable To Get To This User!`")
        return
    if user_.photo:
        user_photo = await client.download_media(user_.photo.big_file_id)
    user_info = f"<b><u>User Info Of</b></u> {user_.mention} \n\n"
    user_info += f"✱ <b>User ID :</b> <code>{user_.id}</code> \n"
    user_info += f"✱ <b>FirstName :</b> <code>{user_.first_name}</code> \n"
    user_info += (
        f"✱ <b>LastName :</b> <code>{user_.last_name}</code> \n"
        if user_.last_name
        else f"✱ <b>LastName :</b> <code>Not Set</code> \n"
    )
    user_info += (
        f"✱ <b>DC :</b> <code>{user_.dc_id}</code> \n"
        if user_.dc_id
        else f"✱ <b>DC :</b> <code>No PFP</code> \n"
    )
    user_info += (
        f"✱ <b>Status :</b> <code>{user_.status}</code> \n"
        if user_.status
        else f"✱ <b>Status :</b> <code>Bot Can't Have Last Seen</code> \n"
    )
    user_info += (
        f"✱ <b>Username :</b> <code>{user_.username}</code> \n"
        if user_.username
        else f"✱ <b>Username :</b> <code>User Doesn't Have A UserName</code> \n"
    )
    user_info += f"✱ <b>Is Scam :</b> <code>{user_.is_scam}</code> \n"
    user_info += f"✱ <b>Is Bot :</b> <code>{user_.is_bot}</code> \n"
    user_info += f"✱ <b>Is Verified :</b> <code>{user_.is_verified}</code> \n"
    user_info += f"✱ <b>Is Contact :</b> <code>{user_.is_contact}</code> \n"
    common = await client.get_common_chats(user_.id)
    user_info += f"✱ <b>Total Groups In Common :</b> <code>{len(common)}</code> \n"
    if user_.id in devs_id:
        user_info += f"\n <code>Wow! This User is One Of My Developer</code> \n"
    if await gban_info(user_.id):
        user_info += f"\n This User Is Gbanned For Reason : <code>{await gban_info(user_.id)}</code> \n"
    if await is_gmuted(user_.id):
        user_info += f"\n This User Is Gmutted! \n"
    if user_photo:
        await msg_.delete()
        if message.reply_to_message:
            await client.send_photo(
                message.chat.id,
                user_photo,
                caption=user_info,
                reply_to_message_id=message.reply_to_message.message_id,
            )
        else:
            await client.send_photo(
                message.chat.id, user_photo, caption=user_info, parse_mode="html"
            )
        os.remove(user_photo)
    else:
        await msg_.edit(user_info)

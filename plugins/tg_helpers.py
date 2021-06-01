# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import (
    edit_or_reply,
    edit_or_send_as_file,
    get_text,
    get_user,
)


@friday_on_cmd(
    ["updatefirstname", "firstname"],
    cmd_help={
        "help": "Change Your Account First Name!",
        "example": "{ch}firstname (new firstname)",
    },
)
async def bleck_name(client, message):
    owo = await edit_or_reply(message, "`Updating FirstName!`")
    new_firstname = get_text(message)
    if not new_firstname:
        await owo.edit("`Give A Input :/`")
        return
    if len(new_firstname) > 64:
        await owo.edit("`Bruh, TG Will Not Allow That :(`")
        return
    try:
        await client.update_profile(first_name=new_firstname)
    except BaseException as e:
        await owo.edit(
            f"`[Failed] - Unable To Update Firstname` \n**TraceBack :** `{e}`"
        )
        return
    await owo.edit(f"`Firstname Sucessfully Changed To {new_firstname} !`")


@friday_on_cmd(
    ["updatebio", "bio"],
    cmd_help={"help": "Change Your Account Bio!", "example": "{ch}bio (new bio)"},
)
async def bleck_bio(client, message):
    owo = await edit_or_reply(message, "`Updating Bio!`")
    new_bio = get_text(message)
    if not new_bio:
        await owo.edit("`Give A Input :/`")
        return
    if len(new_bio) > 70:
        await owo.edit("`Bruh, TG Will Not Allow That :(`")
        return
    try:
        await client.update_profile(bio=new_bio)
    except BaseException as e:
        await owo.edit(f"`[Failed] - Unable To Update Bio` \n**TraceBack :** `{e}`")
        return
    await owo.edit(f"`Bio Sucessfully Changed To {new_bio} !`")


@friday_on_cmd(
    ["updateusername", "username"],
    cmd_help={
        "help": "Change Your Account UserName!",
        "example": "{ch}username (new username)",
    },
)
async def bleck_username(client, message):
    owo = await edit_or_reply(message, "`Updating Username!`")
    new_username = get_text(message)
    if not new_username:
        await owo.edit("`Give A Input :/`")
        return
    try:
        await client.update_username(new_username)
    except BaseException as e:
        await owo.edit(
            f"`[Failed] - Unable To Update Username` \n**TraceBack :** `{e}`"
        )
        return
    await owo.edit(f"`Username Sucessfully Changed To {new_username} !`")


@friday_on_cmd(
    ["updatelastname", "lastname"],
    cmd_help={
        "help": "Change Your Account Last Name!",
        "example": "{ch}lastname (new lastname)",
    },
)
async def bleck_name(client, message):
    owo = await edit_or_reply(message, "`Updating LastName!`")
    new_lastname = get_text(message)
    if not new_lastname:
        await owo.edit("`Give A Input :/`")
        return
    if len(new_lastname) > 64:
        await owo.edit("`Bruh, TG Will Not Allow That :(`")
        return
    try:
        await client.update_profile(last_name=new_lastname)
    except BaseException as e:
        await owo.edit(
            f"`[Failed] - Unable To Update Lastname` \n**TraceBack :** `{e}`"
        )
        return
    await owo.edit(f"`Lastname Sucessfully Changed To {new_lastname} !`")

@friday_on_cmd(
    ["join"],
    cmd_help={
        "help": "Join A Chat Easily.",
        "example": "{ch}join (chat link or username)",
    },
)
async def join_(client, message):
    owo = await edit_or_reply(message, "`Joining Chat...`")
    input_ = get_text(message)
    if not input_:
        await owo.edit("`Give A Input :/`")
        return
    try:
        await client.join_chat(input_)
    except BaseException as e:
        await owo.edit(
            f"`[Failed] - To Join Chat` \n**TraceBack :** `{e}`"
        )
        return
    await owo.edit(f"`Sucessfully, Joined This Chat.`")

@friday_on_cmd(
    ["leave"],
    group_only=True,
    cmd_help={
        "help": "Leave Chat Easily.",
        "example": "{ch}leave",
    },
)
async def leave_(client, message):
    await edit_or_reply(message, "`GOODBYECRUELGROUP - *leaves*`")
    await client.leave_chat(message.chat.id)


@friday_on_cmd(
    ["updateppic", "ppic"],
    cmd_help={
        "help": "Change Your Profile Picture!",
        "example": "{ch}ppic (Reply To New Profile Picture)",
    },
)
async def bleck_pic(client, message):
    owo = await edit_or_reply(message, "`Updating PPic!`")
    if not message.reply_to_message:
        await owo.edit("`Reply To Image / Video To Set As PPic`")
        return
    if not (
        message.reply_to_message.video
        or message.reply_to_message.animation
        or message.reply_to_message.photo
    ):
        await owo.edit("`Reply To Image / Video To Set As PPic`")
        return
    is_video = False
    if message.reply_to_message.video or message.reply_to_message.animation:
        is_video = True
    ppics = await message.reply_to_message.download()
    try:
        if is_video:
            await client.set_profile_photo(video=ppics)
        else:
            await client.set_profile_photo(photo=ppics)
    except BaseException as e:
        await owo.edit(f"`[Failed] - Unable To Update PPic` \n**TraceBack :** `{e}`")
        return
    await owo.edit("`Sucessfully, Updated Profile Pic!`")


@friday_on_cmd(
    ["poll"],
    group_only=True,
    cmd_help={
        "help": "Create A Poll!",
        "example": "{ch}poll Your Message | option 1, option 2, option 3",
    },
)
async def create_poll(client, message):
    msg = await edit_or_reply(message, "`Creating Poll!`")
    poll_ = get_text(message)
    if not poll_:
        await msg.edit("`Give Me Question & Options! See Help For More`")
        return
    if not "|" in poll_:
        await msg.edit("`Give Me Options :/`")
        return
    poll_q, poll_options = poll_.split("|")
    if not "," in poll_options:
        await msg.edit("`A Poll Needs 1+ Options!`")
        return
    option_s = poll_options.split(",")
    await client.send_poll(message.chat.id, question=poll_q, options=option_s)
    await msg.delete()


@friday_on_cmd(
    ["dump"],
    cmd_help={
        "help": "Get Pyrogram Message Dumbs!",
        "example": "{ch}dump",
    },
)
async def dumb_er(client, message):
    ow = await edit_or_reply(message, "`Dumping...`")
    if message.reply_to_message:
        m_sg = message.reply_to_message
    else:
        m_sg = message
    owo = f"{m_sg}"
    await edit_or_send_as_file(owo, ow, client, "Json-Dump", "Dump", "md")


@friday_on_cmd(
    ["purgeme"],
    cmd_help={
        "help": "Purge Your Own Message Until Given Limit!",
        "example": "{ch}purgeme 10",
    },
)
async def pur_ge_me(client, message):
    nice_p = await edit_or_reply(message, "`Processing...`")
    msg_ids = []
    to_purge = get_text(message)
    if not to_purge:
        nice_p.edit("`Give No Of Message To Purge :/`")
        return
    if not to_purge.isdigit():
        nice_p.edit("`Give No Of Message To Purge :/`")
        return
    async for msg in client.search_messages(
        message.chat.id, query="", limit=int(to_purge), from_user="me"
    ):
        if message.message_id != msg.message_id:
            msg_ids.append(msg.message_id)
            if len(msg_ids) == 100:
                await client.delete_messages(
                    chat_id=message.chat.id, message_ids=msg_ids, revoke=True
                )
                msg_ids.clear()
    if msg_ids:
        await client.delete_messages(
            chat_id=message.chat.id, message_ids=msg_ids, revoke=True
        )
    await nice_p.edit(f"`Purged {to_purge} Messages!`")


@friday_on_cmd(
    ["invite", "add"],
    cmd_help={
        "help": "Add Users To Channel / Groups!",
        "example": "{ch}invite @Midhun_xD @chsaiujwal @meisnub",
    },
)
async def add_user_s_to_group(client, message):
    mg = await edit_or_reply(message, "`Adding Users!`")
    user_s_to_add = get_text(message)
    if not user_s_to_add:
        await mg.edit("`Give Me Users To Add! Check Help Menu For More Info!`")
        return
    user_list = user_s_to_add.split(" ")
    try:
        await client.add_chat_members(message.chat.id, user_list, forward_limit=100)
    except BaseException as e:
        await mg.edit(f"`Unable To Add Users! \nTraceBack : {e}`")
        return
    await mg.edit(f"`Sucessfully Added {len(user_list)} To This Group / Channel!`")


@friday_on_cmd(
    ["a2c"],
    cmd_help={
        "help": "Add Users To Your Contacts!",
        "example": "{ch}a2c @Meisnub",
    },
)
async def add_user_s_to_contact(client, message):
    msg_ = await edit_or_reply(message, "`Please Wait!`")
    text_ = get_text(message)
    userk = get_user(message, text_)[0]
    try:
        user_ = await client.get_users(userk)
    except:
        await msg_.edit(f"`404 : Unable To Get To This User!`")
        return
    custom_name = get_text(message) or user_.first_name
    await client.add_contact(user_.id, custom_name)
    await msg_.edit(f"`Added {user_.first_name} To Contacts!`")

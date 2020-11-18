from Elizabeth import client
from Elizabeth.events import register
from telethon import types
from telethon.tl import functions


async def can_approve_users(message):
    result = await client(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.add_admins
    )


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):

        ui = await client.get_peer_id(user)
        ps = (
            await client(functions.messages.GetFullChatRequest(chat.chat_id))
        ).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return None


# ------ THANKS TO LONAMI ------#


@register(pattern="^/approve(?: |$)(.*)")
async def approve(event):
    if event.fwd_from:
        return
    chat_id = event.chat.id
    sender = event.sender_id
    reply_msg = await event.get_reply_message()
    approved_userss = approved_users.find({})

    if event.is_group:
        if not await can_approve_users(message=event):
            return
    else:
        return

    ik = event.pattern_match.group(1)
    if ik.isdigit():
        input = int(ik)
    else:
        input = ik.replace("@", "")

    if not input:
        iid = (
            reply_msg.sender_id
            if event.reply_to_msg_id
            else await event.reply("Reply To Someone's Message Or Provide Some Input")
        )
    elif input:
        cunt = input
        dent = await client.get_entity(cunt)
        iid = dent.id
    elif input and event.reply_to_msg_id:
        cunt = input
        dent = await client.get_entity(cunt)
        iid = dent.id

    if await is_register_admin(event.input_chat, iid):
        await event.reply("Why will I approve an admin ?")
        return

    if iid == event.sender_id or iid == event.sender_id:
        await event.reply("Why are you trying to approve yourself ?")
        print("6")
        return

    if event.sender_id == 1246850012 or iid == 1246850012:
        await event.reply("I am not gonna approve myself")
        print("7")
        return

    chats = approved_users.find({})
    for c in chats:
        if event.chat_id == c["id"] and iid == c["user"]:
            await event.reply("This User is Already Approved")
            return

    approved_users.insert_one({"id": event.chat_id, "user": iid})
    await event.reply("Successfully Approved User")


@register(pattern="^/disapprove(?: |$)(.*)")
async def disapprove(event):
    if event.fwd_from:
        return
    chat_id = event.chat.id
    sender = event.sender_id
    reply_msg = await event.get_reply_message()
    approved_userss = approved_users.find({})

    if event.is_group:
        if not await can_approve_users(message=event):
            return
    else:
        return

    ik = event.pattern_match.group(1)
    if ik.isdigit():
        input = int(ik)
    else:
        input = ik.replace("@", "")

    if not input:
        iid = (
            reply_msg.sender_id
            if event.reply_to_msg_id
            else await event.reply("Reply To Someone's Message Or Provide Some Input")
        )
    elif input:
        cunt = input
        dent = await client.get_entity(cunt)
        iid = dent.id
    elif input and event.reply_to_msg_id:
        cunt = input
        dent = await client.get_entity(cunt)
        iid = dent.id

    if await is_register_admin(event.input_chat, iid):
        await event.reply("Why will I disapprove an admin ?")
        return

    if iid == event.sender_id or iid == event.sender_id:
        await event.reply("Why are you trying to disapprove yourself ?")
        print("6")
        return

    if event.sender_id == 1246850012 or iid == 1246850012:
        await event.reply("I am not gonna disapprove myself")
        print("7")
        return

    chats = approved_users.find({})
    for c in chats:
        if event.chat_id == c["id"] and iid == c["user"]:
            approved_users.delete_one({"id": event.chat_id, "user": iid})
            await event.reply("Successfully Disapproved User")
            return
    await event.reply("This User isn't approved yet")


@register(pattern="^/checkstatus(?: |$)(.*)")
async def checkst(event):
    if event.fwd_from:
        return
    chat_id = event.chat.id
    sender = event.sender_id
    reply_msg = await event.get_reply_message()
    approved_userss = approved_users.find({})

    if event.is_group:
        if not await can_approve_users(message=event):
            return
    else:
        return

    ik = event.pattern_match.group(1)
    if ik.isdigit():
        input = int(ik)
    else:
        input = ik.replace("@", "")

    if not input:
        iid = (
            reply_msg.sender_id
            if event.reply_to_msg_id
            else await event.reply("Reply To Someone's Message Or Provide Some Input")
        )
    elif input:
        cunt = input
        dent = await client.get_entity(cunt)
        iid = dent.id
    elif input and client.reply_to_msg_id:
        cunt = input
        dent = await client.get_entity(cunt)
        iid = dent.id

    if await is_register_admin(event.input_chat, iid):
        await event.reply("Why will check status of an admin ?")
        return

    if event.sender_id == 1246850012 or iid == 1246850012:
        await event.reply("I am not gonna check my status")
        print("7")
        return

    chats = approved_users.find({})
    for c in chats:
        if event.chat_id == c["id"] and iid == c["user"]:
            await event.reply("This User is Approved")
            return
    await event.reply("This user isn't Approved")


@register(pattern="^/listapproved$")
async def apprlst(event):
    print("😁")
    if event.fwd_from:
        return
    chat_id = event.chat.id
    sender = event.sender_id
    reply_msg = await event.get_reply_message()

    if event.is_group:
        if not await can_approve_users(message=event):
            return
    else:
        return

    autos = approved_users.find({})
    pp = ""
    for i in autos:
        if event.chat_id == i["id"]:
            try:
                h = await client.get_entity(i["user"])
                getmyass = ""
                if not h.username:
                    getmyass += f"- [{h.first_name}](tg://user?id={h.id})\n"
                else:
                    getmyass += "- @" + h.username + "\n"
                pp += str(getmyass)
            except ValueError:
                pass
    try:
        await event.reply(pp)
    except Exception:
        await event.reply("No one is approved in this chat.")


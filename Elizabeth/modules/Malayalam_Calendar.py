import asyncio
from datetime import datetime
import requests
import json
from Elizabeth.events import register
from Elizabeth import client
from telethon import types
from telethon.tl import functions
from telethon import events

async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (await client(functions.channels.GetParticipantRequest(chat, user))).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator)
        )
    elif isinstance(chat, types.InputPeerChat):

        ui = await client.get_peer_id(user)
        ps = (await client(functions.messages.GetFullChatRequest(chat.chat_id))) \
            .full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator)
        )
    else:
        return None

@register(pattern="^/calendar")
async def _(event):
    if event.fwd_from:
        return

    if event.is_group:
     if not (await is_register_admin(event.input_chat, event.message.sender_id)):
       await event.reply("😜 Hai.. You are not admin..🤭 You can't use this command.. But you can use in my pm🙈")
       return

    start = datetime.now()
    input_str = event.pattern_match.group(1)
    input_sgra = input_str.split("-")
    if len(input_sgra) == 3:
        yyyy = input_sgra[0]
        mm = input_sgra[1]
        dd = input_sgra[2]
        required_url = "https://calendar.kollavarsham.org/api/years/{}/months/{}/days/{}?lang={}".format(yyyy, mm, dd, "en")
        headers = {"Accept": "application/json"}
        response_content = requests.get(required_url, headers=headers).json()
        a = ""
        if "error" not in response_content:
            current_date_detail_arraays = response_content["months"][0]["days"][0]
            a = json.dumps(current_date_detail_arraays, sort_keys=True, indent=4)
        else:
            a = response_content["error"]
        await event.reply(str(a))
    else:
        await event.reply("SYNTAX: .calendar YYYY-MM-DD")
    end = datetime.now()
    ms = (end - start).seconds

import asyncio
import glob
import io
import os
import subprocess
import time

import spotdl
from telethon import events
from telethon import types
from telethon.errors import MessageEmptyError
from telethon.errors import MessageNotModifiedError
from telethon.errors import MessageTooLongError
from telethon.tl import functions

from ubotindo import LOGGER
from ubotindo import client
from ubotindo.events import register


@register(pattern="^/song (.*)")
async def _(event):
    if event.fwd_from:
        return
    if event.is_group:
        if not (await is_register_admin(event.input_chat,
                                        event.message.sender_id)):
            return
    cmd = event.pattern_match.group(1)
    cmnd = f"{cmd}"
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    subprocess.run(["spotdl", "-s", cmnd, "-q", "best"])
    subprocess.run(
        'for f in *.opus; do      mv -- "$f" "${f%.opus}.mp3"; done',
        shell=True)
    l = glob.glob("*.mp3")
    loa = l[0]
    await event.reply("sending the song")
    await event.client.send_file(
        event.chat_id,
        loa,
        force_document=False,
        allow_cache=False,
        supports_streaming=True,
        caption=cmd,
        reply_to=reply_to_id,
    )
    subprocess.run("rm -rf *.mp3", shell=True)

from Elizabeth import client
import glob
import os
import spotdl
import subprocess
from telethon import types
from telethon.tl import functions
from Elizabeth.events import register



@register(pattern="^/song (.*)")
async def _(event):
    if event.fwd_from:
        return

    cmd = event.pattern_match.group(1)
    cmnd = f"{cmd}"
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    try:
        subprocess.run(["spotdl", "-s", cmnd, "-q", "best"])
        subprocess.run(
            'for f in *.opus; do      mv -- "$f" "${f%.mp3}.mp3"; done', shell=True
        )
        l = glob.glob("*.mp3")
        loa = l[0]
        await event.reply("sending the song")
        await client.send_file(
            event.chat_id,
            loa,
            force_document=False,
            allow_cache=False,
            supports_streaming=True,
            caption=cmd,
            reply_to=reply_to_id,
        )
        os.system("rm -rf *.mp3")
    except Exception:
        await event.reply("I am getting too many requests !\nPlease try again later.")


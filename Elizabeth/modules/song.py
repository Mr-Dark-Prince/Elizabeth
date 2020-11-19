from Elizabeth import client
import glob
import os
import spotdl
import subprocess
from telethon import types
from telethon.tl import functions
from Elizabeth.events import register


import instantmusic,subprocess
os.system("rm -rf *.mp3")
    

@register(pattern="^/song (.*)")
async def _(event):
    if event.fwd_from:
        return
    cmd = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    await event.reply("ok finding the song")
    os.system("instantmusic -q -s "+cmd)
    bro = 'for f in *.webm; do      mv -- "$f" "${f%.webm}.mp3"; done'
    os.system(bro)
    l = glob.glob("*.mp3")
    loa = l[5]
    await event.reply("sending the song")
    await event.client.send_file(
                event.chat_id,
                loa,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id
            )
    os.system("rm -rf *.mp3")
    subprocess.check_output("rm -rf *.mp3",shell=True)



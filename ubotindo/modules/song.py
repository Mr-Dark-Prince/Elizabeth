from telegram import ParseMode, Update, Bot
from telegram.ext import run_async
from ubotindo.modules.disable import DisableAbleCommandHandler
from ubotindo import dispatcher
from ubotindo.modules.dll import dl, db
from ubotindo.events import register
import os

@register(pattern="^/song (.*)")
async def _(event):
    if event.fwd_from:
        return
    message = update.effective_message
    text = message.text[len('/song '):]
    cmd = event.pattern_match.group(1)
    dl(cmd)
    sng = db.get('title') + '.mp3'
    title = db.get('title')
    reply_text = f"Finding **{title}**"
    message.reply_text(reply_text)
    message.reply_audio(audio=sng)
    os.remove(sng)
    
__help__ = """
 - /song songname : download any song"""

__mod_name__ = "Songs"
song_handle = DisableAbleCommandHandler("song", song)
dispatcher.add_handler(song_handle)

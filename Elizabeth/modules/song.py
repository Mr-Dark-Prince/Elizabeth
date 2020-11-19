from telegram import ParseMode, Update, Bot
from telegram.ext import run_async
from Elizabeth.modules.disable import DisableAbleCommandHandler
from Elizabeth import dispatcher
from Elizabeth.modules.Elizabeth import dl, db
import os

@run_async
def song(bot: Bot, update: Update):
    message = update.effective_message
    text = message.text[len('/song '):]
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

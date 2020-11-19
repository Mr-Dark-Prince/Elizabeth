from telegram import ParseMode, Update, Bot
from telegram.ext import run_async
from Elizabeth.events import register
from Elizabeth import client
from Elizabeth.modules.disable import DisableAbleCommandHandler
from Elizabeth import dispatcher
from Elizabeth.modules.Elizabeth import dl, db
import os

@register(pattern="^/song (.*)")
async def _(event):
    if event.fwd_from:
        return

    message = update.effective_message
    text = message.text[len('/song '):]
    dl(cmd)
    cmd = event.pattern_match.group(1)
    sng = db.get('title') + '.mp3'
    title = db.get('title')
    reply_text = f"Finding **{title}**"
    message.reply_text(reply_text)
    message.reply_audio(audio=sng)
    os.remove(sng)

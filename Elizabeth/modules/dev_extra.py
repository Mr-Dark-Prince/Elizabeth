import os
import subprocess
import sys
from time import sleep

from Elizabeth import dispatcher
from Elizabeth import DEV_USERS, dispatcher
from Elizabeth.modules.helper_funcs.filters import CustomFilters

from telegram import TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler, run_async


@run_async
def leave(update, context):
    bot = context.bot
    args = context.args
    if args:
        chat_id = str(args[0])
        try:
            bot.leave_chat(int(chat_id))
            update.effective_message.reply_text("Beep boop, I left that soup!.")
        except TelegramError:
            update.effective_message.reply_text(
                "Beep boop, I could not leave that group(dunno why tho).")
    else:
        update.effective_message.reply_text("Send a valid chat ID")


LEAVE_HANDLER = CommandHandler("leave", leave)

dispatcher.add_handler(LEAVE_HANDLER)

__mod_name__ = "devss"




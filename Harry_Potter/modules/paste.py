import codecs
import os

import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from Harry_Potter import dispatcher
from Harry_Potter.modules.disable import DisableAbleCommandHandler


def paste(update, context):
    msg = update.effective_message

    if msg.reply_to_message.document:
        file = context.bot.get_file(msg.reply_to_message.document)
        file.download("file.txt")
        text = codecs.open("file.txt", "r+", encoding="utf-8")
        paste_text = text.read()
    else:
        paste_text = msg.reply_to_message.text

    try:
        link = (
            requests.post(
                "https://nekobin.com/api/documents",
                json={"content": paste_text},
            )
            .json()
            .get("result")
            .get("key")
        )
        text = "**Pasted to Nekobin!!!**"
        buttons = [
            [
                InlineKeyboardButton(
                    text="View Link", url=f"https://nekobin.com/{link}"
                ),
                InlineKeyboardButton(
                    text="View Raw",
                    url=f"https://nekobin.com/raw/{link}",
                ),
            ]
        ]
        msg.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        os.remove("file.txt")
    except Exception:
        msg.reply_text("What am I supposed to do with this?")
        return


PASTE_HANDLER = DisableAbleCommandHandler("paste", paste)

dispatcher.add_handler(PASTE_HANDLER)

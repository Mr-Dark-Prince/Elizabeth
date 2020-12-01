from mtranslate import translate
from Elizabeth import client
import json
import requests

from Elizabeth.events import register
from telethon import *
from telethon.tl import functions
import os
import urllib.request
from typing import List
from typing import Optional

from telethon.tl import types
from telethon.tl.types import *


@register(pattern="^/tr (.*)")
async def _(event):

    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str
    
    try:
        translated = translate(text,lan,"auto")
        await event.reply(translated)
    except Exception as exc:
        print(exc)
        await event.reply("**Server Error ⚠️**\nTry Again.")


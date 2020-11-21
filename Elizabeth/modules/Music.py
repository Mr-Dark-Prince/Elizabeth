import asyncio
import glob
import os
import subprocess
import time
from asyncio.exceptions import TimeoutError

import requests
from bs4 import BeautifulSoup
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pylast import User
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import DocumentAttributeVideo

from Elizabeth.events import register
from Elizabeth import client


def getmusic(get, DEFAULT_AUDIO_QUALITY):
    search = get

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    }

    html = requests.get(
        "https://www.youtube.com/results?search_query=" +
        search,
        headers=headers).text
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all("a"):
        if "/watch?v=" in link.get("href"):
            # May change when Youtube Website may get updated in the future.
            video_link = link.get("href")
            break

    video_link = "http://www.youtube.com/" + video_link
    command = (
        "youtube-dl --write-thumbnail --extract-audio --audio-format mp3 --audio-quality " +
        DEFAULT_AUDIO_QUALITY +
        " " +
        video_link)
    os.system(command)

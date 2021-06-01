# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from functools import wraps
import aiohttp
import asyncio
import os
import time
import requests
import wget
from youtube_dl import YoutubeDL
import aiofiles
from main_startup.helper_func.basic_helpers import get_all_pros, is_admin_or_owner


def _check_admin(func):
    @wraps(func)
    async def magic_admin(client, message):
        is_a_o = await is_admin_or_owner(message, message.from_user.id)
        if is_a_o:
            await func(client, message)
        else:
            await message.reply_text("`>> You Should Be Admin / Owner To Do This! >>`")

    return magic_admin


def _check_owner_or_sudos(func):
    @wraps(func)
    async def magic_owner(client, message):
        use_ = await get_all_pros()
        if message.from_user.id in use_:
            await func(client, message)
        else:
            await message.reply_text("`>> You Should Be Owner / Sudo To Do This! >>`")

    return magic_owner

async def _dl(url, file_name=None):
    if not file_name:
        from urllib.parse import urlparse
        a = urlparse(url)
        file_name = os.path.basename(a.path)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            f = await aiofiles.open(file_name, mode="wb")
            await f.write(await resp.read())
            await f.close()
    return file_name

async def download_yt(url, as_video=False):
    if as_video:
        opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    else:
        opts = {
        "format": "bestaudio",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "720",
            }
        ],
        "outtmpl": "%(id)s.mp3",
        "quiet": True,
        "logtostderr": False,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        return f"**Failed To Download** \n**Error :** `{str(e)}`", None, None, None
    yt_id = ytdl_data['id']
    name = ytdl_data['title']
    dur = ytdl_data["duration"]
    u_date = ytdl_data["upload_date"]
    uploader = ytdl_data["uploader"]
    views = ytdl_data["view_count"]
    thumb_url = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
    downloaded_thumb = await _dl(thumb_url)
    file_name = f"{ytdl_data['id']}.mp4" if as_video else f"{ytdl_data['id']}.mp3"
    return file_name, downloaded_thumb, name, dur, u_date, uploader, views

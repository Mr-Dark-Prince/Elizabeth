# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import os
import time
import requests
import wget
from youtube_dl import YoutubeDL
from youtubesearchpython import SearchVideos
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text, progress, humanbytes


@friday_on_cmd(
    ["utubevid", "ytv"],
    cmd_help={
        "help": "Download YouTube Videos just with name!",
        "example": "{ch}utubevid (video name OR link)",
    },
)
async def yt_vid(client, message):
    input_str = get_text(message)
    pablo = await edit_or_reply(message, f"`Processing...`")
    if not input_str:
        await pablo.edit(
            "`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`"
        )
        return
    await pablo.edit(f"`Getting {input_str} From Youtube Servers. Please Wait.`")
    search = SearchVideos(str(input_str), offset=1, mode="dict", max_results=1)
    rt = search.result()
    result_s = rt["search_result"]
    url = result_s[0]["link"]
    vid_title = result_s[0]["title"]
    yt_id = result_s[0]["id"]
    uploade_r = result_s[0]["channel"]
    thumb_url = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    downloaded_thumb = wget.download(thumb_url)
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
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await pablo.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    file_stark = f"{ytdl_data['id']}.mp4"
    capy = f"**Video Name ➠** `{vid_title}` \n**Requested For ➠** `{input_str}` \n**Channel ➠** `{uploade_r}` \n**Link ➠** `{url}`"
    await client.send_video(
        message.chat.id,
        video=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        thumb=downloaded_thumb,
        caption=capy,
        supports_streaming=True,
        progress=progress,
        progress_args=(
            pablo,
            c_time,
            f"`Uploading {input_str} Song From YouTube Music!`",
            file_stark,
        ),
    )
    await pablo.delete()
    for files in (downloaded_thumb, file_stark):
        if files and os.path.exists(files):
            os.remove(files)
            
@friday_on_cmd(
    ["ytdl"],
    cmd_help={
        "help": "Download All Contents Supported by youtube_dl",
        "example": "{ch}ytdl (link)",
    },
)
async def yt_dl_(client, message):
    input_str = get_text(message)
    pablo = await edit_or_reply(message, f"`Processing...`")
    if not input_str:
        await pablo.edit(
            "`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`"
        )
        return
    await pablo.edit(f"`Downloading Please Wait..`")
    url = input_str
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
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await pablo.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    file_stark = f"{ytdl_data['id']}.mp4"
    size = os.stat(file_stark).st_size
    capy = f"<< **{file_stark}** [`{humanbytes(size)}`] >>"
    await client.send_video(
        message.chat.id,
        video=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        caption=capy,
        supports_streaming=True,
        progress=progress,
        progress_args=(
            pablo,
            c_time,
            f"`Uploading {file_stark}.`",
            file_stark,
        ),
    )
    await pablo.delete()
    if os.path.exists(file_stark):
        os.remove(file_stark)

@friday_on_cmd(
    ["ytmusic", "yta"],
    cmd_help={
        "help": "Download YouTube Music just with name!",
        "example": "{ch}ytmusic (song name OR link)",
    },
)
async def ytmusic(client, message):
    input_str = get_text(message)
    pablo = await edit_or_reply(
        message, f"`Getting {input_str} From Youtube Servers. Please Wait.`"
    )
    if not input_str:
        await pablo.edit(
            "`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`"
        )
        return
    search = SearchVideos(str(input_str), offset=1, mode="dict", max_results=1)
    rt = search.result()
    try:
        result_s = rt["search_result"]
    except:
        await pablo.edit(
            f"Song Not Found With Name {input_str}, Please Try Giving Some Other Name."
        )
        return
    url = result_s[0]["link"]
    result_s[0]["duration"]
    vid_title = result_s[0]["title"]
    yt_id = result_s[0]["id"]
    uploade_r = result_s[0]["channel"]
    thumb_url = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    downloaded_thumb = wget.download(thumb_url)
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
        await pablo.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    capy = f"**Song Name ➠** `{vid_title}` \n**Requested For ➠** `{input_str}` \n**Channel ➠** `{uploade_r}` \n**Link ➠** `{url}`"
    file_stark = f"{ytdl_data['id']}.mp3"
    await client.send_audio(
        message.chat.id,
        audio=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        title=str(ytdl_data["title"]),
        performer=str(ytdl_data["uploader"]),
        thumb=downloaded_thumb,
        caption=capy,
        progress=progress,
        progress_args=(
            pablo,
            c_time,
            f"`Uploading {input_str} Song From YouTube Music!`",
            file_stark,
        ),
    )
    await pablo.delete()
    for files in (downloaded_thumb, file_stark):
        if files and os.path.exists(files):
            os.remove(files)


@friday_on_cmd(
    ["deezer", "dsong"],
    cmd_help={
        "help": "Download Songs From Deezer Just With Name!",
        "example": "{ch}deezer (song name)",
    },
)
async def deezer(client, message):
    pablo = await edit_or_reply(message, "`Searching For Song.....`")
    sgname = get_text(message)
    if not sgname:
        await pablo.edit(
            "`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`"
        )
        return
    link = f"https://api.deezer.com/search?q={sgname}&limit=1"
    dato = requests.get(url=link).json()
    match = dato.get("data")
    try:
        urlhp = match[0]
    except IndexError:
        await pablo.edit("`Song Not Found. Try Searching Some Other Song`")
        return
    urlp = urlhp.get("link")
    thumbs = urlhp["album"]["cover_big"]
    thum_f = wget.download(thumbs)
    polu = urlhp.get("artist")
    replo = urlp[29:]
    urlp = f"https://starkapis.herokuapp.com/deezer/{replo}"
    datto = requests.get(url=urlp).json()
    mus = datto.get("url")
    sname = f"{urlhp.get('title')}.mp3"
    doc = requests.get(mus)
    await client.send_chat_action(message.chat.id, "upload_audio")
    await pablo.edit("`Downloading Song From Deezer!`")
    with open(sname, "wb") as f:
        f.write(doc.content)
    c_time = time.time()
    car = f"""
**Song Name :** {urlhp.get("title")}
**Duration :** {urlhp.get('duration')} Seconds
**Artist :** {polu.get("name")}

Music Downloaded And Uploaded By Friday Userbot

Get Your Friday From @FridayOT"""
    await pablo.edit(f"`Downloaded {sname}! Now Uploading Song...`")
    await client.send_audio(
        message.chat.id,
        audio=open(sname, "rb"),
        duration=int(urlhp.get("duration")),
        title=str(urlhp.get("title")),
        performer=str(polu.get("name")),
        thumb=thum_f,
        caption=car,
        progress=progress,
        progress_args=(pablo, c_time, f"`Uploading {sname} Song From Deezer!`", sname),
    )
    await client.send_chat_action(message.chat.id, "cancel")
    await pablo.delete()

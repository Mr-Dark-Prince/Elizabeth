# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import os
import time

from main_startup.core.decorators import friday_on_cmd
from main_startup.core.startup_helpers import run_cmd
from main_startup.helper_func.basic_helpers import (
    edit_or_reply,
    edit_or_send_as_file,
    get_text,
    progress,
)
from main_startup.helper_func.plugin_helpers import convert_vid_to_vidnote


@friday_on_cmd(
    ["getsrt", "extractsubtitle"],
    cmd_help={
        "help": "Get Subtitle / Srt from Any Video",
        "example": "{ch}getsrt (replying to video file)",
    },
)
async def get_str(client, message):
    msg_ = await edit_or_reply(message, "`Please Halt!`")
    if not message.reply_to_message:
        await msg_.edit("`Please Reply To Video To Get Its Subtitle!`")
        return
    if not message.reply_to_message.video:
        await msg_.edit("`Please Reply To Video To Get Its Subtitle!`")
        return
    c_time = time.time()
    file_ = await message.reply_to_message.download(
        progress=progress, progress_args=(msg_, c_time, f"`Downloading This Video!`")
    )
    file_name = (message.reply_to_message.video.file_name).split(".")[0]
    srt_file_name = str(file_name) + ".srt"
    cmd_to_un = f"ffmpeg -i {file_} {srt_file_name}"
    await run_cmd(cmd_to_un)
    if not os.path.exists(srt_file_name):
        await msg_.edit("`Seems Like This Media Don't Have Subtitle`")
        os.remove(file_)
        return
    await msg_.edit("`Almost Done! Now Uploading Srt File!`")
    if message.reply_to_message:
        await client.send_document(
            message.chat.id,
            srt_file_name,
            caption=f">> {file_name} <<",
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_document(
            message.chat.id, srt_file_name, caption=f">> {file_name} <<"
        )
    await msg_.delete()
    for files in (file_, srt_file_name):
        if files and os.path.exists(files):
            os.remove(files)


@friday_on_cmd(
    ["fastforward"],
    cmd_help={
        "help": "Make Any Video / Gif Fast! (Fast Forward)",
        "example": "{ch}fastforward (replying to video file)",
    },
)
async def hell_speed_s(client, message):
    msg_ = await edit_or_reply(message, "`Please Halt!`")
    if not message.reply_to_message:
        await msg_.edit("`Please Reply To Video To Fast Forward It!`")
        return
    if not (message.reply_to_message.video or message.reply_to_message.animation):
        await msg_.edit("`Please Reply To Video To Fast Forward It!`")
        return
    c_time = time.time()
    file_ = await message.reply_to_message.download(
        progress=progress, progress_args=(msg_, c_time, f"`Downloading This Video!`")
    )
    file_name = "FastForwarded.mp4"
    cmd_to_un = f'ffmpeg -i {file_} -vf "setpts=0.25*PTS" {file_name}'
    await run_cmd(cmd_to_un)
    if not os.path.exists(file_name):
        await msg_.edit("`My Logic Broke! Rip`")
        return
    if message.reply_to_message:
        await client.send_video(
            message.chat.id,
            file_name,
            reply_to_message_id=message.reply_to_message.message_id,
            progress=progress,
            progress_args=(msg_, c_time, f"`Uploading Fast Forwarded Video`"),
        )
    else:
        await client.send_video(
            message.chat.id,
            file_name,
            progress=progress,
            progress_args=(msg_, c_time, f"`Uploading Fast Forwarded Video`"),
        )
    await msg_.delete()
    for files in (file_, file_name):
        if files and os.path.exists(files):
            os.remove(files)


@friday_on_cmd(
    ["slowdown"],
    cmd_help={
        "help": "Make Any Video / Gif Slow! (Slow Down)",
        "example": "{ch}slowdown (replying to video file)",
    },
)
async def fking_slow(client, message):
    msg_ = await edit_or_reply(message, "`Please Halt!`")
    if not message.reply_to_message:
        await msg_.edit("`Please Reply To Video To Slow Down!`")
        return
    if not (message.reply_to_message.video or message.reply_to_message.animation):
        await msg_.edit("`Please Reply To Video To Slow Down!`")
        return
    c_time = time.time()
    file_ = await message.reply_to_message.download(
        progress=progress, progress_args=(msg_, c_time, f"`Downloading This Video!`")
    )
    file_name = "SlowDown.mp4"
    cmd_to_un = f'ffmpeg -i {file_} -vf "setpts=4*PTS" {file_name}'
    await run_cmd(cmd_to_un)
    if not os.path.exists(file_name):
        await msg_.edit("`My Logic Broke! Rip`")
        return
    if message.reply_to_message:
        await client.send_video(
            message.chat.id,
            file_name,
            reply_to_message_id=message.reply_to_message.message_id,
            progress=progress,
            progress_args=(msg_, c_time, f"`Uploading Slow Video`"),
        )
    else:
        await client.send_video(
            message.chat.id,
            file_name,
            progress=progress,
            progress_args=(msg_, c_time, f"`Uploading Slow Video`"),
        )
    await msg_.delete()
    for files in (file_, file_name):
        if files and os.path.exists(files):
            os.remove(files)


@friday_on_cmd(
    ["vidnote"],
    cmd_help={
        "help": "Make Any Video / Gif To Video Note",
        "example": "{ch}vidnote (replying to video file)",
    },
)
async def v_note(client, message):
    msg_ = await edit_or_reply(message, "`Please Halt!`")
    if not message.reply_to_message:
        await msg_.edit("`Please Reply To A Video To Convert To Video Note!`")
        return
    if not (message.reply_to_message.video or message.reply_to_message.animation):
        await msg_.edit("`Please Reply To A Video To Convert To Video Note!`")
        return
    c_time = time.time()
    file_ = await message.reply_to_message.download(
        progress=progress,
        progress_args=(msg_, c_time, f"`Downloading This Video/Gif!`"),
    )
    file_name = "vid_note.mp4"
    await convert_vid_to_vidnote(file_, file_name)
    if not os.path.exists(file_name):
        await msg_.edit("`My Logic Broke! Rip`")
        return
    if message.reply_to_message:
        await client.send_video_note(
            message.chat.id,
            file_name,
            progress=progress,
            progress_args=(msg_, c_time, f"`Uploading Video Note`"),
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_video_note(
            message.chat.id,
            file_name,
            progress=progress,
            progress_args=(msg_, c_time, f"`Uploading Video Note`"),
        )
    await msg_.delete()
    for files in (file_, file_name):
        if files and os.path.exists(files):
            os.remove(files)

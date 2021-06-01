# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import json
import logging
import os
import subprocess
import textwrap
from json import JSONDecodeError
import numpy as np
from PIL import Image, ImageDraw
import requests
from PIL import Image, ImageDraw, ImageFont
from pymediainfo import MediaInfo

from main_startup.core.startup_helpers import run_cmd


def generate_meme(
    image_path,
    top_text,
    bottom_text="",
    font_path="./bot_utils_files/Fonts/impact.ttf",
    font_size=11,
):
    """Make Memes Like A Pro"""
    im = Image.open(image_path)
    draw = ImageDraw.Draw(im)
    image_width, image_height = im.size
    font = ImageFont.truetype(font=font_path, size=int(image_height * font_size) // 100)
    top_text = top_text.upper()
    bottom_text = bottom_text.upper()
    char_width, char_height = font.getsize("A")
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(top_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line)
    y = 9
    for line in top_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2
        draw.text((x - 2, y - 2), line, font=font, fill="black")
        draw.text((x + 2, y - 2), line, font=font, fill="black")
        draw.text((x + 2, y + 2), line, font=font, fill="black")
        draw.text((x - 2, y + 2), line, font=font, fill="black")
        draw.text((x, y), line, fill="white", font=font)
        y += line_height

    y = image_height - char_height * len(bottom_lines) - 14
    for line in bottom_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2
        draw.text((x - 2, y - 2), line, font=font, fill="black")
        draw.text((x + 2, y - 2), line, font=font, fill="black")
        draw.text((x + 2, y + 2), line, font=font, fill="black")
        draw.text((x - 2, y + 2), line, font=font, fill="black")
        draw.text((x, y), line, fill="white", font=font)
        y += line_height
    ok = "memeimg.webp"
    im.save(ok, "WebP")


async def convert_to_image(message, client) -> [None, str]:
    """Convert Most Media Formats To Raw Image"""
    if not message:
        return None
    if not message.reply_to_message:
        return None
    final_path = None
    if not (
        message.reply_to_message.video
        or message.reply_to_message.photo
        or message.reply_to_message.sticker
        or message.reply_to_message.media
        or message.reply_to_message.animation
        or message.reply_to_message.audio
    ):
        return None
    if message.reply_to_message.photo:
        final_path = await message.reply_to_message.download()
    elif message.reply_to_message.sticker:
        if message.reply_to_message.sticker.mime_type == "image/webp":
            final_path = "webp_to_png_s_proton.png"
            path_s = await message.reply_to_message.download()
            im = Image.open(path_s)
            im.save(final_path, "PNG")
        else:
            path_s = await client.download_media(message.reply_to_message)
            final_path = "lottie_proton.png"
            cmd = (
                f"lottie_convert.py --frame 0 -if lottie -of png {path_s} {final_path}"
            )
            await run_cmd(cmd)
    elif message.reply_to_message.audio:
        thumb = message.reply_to_message.audio.thumbs[0].file_id
        final_path = await client.download_media(thumb)
    elif message.reply_to_message.video or message.reply_to_message.animation:
        final_path = "fetched_thumb.png"
        vid_path = await client.download_media(message.reply_to_message)
        await run_cmd(f"ffmpeg -i {vid_path} -filter:v scale=500:500 -an {final_path}")
    return final_path


async def convert_vid_to_vidnote(input_vid: str, final_path: str):
    """ Convert Video To Video Note (Round) """
    media_info = MediaInfo.parse(input_vid)
    for track in media_info.tracks:
        if track.track_type == "Video":
            aspect_ratio = track.display_aspect_ratio
            height = track.height
            width = track.width
    if aspect_ratio != 1:
        crop_by = width if (height > width) else height
        await run_cmd(
            f'ffmpeg -i {input_vid} -vf "crop={crop_by}:{crop_by}" {final_path}'
        )
        os.remove(input_vid)
    else:
        os.rename(input_vid, final_path)
        
async def convert_image_to_image_note(input_path):
    """Crop Image To Circle"""
    img = Image.open(input_path).convert("RGB")
    npImage = np.array(img)
    h, w = img.size
    alpha = Image.new('L', img.size,0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0,0,h,w],0,360,fill=255)
    npAlpha = np.array(alpha)
    npImage = np.dstack((npImage,npAlpha))
    img_path = 'converted_by_FridayUB.webp'
    Image.fromarray(npImage).save(img_path)
    return img_path



def extract_w_h(file):
    """ Extract Video's Width & Height """
    command_to_run = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        file,
    ]
    try:
        t_response = subprocess.check_output(command_to_run, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        logging.error(str(exc))
    else:
        x_reponse = t_response.decode("UTF-8")
        response_json = json.loads(x_reponse)
        width = int(response_json["streams"][0]["width"])
        height = int(response_json["streams"][0]["height"])
        return width, height

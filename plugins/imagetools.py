# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import html
import os
import random
import textwrap
from datetime import datetime
from shutil import rmtree

import cv2
import numpy as np
import pytz
import requests
import wget
from glitch_this import ImageGlitcher
from NoteShrinker import NoteShrinker
from PIL import Image, ImageDraw, ImageFont
from pygifsicle import optimize
from telegraph import Telegraph, exceptions, upload_file

from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd
from main_startup.core.startup_helpers import run_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from main_startup.helper_func.plugin_helpers import (
    convert_to_image,
    convert_image_to_image_note,
    convert_vid_to_vidnote,
    generate_meme
)

glitcher = ImageGlitcher()
DURATION = 200
LOOP = 0

telegraph = Telegraph()
r = telegraph.create_account(short_name="FridayUserBot")
auth_url = r["auth_url"]


@friday_on_cmd(
    ["hwn", "Improvisenote"],
    cmd_help={
        "help": "enhance the replied notes!",
        "example": "{ch}hnw (reply to Image)",
    },
)
async def hwn(client, message):
    pablo = await edit_or_reply(message, "`Processing...`")
    if not message.reply_to_message:
        await pablo.edit("`Reply To Notes / Document To Enhance It!`")
        return
    cool = await convert_to_image(message, client)
    if not cool:
        await pablo.edit("`Reply to a valid media first.`")
        return
    if not os.path.exists(cool):
        await pablo.edit("`Invalid Media!`")
        return
    ns = NoteShrinker([cool])
    shrunk = ns.shrink()
    imag_e = "enhanced_image.png"
    for img in shrunk:
        img.save(imag_e)
    await client.send_photo(message.chat.id, imag_e)
    await pablo.delete()
    os.remove(imag_e)


@friday_on_cmd(
    ["glitch"],
    cmd_help={
        "help": "Glitch the replied image/sticker!",
        "example": "{ch}glitch (reply to Image or sticker)",
    },
)
async def glitchtgi(client, message):
    pablo = await edit_or_reply(message, "`Processing...`")
    if not message.reply_to_message:
        await pablo.edit("Please Reply To Image For Glitching")
        return
    photolove = await convert_to_image(message, client)
    await pablo.edit("`Gli, Glitchiiingggg.....`")
    pathsn = f"Glitched.gif"
    glitch_imgs = glitcher.glitch_image(photolove, 2, gif=True, color_offset=True)
    glitch_imgs[0].save(
        pathsn,
        format="GIF",
        append_images=glitch_imgs[1:],
        save_all=True,
        duration=DURATION,
        loop=LOOP,
    )
    await pablo.edit("`Optimizing Now!`")
    optimize(pathsn)
    await pablo.edit("`Starting Upload!`")
    if message.reply_to_message:
        await client.send_animation(
            message.chat.id,
            pathsn,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_animation(message.chat.id, pathsn)
    if os.path.exists(pathsn):
        os.remove(pathsn)
    await pablo.delete()


@friday_on_cmd(
    ["memify"],
    cmd_help={
        "help": "Make Memes With the replied image/sticker!",
        "example": "{ch}memify (upper text;lower text) (reply to Image or sticker)",
    },
)
async def momify(client, message):
    owo = await edit_or_reply(message, "`Making Memes! Look There, OwO`")
    img = await convert_to_image(message, client)
    hmm = get_text(message)
    if not hmm:
        await owo.edit("`Give Text :/`")
        returbn
    if not img:
        await owo.edit("`Reply to a valid media first.`")
        return
    if not os.path.exists(img):
        await owo.edit("`Invalid Media!`")
        return
    if ";" in hmm:
        stark = hmm.split(";", 1)
        first_txt = stark[0]
        second_txt = stark[1]
        top_text = first_txt
        bottom_text = second_txt
        generate_meme(img, top_text=top_text, bottom_text=bottom_text)
    else:
        top_text = hmm
        bottom_text = ""
        generate_meme(img, top_text=top_text, bottom_text=bottom_text)
    imgpath = "memeimg.webp"
    if message.reply_to_message:
        await client.send_sticker(
            message.chat.id,
            sticker=imgpath,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_sticker(message.chat.id, sticker=imgpath)
    if os.path.exists(imgpath):
        os.remove(imgpath)
    await owo.delete()


@friday_on_cmd(
    ["flip"],
    cmd_help={
        "help": "flip the replied image/sticker!",
        "example": "{ch}flip (reply to Image or sticker)",
    },
)
async def flips(client, message):
    owo = await edit_or_reply(message, "`OwO, Flipping...`")
    img = await convert_to_image(message, client)
    if not img:
        await owo.edit("`Reply to a valid media first.`")
        return
    if not os.path.exists(img):
        await owo.edit("`Invalid Media!`")
        return
    image = cv2.imread(img)
    flipped = cv2.flip(image, 0)
    ok = "Flipped.webp"
    cv2.imwrite(ok, flipped)
    if message.reply_to_message:
        await client.send_sticker(
            message.chat.id,
            sticker=ok,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_sticker(message.chat.id, sticker=ok)
    await owo.delete()
    for files in (ok, img):
        if files and os.path.exists(files):
            os.remove(files)

@friday_on_cmd(
    ["imgnote"],
    cmd_help={
        "help": "Crop Image Into Round & Cool Sticker",
        "example": "{ch}imgnote (reply to Image or sticker)",
    },
)
async def c_imagenote(client, message):
    owo = await edit_or_reply(message, "`OwO, Cropping.`")
    img = await convert_to_image(message, client)
    if not img:
        await owo.edit("`Reply to a valid media first...`")
        return
    if not os.path.exists(img):
        await owo.edit("`Invalid Media!`")
        return
    ok = await convert_image_to_image_note(img)
    if not os.path.exists(ok):
        await owo.edit("`Unable To Convert To Round Image.`")
        return
    if message.reply_to_message:
        await client.send_sticker(
            message.chat.id,
            sticker=ok,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_sticker(message.chat.id, sticker=ok)
    await owo.delete()
    for files in (ok, img):
        if files and os.path.exists(files):
            os.remove(files)


@friday_on_cmd(
    ["mirror"],
    cmd_help={
        "help": "mirror the replied image/sticker!",
        "example": "{ch}mirror (reply to Image or sticker)",
    },
)
async def mirrorlol(client, message):
    owo = await edit_or_reply(message, "`OwO, Let me go near Mirror...`")
    img = await convert_to_image(message, client)
    if not img:
        await owo.edit("`Reply to a valid media first.`")
        return
    if not os.path.exists(img):
        await owo.edit("`Invalid Media!`")
        return
    image = cv2.imread(img)
    flipped = cv2.flip(image, 1)
    ok = "mirrored.webp"
    cv2.imwrite(ok, flipped)
    if message.reply_to_message:
        await client.send_sticker(
            message.chat.id,
            sticker=ok,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_sticker(message.chat.id, sticker=ok)
    await owo.delete()
    for files in (ok, img):
        if files and os.path.exists(files):
            os.remove(files)


@friday_on_cmd(
    ["ghost"],
    cmd_help={
        "help": "ghost the replied image/sticker!",
        "example": "{ch}ghost (reply to Image or sticker)",
    },
)
async def oohno(client, message):
    owo = await edit_or_reply(message, "`OwO, Scarrry Ghosssst`")
    img = await convert_to_image(message, client)
    if not img:
        await owo.edit("`Reply to a valid media first.`")
        return
    if not os.path.exists(img):
        await owo.edit("`Invalid Media!`")
        return
    image = cv2.imread(img)
    treshold, fridaydevs = cv2.threshold(image, 150, 225, cv2.THRESH_BINARY)
    file_name = "Tresh.webp"
    ok = file_name
    cv2.imwrite(ok, fridaydevs)
    if message.reply_to_message:
        await client.send_sticker(
            message.chat.id,
            sticker=ok,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_sticker(message.chat.id, sticker=ok)
    await owo.delete()
    for files in (ok, img):
        if files and os.path.exists(files):
            os.remove(files)


@friday_on_cmd(
    ["sketch"],
    cmd_help={
        "help": "sketch the replied image/sticker!",
        "example": "{ch}sketch (reply to Image or sticker)",
    },
)
async def nice(client, message):
    owo = await edit_or_reply(message, "`OwO, Let Me Draw.`")
    img = await convert_to_image(message, client)
    if not img:
        await owo.edit("`Reply to a valid media first.`")
        return
    if not os.path.exists(img):
        await owo.edit("`Invalid Media!`")
        return
    image = cv2.imread(img)
    scale_percent = 0.60
    width = int(image.shape[1] * scale_percent)
    height = int(image.shape[0] * scale_percent)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    kernel_sharpening = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(resized, -1, kernel_sharpening)
    gray = cv2.cvtColor(sharpened, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    gauss = cv2.GaussianBlur(inv, ksize=(15, 15), sigmaX=0, sigmaY=0)
    pencil_image = dodgeV2(gray, gauss)
    ok = "Drawn.webp"
    cv2.imwrite(ok, pencil_image)
    if message.reply_to_message:
        await client.send_sticker(
            message.chat.id,
            sticker=ok,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_sticker(message.chat.id, sticker=ok)
    await owo.delete()
    for files in (ok, img):
        if files and os.path.exists(files):
            os.remove(files)


def dodgeV2(image, mask):
    return cv2.divide(image, 255 - mask, scale=256)


@friday_on_cmd(
    ["genca", "gencertificate"],
    cmd_help={
        "help": "Get Fake Certificate With Given Name!",
        "example": "{ch}getca (Name On Certificate)",
    },
)
async def getfakecertificate(client, message):
    pablo = await edit_or_reply(message, "`Processing.....`")
    text = get_text(message)
    if not text:
        await pablo.edit("Please Give Name For Certificate")
        return
    famous_people = ["Modi", "Trump", "Albert", "Gandhi", "Chsaiujwal", "Aditya"]
    img = Image.open("./bot_utils_files/image_templates/certificate_templete.png")
    d1 = ImageDraw.Draw(img)
    myFont = ImageFont.truetype("./bot_utils_files/Fonts/impact.ttf", 200)
    myFont2 = ImageFont.truetype("./bot_utils_files/Fonts/impact.ttf", 70)
    myFont3 = ImageFont.truetype("./bot_utils_files/Fonts/Streamster.ttf", 50)
    d1.text((1433, 1345), text, font=myFont, fill=(51, 51, 51))
    TZ = pytz.timezone(Config.TZ)
    datetime_tz = datetime.now(TZ)
    oof = datetime_tz.strftime(f"%Y/%m/%d")
    d1.text((961, 2185), oof, font=myFont2, fill=(51, 51, 51))
    d1.text((2441, 2113), random.choice(famous_people), font=myFont3, fill=(51, 51, 51))
    file_name = "certificate.png"
    ok = file_name
    img.save(ok, "PNG")
    if message.reply_to_message:
        await client.send_photo(
            message.chat.id,
            photo=ok,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_photo(message.chat.id, photo=ok)
    await pablo.delete()
    if os.path.exists(ok):
        os.remove(ok)


@friday_on_cmd(
    ["thug"],
    cmd_help={
        "help": "thug the replied image/sticker!",
        "example": "{ch}thug (reply to Image or sticker)",
    },
)
async def weallarethugs(client, message):
    tgi = await edit_or_reply(message, "`Using My Thug Algo To Make Him Thug!`")
    img = await convert_to_image(message, client)
    if not img:
        await tgi.edit("`Reply to a valid media first.`")
        return
    if not os.path.exists(img):
        await tgi.edit("`Invalid Media!`")
        return
    imagePath = img
    maskPath = "./bot_utils_files/image_templates/thug_life_mask.png"
    cascPath = "./bot_utils_files/ai_helpers/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.15)
    background = Image.open(imagePath)
    for (x, y, w, h) in faces:
        mask = Image.open(maskPath)
        mask = mask.resize((w, h), Image.ANTIALIAS)
        offset = (x, y)
        background.paste(mask, offset, mask=mask)
    file_name = "proton_thug.png"
    background.save(file_name, "PNG")
    if message.reply_to_message:
        await client.send_photo(
            message.chat.id,
            photo=file_name,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_photo(message.chat.id, photo=file_name)
    await tgi.delete()
    for files in (file_name, img):
        if files and os.path.exists(files):
            os.remove(files)


@friday_on_cmd(
    ["toon"],
    cmd_help={
        "help": "toonify the replied image/sticker!",
        "example": "{ch}toon (reply to Image or sticker)",
    },
)
async def toonize(client, message):
    tgi = await edit_or_reply(message, "`Using My Toonize Algo To Make Him A Cartoon!`")
    img = await convert_to_image(message, client)
    if not img:
        await tgi.edit("`Reply to a valid media first.`")
        return
    if not os.path.exists(img):
        await tgi.edit("`Invalid Media!`")
        return
    imagez = cv2.imread(img)
    cartoon_image_style_2 = cv2.stylization(imagez, sigma_s=60, sigma_r=0.5)
    file_name = "Tooned.png"
    cv2.imwrite(file_name, cartoon_image_style_2)
    if message.reply_to_message:
        await client.send_photo(
            message.chat.id,
            photo=file_name,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_photo(message.chat.id, photo=file_name)
    await tgi.delete()
    for files in (file_name, img):
        if files and os.path.exists(files):
            os.remove(files)


@friday_on_cmd(
    ["lnews"],
    cmd_help={
        "help": "Create Fake News With Text Headlines and replied image/sticker!",
        "example": "{ch}lnews (Headlines Text) (reply to Image or sticker)",
    },
)
async def wewnews(client, message):
    pablo = await edit_or_reply(message, "`Processing.....`")
    text = get_text(message)
    if not text:
        await pablo.edit("Please Give Headlines For News")
        return
    if not message.reply_to_message:
        await pablo.edit("Please Reply To Image For News")
        return
    img = await convert_to_image(message, client)
    if not img:
        await pablo.edit("`Reply to a valid media first.`")
        return
    if not os.path.exists(img):
        await pablo.edit("`Invalid Media!`")
        return
    background = Image.open(img)
    newss = "./bot_utils_files/image_templates/live_new_templete.png"
    foreground = Image.open(newss)
    im = background.resize((2800, 1500))
    im.paste(foreground, (0, 0), mask=foreground)
    d1 = ImageDraw.Draw(im)
    myFont = ImageFont.truetype("./bot_utils_files/Fonts/live_news_font.ttf", 165)
    d1.text((7, 1251), text, font=myFont, fill=(0, 0, 0))
    im.save("Fridaylivenews.png")
    file_name = "Fridaylivenews.png"
    ok = file_name
    if message.reply_to_message:
        await client.send_photo(
            message.chat.id,
            photo=ok,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_photo(message.chat.id, photo=ok)
    await pablo.delete()
    for files in (ok, img):
        if files and os.path.exists(files):
            os.remove(files)


@friday_on_cmd(
    ["colorize"],
    cmd_help={
        "help": "Colorise the replied Back&white image/sticker!",
        "example": "{ch}colorize (reply to Image or sticker)",
    },
)
async def color_magic(client, message):
    owo = await edit_or_reply(message, "`Using My Color Magic To Color This, OwO!`")
    img = await convert_to_image(message, client)
    if not img:
        await owo.edit("`Reply to a valid media first.`")
        return
    if not os.path.exists(img):
        await owo.edit("`Invalid Media!`")
        return
    net = cv2.dnn.readNetFromCaffe(
        "./bot_utils_files/ai_helpers/colouregex.prototxt",
        "./bot_utils_files/ai_helpers/colorization_release_v2.caffemodel",
    )
    pts = np.load("./bot_utils_files/ai_helpers/pts_in_hull.npy")
    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    pts = pts.transpose().reshape(2, 313, 1, 1)
    net.getLayer(class8).blobs = [pts.astype("float32")]
    net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]
    image = cv2.imread(img)
    scaled = image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))
    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)
    colorized = (255 * colorized).astype("uint8")
    ok = "Colour.png"
    cv2.imwrite(ok, colorized)
    if message.reply_to_message:
        await client.send_photo(
            message.chat.id,
            photo=ok,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_photo(message.chat.id, photo=ok)
    await owo.delete()
    for files in (ok, img):
        if files and os.path.exists(files):
            os.remove(files)


@friday_on_cmd(
    ["spin"],
    cmd_help={
        "help": "Spin the replied image/sticker!",
        "example": "{ch}spin (number between 1-6) (reply to Image or sticker)",
    },
)
async def spin(client, message):
    pablo = await edit_or_reply(message, "`Processing.....`")
    lolshit = get_text(message)
    if not lolshit:
        lolshit = "1"
    lmaodict = {"1": 1, "2": 3, "3": 6, "4": 12, "5": 24, "6": 60}
    if not lolshit.isnumeric():
        await pablo.edit("`Only Speed from 1-6 Is Allowded !`")
        return
    if int(lolshit) > 6:
        await pablo.edit("`Only Speed from 1-6 Is Allowded !`")
        return
    keke = str(lolshit)
    if not message.reply_to_message:
        await pablo.edit("`Reply To Media First !`")
        return
    else:
        if lolshit:
            step = lmaodict.get(keke)
        else:
            step = 1
    pic_loc = await convert_to_image(message, client)
    if not pic_loc:
        await pablo.edit("`Reply to a valid media first.`")
        return
    if not os.path.exists(pic_loc):
        await pablo.edit("`No Media Found!`")
        return
    await pablo.edit("🌀 `Tighten your seatbelts, sh*t is about to get wild ...`")
    spin_dir = 1
    path = "./rotate-disc/"
    if not os.path.exists(path):
        os.mkdir(path)
    im = Image.open(pic_loc)
    if im.mode != "RGB":
        im = im.convert("RGB")
    for k, nums in enumerate(range(1, 360, step), start=0):
        y = im.rotate(nums * spin_dir)
        y.save(os.path.join(path, "spinx%s.jpg" % k))
    output_vid = os.path.join(path, "out.mp4")
    # ;__; Maths lol, y = mx + c
    frate = int(((90 / 59) * step) + (1680 / 59))
    await run_cmd(
        f'ffmpeg -framerate {frate} -i {path}spinx%d.jpg -c:v libx264 -preset ultrafast -vf "crop=trunc(iw/2)*2:trunc(ih/2)*2" -pix_fmt yuv420p {output_vid}'
    )
    if os.path.exists(output_vid):
        round_vid = os.path.join(path, "out_round.mp4")
        await convert_vid_to_vidnote(output_vid, round_vid)
        await client.send_video_note(
            message.chat.id,
            round_vid,
            reply_to_message_id=message.reply_to_message.message_id,
        )
        await pablo.delete()
    os.remove(pic_loc)
    rmtree(path, ignore_errors=True)


@friday_on_cmd(
    ["ph"],
    cmd_help={
        "help": "Create Fake PornHub Comment With Given Name And Text!",
        "example": "{ch}ph (Name:Comment)",
    },
)
async def ph(client, message):
    pablo = await edit_or_reply(message, "`Processing.....`")
    Hell = get_text(message)
    if not Hell:
        await pablo.edit(
            "`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`"
        )
        return
    Escobar = Hell.split(":")
    username = Escobar[0]
    try:
        texto = Escobar[1]
    except:
        await pablo.edit(
            "`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`"
        )
        return
    img = Image.open("./bot_utils_files/image_templates/ph_comment_templete.jpg")
    d1 = ImageDraw.Draw(img)
    myFont = ImageFont.truetype("./bot_utils_files/Fonts/ph_comment_font.TTF", 100)
    d1.text((300, 700), username, font=myFont, fill=(135, 98, 87))
    d1.text((12, 1000), texto, font=myFont, fill=(203, 202, 202))
    img.save("FRIDAYOT.jpg")
    file_name = "FRIDAYOT.jpg"
    ok = file_name
    if message.reply_to_message:
        await client.send_photo(
            message.chat.id,
            photo=ok,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_photo(message.chat.id, photo=ok)
    if os.path.exists(ok):
        os.remove(ok)
    await pablo.delete()


@friday_on_cmd(
    ["fgs"],
    cmd_help={
        "help": "Create Fake Google Search!",
        "example": "{ch}fgs (search text: recommend text)",
    },
)
async def fgs(client, message):
    pablo = await edit_or_reply(message, "`Processing.....`")
    Hell = get_text(message)
    if not Hell:
        await pablo.edit(
            "`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`"
        )
        return
    Escobar = Hell.split(":")
    search = Escobar[0]
    try:
        result = Escobar[1]
    except:
        await pablo.edit(
            "`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`"
        )
        return
    photo = Image.open("./bot_utils_files/image_templates/google_search_templete.jpg")
    drawing = ImageDraw.Draw(photo)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    font1 = ImageFont.truetype("./bot_utils_files/Fonts/ProductSans-BoldItalic.ttf", 20)
    font2 = ImageFont.truetype("./bot_utils_files/Fonts/ProductSans-Light.ttf", 23)
    drawing.text((450, 258), result, fill=blue, font=font1)
    drawing.text((270, 37), search, fill=black, font=font2)
    file_name = "fgs.jpg"
    photo.save(file_name)
    await pablo.delete()
    if message.reply_to_message:
        await client.send_photo(
            message.chat.id,
            photo=file_name,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_photo(message.chat.id, photo=file_name)
    if os.path.exists(file_name):
        os.remove(file_name)


@friday_on_cmd(
    ["jail"],
    cmd_help={
        "help": "Jail the replied image/sticker!",
        "example": "{ch}jail (reply to Image or sticker)",
    },
)
async def jail(client, message):
    pablo = await edit_or_reply(message, "`Processing.....`")
    Hell = get_text(message)
    if not Hell and not message.reply_to_message:
        await pablo.edit(
            "`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`"
        )
        return
    if message.reply_to_message:
        img = await convert_to_image(message, client)
        if img is False:
            lol = await client.get_profile_photos(
                message.reply_to_message.from_user.id, limit=1
            )
            try:
                img = await client.download_media(lol[0].file_id)
            except IndexError:
                await pablo.edit("User Has No Profile Picture")
                return
    if Hell and not message.reply_to_message:
        lol = await client.get_profile_photos(Hell, limit=1)

        try:
            img = await client.download_media(lol[0].file_id)

        except IndexError:
            await pablo.edit("User Has No Profile Picture")
            return
    mon = "./bot_utils_files/image_templates/jail_templete.png"
    foreground = Image.open(mon).convert("RGBA")
    background = Image.open(img).convert("RGB")
    with Image.open(img) as img:
        width, height = img.size
    fg_resized = foreground.resize((width, height))
    background.paste(fg_resized, box=(0, 0), mask=fg_resized)
    background.save("FridayJail.png")
    file_name = "FridayJail.png"
    if message.reply_to_message:
        await client.send_photo(
            message.chat.id,
            photo=file_name,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_photo(message.chat.id, photo=file_name)
    await pablo.delete()
    if os.path.exists(file_name):
        os.remove(file_name)


@friday_on_cmd(
    ["picgen", "fakepic", "fpic"],
    cmd_help={"help": "Generates Fake Image!", "example": "{ch}picgen"},
)
async def picgen(client, message):
    pablo = await edit_or_reply(message, "`Processing.....`")
    url = "https://thispersondoesnotexist.com/image"
    response = requests.get(url)
    if response.status_code == 200:
        with open("FRIDAYOT.jpg", "wb") as f:
            f.write(response.content)
    captin = f"Fake Image By Friday.\nGet Your Own Friday From @FRIDAYCHAT."
    fole = "FRIDAYOT.jpg"
    if message.reply_to_message:
        await client.send_photo(
            message.chat.id,
            photo=fole,
            caption=captin,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_photo(message.chat.id, photo=fole, caption=captin)
    await pablo.delete()
    if os.path.exists(fole):
        os.remove(fole)


@friday_on_cmd(
    ["slogo"],
    cmd_help={
        "help": "Create A logo with given text!",
        "example": "{ch}slogo (text for logo)",
    },
)
async def slogo(client, message):
    event = await edit_or_reply(message, "`Processing.....`")
    text = get_text(message)
    if not text:
        await event.edit(
            "`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`"
        )
        return
    img = Image.open("./bot_utils_files/image_templates/yellow_bg_for_logo.jpg")
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    font = ImageFont.truetype("./bot_utils_files/Fonts/BADABB__.TTF", 650)
    w, h = draw.textsize(text, font=font)
    h += int(h * 0.21)
    image_width, image_height = img.size
    draw.text(
        ((image_widthz - w) / 2, (image_heightz - h) / 2),
        text,
        font=font,
        fill=(200, 200, 200),
    )
    x = (image_widthz - w) / 2
    y = (image_heightz - h) / 2
    await client.send_chat_action(message.chat.id, "upload_photo")
    draw.text(
        (x, y), text, font=font, fill="white", stroke_width=60, stroke_fill="black"
    )
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await client.send_chat_action(message.chat.id, "cancel")
    if message.reply_to_message:
        await client.send_photo(
            message.chat.id,
            photo=fname2,
            caption="Made Using FridayUserBot",
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_photo(
            message.chat.id, photo=fname2, caption="Made Using FridayUserBot"
        )
    await event.delete()
    if os.path.exists(fname2):
        os.remove(fname2)


@friday_on_cmd(
    ["adityalogo", "alogo"],
    cmd_help={
        "help": "Create AdityaLogo With Given Text!",
        "example": "{ch}adityalogo (text for logo)",
    },
)
async def adityalogo(client, message):
    event = await edit_or_reply(message, "`Processing.....`")
    text = get_text(message)
    if not text:
        await event.edit(
            "`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`"
        )
        return
    img = Image.open("./bot_utils_files/image_templates/black_blank_image.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./bot_utils_files/Fonts/Streamster.ttf", 220)
    image_widthz, image_heightz = img.size
    w, h = draw.textsize(text, font=font)
    h += int(h * 0.21)
    draw.text(
        ((image_widthz - w) / 2, (image_heightz - h) / 2),
        text,
        font=font,
        fill=(255, 255, 0),
    )
    file_name = "LogoBy@MeisNub.png"
    await client.send_chat_action(message.chat.id, "upload_photo")
    img.save(file_name, "png")
    if message.reply_to_message:
        await client.send_photo(
            message.chat.id,
            photo=file_name,
            caption="Made Using FridayUserBot",
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_photo(
            message.chat.id, photo=file_name, caption="Made Using FridayUserBot"
        )
    await client.send_chat_action(message.chat.id, "cancel")
    await event.delete()
    if os.path.exists(file_name):
        os.remove(file_name)


@friday_on_cmd(
    ["stcr"],
    cmd_help={
        "help": "Create Cool Stickers !",
        "example": "{ch}stcr Ujwal",
    },
)
async def ujwal_s_ticker(client, message):
    msg_ = await edit_or_reply(message, "`Processing.....`")
    text = get_text(message)
    if not text:
        msg_.edit("`Give Me Text As Input!`")
        return
    sticktext = textwrap.wrap(text, width=10)
    sticktext = "\n".join(sticktext)
    R = random.randint(0, 256)
    G = random.randint(0, 256)
    B = random.randint(0, 256)
    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    font_ = choose_random_font()
    fontsize = 230
    font = ImageFont.truetype(font_, size=fontsize)
    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype(font_, size=fontsize)
    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(
        ((512 - width) / 2, (512 - height) / 2), sticktext, font=font, fill=(R, G, B)
    )
    ok = "sticklet.webp"
    image.save(ok, "WebP")
    if message.reply_to_message:
        await client.send_sticker(
            message.chat.id,
            sticker=ok,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_sticker(message.chat.id, sticker=ok)
    await msg_.delete()
    for files in (font_, ok):
        if files and os.path.exists(files):
            os.remove(files)


def choose_random_font():
    fonts_ = [
        "https://github.com/DevsExpo/FONTS/raw/main/Ailerons-Typeface.otf",
        "https://github.com/DevsExpo/FONTS/raw/main/Toxico.otf",
        "https://github.com/DevsExpo/FONTS/raw/main/againts.otf",
        "https://github.com/DevsExpo/FONTS/raw/main/go3v2.ttf",
        "https://github.com/DevsExpo/FONTS/raw/main/vermin_vibes.ttf",
    ]
    random_s = random.choice(fonts_)
    return wget.download(random_s)

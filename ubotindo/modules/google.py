import asyncio
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
#from google_images_download import google_images_download
import sys
import shutil
from re import findall
import html2text

@register(pattern="^/google (.*)") 
async def _(event):
    if event.fwd_from:
        return
    if event.is_group:
     if not (await is_register_admin(event.input_chat, event.message.sender_id)):
       await event.reply("")
       return
    # SHOW_DESCRIPTION = False
    input_str = event.pattern_match.group(1) # + " -inurl:(htm|html|php|pls|txt) intitle:index.of \"last modified\" (mkv|mp4|avi|epub|pdf|mp3)"
    input_url = "https://bots.shrimadhavuk.me/search/?q={}".format(input_str)
    headers = {"USER-AGENT": "UniBorg"}
    response = requests.get(input_url, headers=headers).json()
    output_str = " "
    for result in response["results"]:
        text = result.get("title")
        url = result.get("url")
        description = result.get("description")
        last = html2text.html2text(description)
        output_str += "[{}]({})\n{}\n".format(text, url, last)       
    await event.reply("{}".format(output_str), link_preview=False, parse_mode='Markdown')

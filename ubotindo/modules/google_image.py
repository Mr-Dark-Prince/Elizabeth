# from alexa.google_imgs import googleimagesdownload
import os
import shutil
from re import findall
from bing_image_downloader import downloader
import os
import glob
from ubotindo.events import register


@register(pattern="^/img (.*)")
async def img_sampler(event):
     if event.fwd_from:
        return
     if event.is_group:
       if not (await is_register_admin(event.input_chat, event.message.sender_id)):
          await event.reply("")
          return
     query = event.pattern_match.group(1)
     jit = f'"{query}"'
     downloader.download(jit, limit=5, output_dir='store', adult_filter_off=False, force_replace=False, timeout=60)
     os.chdir(f'./store/"{query}"')
     types = ('*.png', '*.jpeg', '*.jpg') # the tuple of file types
     files_grabbed = []
     for files in types:
         files_grabbed.extend(glob.glob(files))
     await event.client.send_file(event.chat_id, files_grabbed, reply_to=event.id)
     os.remove(files_grabbed)
     os.chdir('./')

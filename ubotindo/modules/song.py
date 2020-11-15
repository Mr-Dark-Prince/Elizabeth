from youtube_search import YoutubeSearch
from pytube import YouTube as YT, exceptions
from ubotindo import utils
import os
import json
import logging
import glob
import subprocess


    async def songxxx(message):
        args = utils.get_arg(message)
        reply = await message.get_reply_message()
        if not args:
            await message.edit("<i>Enter a song name first</i>")
            return
        await message.edit("<i>Searching..</i>")
        results = json.loads(YoutubeSearch(args, max_results=1).to_json())
        if results:
            await message.edit("<i>Downloading</i>")
            link = f"https://www.youtube.com{results['videos'][0]['link']}"
            cmd = f"youtube2mp3 -d {os.getcwd()} -y {link}"
            process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            process.wait()
            await message.edit("<i>Uploading..</i>")
            file = glob.glob("*.mp3")[0]
            await message.client.send_file(message.chat_id, file, reply_to=reply.id if reply else None)
            await message.delete()
            os.remove(file)

# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.


import os

from telegraph import Telegraph, exceptions, upload_file

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from main_startup.helper_func.plugin_helpers import convert_to_image

telegraph = Telegraph()
r = telegraph.create_account(short_name="FridayUserBot")
auth_url = r["auth_url"]


@friday_on_cmd(
    ["telegraph"],
    cmd_help={
        "help": "Get Telegraph link of replied image",
        "example": "{ch}telegraph (reply to text or image)",
    },
)
async def telegrapher(client, message):
    pablo = await edit_or_reply(message, "`Processing..`")
    if not message.reply_to_message:
        await pablo.edit("Reply To Message To Parse it To Telegraph !")
        return
    if message.reply_to_message.media:
        # Assume its media
        if message.reply_to_message.sticker:
            m_d = await convert_to_image(message, client)
        else:
            m_d = await message.reply_to_message.download()
        try:
            media_url = upload_file(m_d)
        except exceptions.TelegraphException as exc:
            await pablo.edit(
                f"`Unable To Upload Media To Telegraph! \nTraceBack : {exc}`"
            )
            os.remove(m_d)
            return
        U_done = f"Uploaded To Telegraph! \nLink : https://telegra.ph/{media_url[0]}"
        await pablo.edit(U_done, disable_web_page_preview=False)
        os.remove(m_d)
    elif message.reply_to_message.text:
        # Assuming its text
        page_title = get_text(message) if get_text(message) else client.me.first_name
        page_text = message.reply_to_message.text
        page_text = page_text.replace("\n", "<br>")
        try:
            response = telegraph.create_page(page_title, html_content=page_text)
        except exceptions.TelegraphException as exc:
            await pablo.edit(f"`Unable To Create Telegraph! \nTraceBack : {exc}`")
            return
        wow_graph = f"Telegraphed! \nLink : https://telegra.ph/{response['path']}"
        await pablo.edit(wow_graph, disable_web_page_preview=False)

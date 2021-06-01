# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import os

from main_startup.core.decorators import friday_on_cmd
from main_startup.core.startup_helpers import load_plugin
from main_startup.helper_func.basic_helpers import edit_or_reply


@friday_on_cmd(
    ["install"],
    cmd_help={
        "help": "Install Custom Plugins In Userbot",
        "example": "{ch}install (replying to plugin (.py))",
    },
)
async def installer(client, message):
    pablo = await edit_or_reply(message, "`Processing...`")
    if not message.reply_to_message:
        await pablo.edit("`Reply To A Plugin File To Install Plugin`")
        return
    if not message.reply_to_message.document:
        await pablo.edit("`Is It A Even A Document?`")
        return
    file_name = message.reply_to_message.document.file_name
    ext = file_name.split(".")[1]
    if os.path.exists(os.path.join("./plugins/", file_name)):
        await pablo.edit("`This Plugin is Already Installed!`")
        return
    if not ext.lower() == "py":
        await pablo.edit("`Only Py Files :(`")
        return
    Escobar = await message.reply_to_message.download(file_name="./plugins/")
    base_name = os.path.basename(Escobar)
    file_n = base_name.split(".")[0]
    try:
        load_plugin(file_n)
    except Exception as e:
        await pablo.edit(f"Error Installing Plugin.\n**Error** {e}")
        os.remove(Escobar)
        return
    await pablo.edit(f"`Sucessfully Installed {file_name}!`")

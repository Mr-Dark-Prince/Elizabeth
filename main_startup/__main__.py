# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import logging
import os
import platform

import pyrogram
from pyrogram import __version__

from main_startup import (
    Friday,
    Friday2,
    Friday3,
    Friday4,
    bot,
    friday_version,
    mongo_client,
)
from main_startup.core.startup_helpers import (
    load_plugin,
    load_xtra_mod,
    plugin_collecter,
    run_cmd,
    update_it
)

from .config_var import Config


async def mongo_check():
    """Check Mongo Client"""
    try:
        await mongo_client.server_info()
    except BaseException as e:
        logging.error("Something Isn't Right With Mongo! Please Check Your URL")
        logging.error(str(e))
        quit(1)


async def load_unofficial_modules():
    """Load Extra Plugins."""
    logging.info("Loading X-Tra Plugins!")
    await run_cmd("bash bot_utils_files/other_helpers/xtra_plugins.sh")
    xtra_mods = plugin_collecter("./xtraplugins/")
    for mods in xtra_mods:
        try:
            load_xtra_mod(mods)
        except Exception as e:
            logging.error(
                "[USER][XTRA-PLUGINS] - Failed To Load : " + f"{mods} - {str(e)}"
            )


async def fetch_plugins_from_channel():
    """Fetch Plugins From Channel"""
    try:
        async for message in Friday.search_messages(
            Config.PLUGIN_CHANNEL, filter="document", query=".py"
        ):
            hmm = message.document.file_name
            if os.path.exists(os.path.join("./plugins/", hmm)):
                pass
            else:
                await Friday.download_media(message, file_name="./plugins/")
    except BaseException as e:
        logging.error(f"Failed! To Install Plugins From Plugin Channel Due To {e}!")
        return
    logging.info("All Plugins From Plugin Channel Loaded!")


async def run_bot():
    """Run The Bot"""
    await mongo_check()
    try:
        await update_it()
    except:
        pass
    if bot:
        await bot.start()
        bot.me = await bot.get_me()
        assistant_mods = plugin_collecter("./assistant/")
        for mods in assistant_mods:
            try:
                load_plugin(mods, assistant=True)
            except Exception as e:
                logging.error("[ASSISTANT] - Failed To Load : " + f"{mods} - {str(e)}")
    await Friday.start()
    Friday.me = await Friday.get_me()
    Friday.has_a_bot = True if bot else False
    if Friday2:
        await Friday2.start()
        Friday2.me = await Friday2.get_me()
        Friday2.has_a_bot = True if bot else False
    if Friday3:
        await Friday3.start()
        Friday3.me = await Friday3.get_me()
        Friday3.has_a_bot = True if bot else False
    if Friday4:
        await Friday4.start()
        Friday4.me = await Friday4.get_me()
        Friday4.has_a_bot = True if bot else False
    if Config.PLUGIN_CHANNEL:
        await fetch_plugins_from_channel()
    needed_mods = plugin_collecter("./plugins/")
    for nm in needed_mods:
        try:
            load_plugin(nm)
        except Exception as e:
            logging.error("[USER] - Failed To Load : " + f"{nm} - {str(e)}")
    if Config.LOAD_UNOFFICIAL_PLUGINS:
        await load_unofficial_modules()
    full_info = f"""Friday Based On Pyrogram V{__version__}
Python Version : {platform.python_version()}
Friday Version : {friday_version}
You Can Visit @FridaySupportOfficial For Updates And @FridayChat For Any Query / Help!
"""
    logging.info(full_info)
    await pyrogram.idle()


if __name__ == "__main__":
    Friday.loop.run_until_complete(run_bot())

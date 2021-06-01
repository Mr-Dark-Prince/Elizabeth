# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import os

import heroku3
from dotenv import load_dotenv
from distutils.util import strtobool

if os.path.exists("local.env"):
    load_dotenv("local.env")


def fetch_heroku_git_url(api_key, app_name):
    if not api_key:
        return None
    if not app_name:
        return None
    heroku = heroku3.from_key(api_key)
    try:
        heroku_applications = heroku.apps()
    except:
        return None
    heroku_app = None
    for app in heroku_applications:
        if app.name == app_name:
            heroku_app = app
            break
    if not heroku_app:
        return None
    return heroku_app.git_url.replace("https://", "https://api:" + api_key + "@")


class Config(object):
    API_ID = int(os.environ.get("API_ID", 1))
    API_HASH = os.environ.get("API_HASH", None)
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)
    STRINGSESSION = os.environ.get("STRINGSESSION", None)
    ASSISTANT_START_PIC = os.environ.get(
        "ASSISTANT_START_PIC", "https://telegra.ph//file/92c1a600394c723db90fc.jpg"
    )
    STRINGSESSION_2 = os.environ.get("STRINGSESSION_2", None)
    STRINGSESSION_3 = os.environ.get("STRINGSESSION_3", None)
    STRINGSESSION_4 = os.environ.get("STRINGSESSION_4", None)
    LOAD_UNOFFICIAL_PLUGINS = bool(strtobool(str(os.environ.get("LOAD_UNOFFICIAL_PLUGINS", False))))
    PLUGIN_CHANNEL = os.environ.get("PLUGIN_CHANNEL", False)
    TZ = os.environ.get("TZ", "Asia/Kolkata")
    MONGO_DB = os.environ.get("MONGO_DB", None)
    LOG_GRP = int(os.environ.get("LOG_GRP", False))
    COMMAND_HANDLER = os.environ.get("COMMAND_HANDLER", ".")
    SUDO_USERS = set(int(x) for x in os.environ.get("SUDO_USERS", "").split())
    AFS = list(SUDO_USERS)
    CUSTOM_HELP_EMOJI = os.environ.get("CUSTOM_HELP_EMOJI", "✘")
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    LYDIA_API_KEY = os.environ.get("LYDIA_API_KEY", None)
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    FBAN_GROUP = int(os.environ.get("FBAN_GROUP", False))
    UPSTREAM_REPO = os.environ.get(
        "UPSTREAM_REPO", "https://github.com/DevsExpo/FridayUserbot"
    )
    ALIVE_IMG = os.environ.get(
        "ALIVE_IMG", "https://telegra.ph//file/b94f56dd76b158149992e.jpg"
    )
    U_BRANCH = "master"
    HEROKU_URL = fetch_heroku_git_url(HEROKU_API_KEY, HEROKU_APP_NAME)
    V_T_KEY = os.environ.get("VIRUSTOTAL_API_KEY", None)
    TAG_LOGGER = os.environ.get("TAG_LOGGER", False)
    PM_PSW = bool(strtobool(str(os.environ.get("PM_PSW", True))))
    MAIN_NO_LOAD = [x for x in os.environ.get("MAIN_NO_LOAD", "").split(',')]
    XTRA_NO_LOAD = [x for x in os.environ.get("XTRA_NO_LOAD", "").split(',')]
    DISABLED_SUDO_CMD_S = os.environ.get("DISABLED_SUDO_CMD_S", None)
    ENABLE_WAIFU_FOR_ALL_CHATS = bool(strtobool(str(os.environ.get("ENABLE_WAIFU_FOR_ALL_CHATS", False))))
    CHROME_DRIVER_PATH = os.environ.get("CHROME_DRIVER_PATH", "/usr/bin/chromedriver")
    CHROME_BIN_PATH = os.environ.get("CHROME_BIN_PATH", "/usr/bin/google-chrome-stable")

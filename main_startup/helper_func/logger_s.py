# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import logging
import os

from main_startup import Config
from main_startup.helper_func.basic_helpers import edit_or_send_as_file


class LogIt:
    def __init__(self, message):
        self.chat_id = Config.LOG_GRP
        self.message = message

    async def log_msg(self, client, text: str = "?"):
        if len(text) > 1024:
            try:
                Hitler = await client.send_document(self.chat_id, make_file(text))
            except BaseException as e:
                logging.error(str(e))
                return None
            os.remove("logger.log")
            return Hitler
        else:
            try:
                return await client.send_message(self.chat_id, text)
            except:
                logging.error(str(e))
                return None

    async def fwd_msg_to_log_chat(self):
        try:
            return await self.message.forward(self.chat_id)
        except BaseException as e:
            logging.error(str(e))
            return None


def make_file(text):
    open("logger.log", "w").write(text)
    return "logger.log"

# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import inspect
import logging
import os
from datetime import datetime
from traceback import format_exc

import pytz
from pyrogram import ContinuePropagation, StopPropagation, filters
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageIdInvalid,
    MessageNotModified,
    MessageEmpty,
    UserNotParticipant
)
from pyrogram.handlers import MessageHandler

from main_startup import (
    CMD_LIST,
    XTRA_CMD_LIST,
    Config,
    Friday,
    Friday2,
    Friday3,
    Friday4,
    bot
)
from main_startup.config_var import Config
from main_startup.helper_func.basic_helpers import is_admin_or_owner

from .helpers import edit_or_reply


def friday_on_cmd(
    cmd: list,
    group: int = 0,
    pm_only: bool = False,
    group_only: bool = False,
    chnnl_only: bool = False,
    only_if_admin: bool = False,
    ignore_errors: bool = False,
    propagate_to_next_handler: bool = True,
    file_name: str = None,
    is_official: bool = True,
    cmd_help: dict = {"help": "No One One Gonna Help You", "example": "{ch}what"},
):
    """- Main Decorator To Register Commands. -"""
    filterm = (
        (filters.me | filters.user(Config.AFS))
        & filters.command(cmd, Config.COMMAND_HANDLER)
        & ~filters.via_bot
        & ~filters.forwarded
    )
    add_help_menu(
        cmd=cmd[0],
        stack=inspect.stack(),
        is_official=is_official,
        cmd_help=cmd_help["help"],
        example=cmd_help["example"],
    )

    def decorator(func):
        async def wrapper(client, message):
            message.client = client
            chat_type = message.chat.type
            if only_if_admin and not await is_admin_or_owner(
                message, (client.me).id
            ):
                await edit_or_reply(
                    message, "`This Command Only Works, If You Are Admin Of The Chat!`"
                )
                return
            if group_only and chat_type != "supergroup":
                await edit_or_reply(message, "`Are you sure this is a group?`")
                return
            if chnnl_only and chat_type != "channel":
                await edit_or_reply(message, "This Command Only Works In Channel!")
                return
            if pm_only and chat_type != "private":
                await edit_or_reply(message, "`This Cmd Only Works On PM!`")
                return
            if ignore_errors:
                await func(client, message)
            else:
                try:
                    await func(client, message)
                except StopPropagation:
                    raise StopPropagation
                except KeyboardInterrupt:
                    pass
                except MessageNotModified:
                    pass
                except MessageIdInvalid:
                    logging.warning(
                        "Please Don't Delete Commands While it's Processing.."
                    )
                except UserNotParticipant:
                    pass
                except ContinuePropagation:
                    raise ContinuePropagation
                except BaseException as e:
                    logging.error(
                        f"Exception - {func.__module__} - {func.__name__}"
                    )
                    TZ = pytz.timezone(Config.TZ)
                    datetime_tz = datetime.now(TZ)
                    text = "**!ERROR - REPORT!**\n\n"
                    text += f"\n**Trace Back : ** `{str(format_exc())}`"
                    text += f"\n**Plugin-Name :** `{func.__module__}`"
                    text += f"\n**Function Name :** `{func.__name__}` \n"
                    text += datetime_tz.strftime(
                        "**Date :** `%Y-%m-%d` \n**Time :** `%H:%M:%S`"
                    )
                    text += "\n\n__You can Forward This to @FridayChat, If You Think This is Serious A Error!__"
                    try:
                        await client.send_message(Config.LOG_GRP, text)
                    except BaseException:
                        logging.error(text)
        add_handler(filterm, wrapper, cmd)
        return wrapper

    return decorator


def listen(filter_s):
    """Simple Decorator To Handel Custom Filters"""
    def decorator(func):
        async def wrapper(client, message):
            try:
                await func(client, message)
            except StopPropagation:
                raise StopPropagation
            except ContinuePropagation:
                raise ContinuePropagation
            except UserNotParticipant:
                pass
            except MessageEmpty:
                pass
            except BaseException as e:
                logging.error(f"Exception - {func.__module__} - {func.__name__}")
                TZ = pytz.timezone(Config.TZ)
                datetime_tz = datetime.now(TZ)
                text = "**!ERROR WHILE HANDLING UPDATES!**\n\n"
                text += f"\n**Trace Back : ** `{str(format_exc())}`"
                text += f"\n**Plugin-Name :** `{func.__module__}`"
                text += f"\n**Function Name :** `{func.__name__}` \n"
                text += datetime_tz.strftime(
                    "**Date :** `%Y-%m-%d` \n**Time :** `%H:%M:%S`"
                )
                text += "\n\n__You can Forward This to @FridayChat, If You Think This is A Error!__"
                try:
                    await client.send_message(Config.LOG_GRP, text)
                except BaseException:
                    logging.error(text)
            message.continue_propagation()
        Friday.add_handler(MessageHandler(wrapper, filters=filter_s), group=0)
        if Friday2:
            Friday2.add_handler(MessageHandler(wrapper, filters=filter_s), group=0)
        if Friday3:
            Friday3.add_handler(MessageHandler(wrapper, filters=filter_s), group=0)
        if Friday4:
            Friday4.add_handler(MessageHandler(wrapper, filters=filter_s), group=0)
        return wrapper

    return decorator


def add_help_menu(
    cmd,
    stack,
    is_official=True,
    cmd_help="No One Gonna Help You",
    example="{ch}what",
    file_name=None,
):
    if not file_name:
        previous_stack_frame = stack[1]
        if "xtraplugins" in previous_stack_frame.filename:
            is_official = False
        file_name = os.path.basename(previous_stack_frame.filename.replace(".py", ""))
    cmd_helpz = example.format(ch=Config.COMMAND_HANDLER)
    cmd_helper = f"**Module Name :** `{file_name.replace('_', ' ').title()}` \n\n**Command :** `{Config.COMMAND_HANDLER}{cmd}` \n**Help :** `{cmd_help}` \n**Example :** `{cmd_helpz}`"
    if is_official:
        if file_name not in CMD_LIST.keys():
            CMD_LIST[file_name] = cmd_helper
        else:
            CMD_LIST[
                file_name
            ] += f"\n\n**Command :** `{Config.COMMAND_HANDLER}{cmd}` \n**Help :** `{cmd_help}` \n**Example :** `{cmd_helpz}`"
    else:
        if file_name not in XTRA_CMD_LIST.keys():
            XTRA_CMD_LIST[file_name] = cmd_helper
        else:
            XTRA_CMD_LIST[
                file_name
            ] += f"\n\n**Command :** `{Config.COMMAND_HANDLER}{cmd}` \n**Help :** `{cmd_help}` \n**Example :** `{cmd_helpz}`"
            

def add_handler(filter_s, func_, cmd):
    d_c_l = Config.DISABLED_SUDO_CMD_S
    if d_c_l:
        d_c_l = d_c_l.split(" ")
        d_c_l = list(d_c_l)
        if "dev" in d_c_l:
            d_c_l.extend(['eval', 'bash', 'install']) 
        if any(item in list(d_c_l) for item in list(cmd)): 
            filter_s = (filters.me & filters.command(cmd, Config.COMMAND_HANDLER) & ~filters.via_bot & ~filters.forwarded)
    Friday.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if Friday2:
        Friday2.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if Friday3:
        Friday3.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if Friday4:
        Friday4.add_handler(MessageHandler(func_, filters=filter_s), group=0)      
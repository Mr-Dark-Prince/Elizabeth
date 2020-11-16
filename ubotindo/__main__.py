import importlib, traceback, html, json
import re
import time
import subprocess
from typing import Optional, List

from telegram import Message, Chat, User
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async, DispatcherHandlerStop
from telegram.utils.helpers import escape_markdown
from Shoko.modules.helper_funcs.admin_rights import user_can_ban
from Shoko.modules.helper_funcs.readable_time import get_readable_time

from Shoko import (
    dispatcher,
    since_time_start,
    updater,
    TOKEN,
    OWNER_ID,
    WEBHOOK,
    CERT_PATH,
    PORT,
    URL,
    LOGGER,
    BLACKLIST_CHATS,
    WHITELIST_CHATS,
)

# needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!
from Shoko.modules import ALL_MODULES
from Shoko.modules.purge import client
from Shoko.modules.helper_funcs.chat_status import is_user_admin
from Shoko.modules.helper_funcs.misc import paginate_modules
from Shoko.modules.helper_funcs.alternate import typing_action


PM_START_TEXT = f"""
Hey there! my name is *{dispatcher.bot.first_name}*. If you have any questions on how to use me, Click Help button.

I'm here to make your group management fun and easy!
i have lots of handy features, such as flood control, a warning system, a note keeping system, and even replies on predetermined filters.

Any issues or need help related to me? join our group [Shoko support chat](https://t.me/Shokosupport).

Wanna Add me to your Group? Just click the button below!
"""

buttons = [
    [
        InlineKeyboardButton(
        text="Help & Commands ❔", callback_data="help_back"
        ),
        InlineKeyboardButton(
        text="About", callback_data="aboutmanu_"
        ),
    ]
    
]

buttons += [
    [
        InlineKeyboardButton(
            text="Add to Group 👥", url="t.me/zoldycktmbot?startgroup=true"
        ),
       
    ]
]


HELP_STRINGS = f"""
Hello there! My name is *{dispatcher.bot.first_name}*.
I'm a modular group management bot with a few fun extras! Have a look at the following for an idea of some of \
the things I can help you with.

*Main* commands available:
 /start: Starts me, can be used to check i'm alive or no...
 /help: PM's you this message.
 /help <module name>: PM's you info about that module.
 /settings: in PM: will send you your settings for all supported modules.
   - in a group: will redirect you to pm, with all that chat's settings.
 \nClick on the buttons below to get documentation about specific modules!"""


IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []

CHAT_SETTINGS = {}
USER_SETTINGS = {}

GDPR = []

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("Shoko.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if not imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__gdpr__"):
        GDPR.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


    
# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard
    )


@run_async
def test(update, context):
    try:
        print(update)
    except:
        pass
    update.effective_message.reply_text(
        "Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN
    )
    update.effective_message.reply_text("This person edited a message")
    print(update.effective_message)


@run_async
@typing_action
def start(update, context):
    if update.effective_chat.type == "private":
        args = context.args
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            update.effective_message.reply_text(
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=True,
            )
    else:
        update.effective_message.reply_text(
            text="hey there! Shoko is alive :3"
                 "\n_Click the button below to know the current ping!_",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                  [
                    InlineKeyboardButton(text="Ping ⁉️", callback_data="start_ping")
                  ],
                
                ]
            ),
        )

def start_p(update, context):
    query = update.callback_query
    if query.data == "start_ping":
        shoko_rbot = get_readable_time((time.time() - since_time_start))
        context.bot.answer_callback_query(query.id,
                                          text=f"Shoko is running since: {shoko_rbot}"
                                               f"\n\nTelegram ping: {ping()}",
                                          show_alert=True)
            

def ping(server='google.com', count=1, wait_sec=1):
   
    cmd = "ping -c {} -W {} {}".format(count, wait_sec, server).split(' ')
    try:
        output = subprocess.check_output(cmd).decode().strip()
        lines = output.split("\n")
        total = lines[-2].split(',')[3].split()[1]
        loss = lines[-2].split(',')[2].split()[0]
        timing = lines[-1].split()[3].split('/')
        ping_t = f"\nmin: {timing[0]}" \
                 f"\navg: {timing[1]}" \
                 f"\nmax: {timing[2]}" \
                 f"\ntotal: {total}" \
                 f"\nloss: {loss}" 
                 
                 
        return ping_t
   
    except Exception as e:
        print(e)
        return None
        
def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


@run_async
def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "Here is the help for the *{}* module:\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="Back", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.reply_text(
                HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.reply_text(
                HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.reply_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        # ensure no spinny white circle
        query.message.delete()
        context.bot.answer_callback_query(query.id)
    except Exception as excp:
        if excp.message == "Message is not modified":
            pass
        elif excp.message == "Query_id_invalid":
            pass
        elif excp.message == "Message can't be deleted":
            pass
        else:
            query.message.edit_text(excp.message)
            LOGGER.exception("Exception in help buttons. %s", str(query.data))

@run_async
def Shoko_about_callback(update, context):
    query = update.callback_query
    if query.data == "aboutmanu_":
        query.message.edit_text(
            text="*Shoko is a bot for managing your group with additional features,*"
                 "\nand is fork of [marie](https://github.com/PaulSonOfLars/tgbot)."
                 "\n\n_Shoko's licensed under the GNU General Public License v3.0_,"
                 "\nhere is the [repository](https://github.com/gizmostuffin/Shoko)."
                 "\n\nIf any question about Shoko, let us know at @Shokosupport.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                  [
                    InlineKeyboardButton(text="How to use ❓", callback_data="aboutmanu_howto"),
                    InlineKeyboardButton(text="Terms and Conditions", callback_data="aboutmanu_tac")
                  ],
                 [
                    InlineKeyboardButton(text="Back", callback_data="aboutmanu_back")
                 ]
                ]
            ),
        )
    elif query.data == "aboutmanu_back":
        query.message.edit_text(
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=True,
            )
        
    elif query.data == "aboutmanu_howto":
        query.message.edit_text(
            text="*Basic help:*"
                 "\nTo add Shoko to your chats, simply click [here](http://t.me/zoldycktmbot?startgroup=true)  and select your chat."
                 "\nYou can also click on @zoldycktmbot, and go to the three dots on the top right of your screen, and select 'add to group'."
                 "",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(text="Admins Permissions", callback_data="aboutmanu_permis"),
                InlineKeyboardButton(text="Anti-spam settings", callback_data="aboutmanu_spamprot")],
                [
                InlineKeyboardButton(text="Back", callback_data="aboutmanu_")]
                                               ]),
        )
    elif query.data == "aboutmanu_permis":
        query.message.edit_text(
            text="<b>Admin permissions:</b>"
                 "\nTo avoid slowing down, Shoko caches admin rights for each user. This cache lasts about 10 minutes; this may change in the future. This means that if you promote a user manually (without using the /promote command), Shoko will only find out ~10 minutes later."
                 "\n\nIf you are getting a message saying:"
                 "\n<Code>You must be this chat administrator to perform this action!</code>"
                 "\nThis has nothing to do with Shoko's rights; this is all about YOUR permissions as an admin. Shoko respects admin permissions; if you do not have the Ban Users permission as a telegram admin, you won't be able to ban users with Shoko. Similarly, to change Shoko settings, you need to have the Change group info permission."
                 "\n\nThe message very clearly says that you need these rights - <i>not</i> Shoko.",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Back", callback_data="aboutmanu_howto")]]),
        )
    elif query.data == "aboutmanu_spamprot":
        query.message.edit_text(
            text="*Anti-spam settings:*"
                 "\n- /antispam <on/off/yes/no>: Change antispam security settings in the group, or return your current settings(when no arguments)."
                 "\n_This helps protect you and your groups by removing spam flooders as quickly as possible._"
                 "\n\n- /setflood <int/'no'/'off'>: enables or disables flood control"
                 "\n- /setfloodmode <ban/kick/mute/tban/tmute> <value>: Action to perform when user have exceeded flood limit. ban/kick/mute/tmute/tban"
                 "\n_Antiflood allows you to take action on users that send more than x messages in a row. Exceeding the set flood will result in restricting that user._"
                 "\n\n- /addblacklist <triggers>: Add a trigger to the blacklist. Each line is considered one trigger, so using different lines will allow you to add multiple triggers."
                 "\n- /blacklistmode <off/del/warn/ban/kick/mute/tban/tmute>: Action to perform when someone sends blacklisted words."
                 "\n_Blacklists are used to stop certain triggers from being said in a group. Any time the trigger is mentioned, the message will immediately be deleted. A good combo is sometimes to pair this up with warn filters!_"
                 "\n\n- /reports <on/off>: Change report setting, or view current status."
                 "\n • If done in pm, toggles your status."
                 "\n • If in chat, toggles that chat's status."
                 "\n_If someone in your group thinks someone needs reporting, they now have an easy way to call all admins._"
                 "\n\n- /lock <type>: Lock items of a certain type (not available in private)"
                 "\n- /locktypes: Lists all possible locktypes"
                 "\n_The locks module allows you to lock away some common items in the telegram world; the bot will automatically delete them!_"
                 "\n\n- /addwarn <keyword> <reply message>: Sets a warning filter on a certain keyword. If you want your keyword to be a sentence, encompass it with quotes, as such: /addwarn \"very angry\" This is an angry user. "
                 "\n- /warn <userhandle>: Warns a user. After 3 warns, the user will be banned from the group. Can also be used as a reply."
                 "\n- /strongwarn <on/yes/off/no>: If set to on, exceeding the warn limit will result in a ban. Else, will just kick."
                 "\n_If you're looking for a way to automatically warn users when they say certain things, use the /addwarn command._"
                 "\n\n- /welcomemute <off/soft/strong>: All users that join, get muted"
                 "\n_ A button gets added to the welcome message for them to unmute themselves. This proves they aren't a bot! soft - restricts users ability to post media for 24 hours. strong - mutes on join until they prove they're not bots._",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Back", callback_data="aboutmanu_howto")]]),
        )
    elif query.data == "aboutmanu_tac":
        query.message.edit_text(
            text="<b>Terms and Conditions:</b>"
                 "\nTo use this bot, you need to read Terms and Conditions"
                 "\n- Watch your group, if someone spamming your group, you can use report feature from your Telegram Client."
                 "\n- Make sure antiflood is enabled, so nobody can ruin your group."
                 "\n- Do not spam commands, buttons, or anything in bot PM, else you will be Gbanned."
                 "\n- If you need to ask anything about this bot, Go @Shokosupport."
                 "\n- If you asking nonsense in @Shokosupport, you will get banned."
                 "\n- Sharing any files/videos others than about bot in @Shokosupport is prohibited."
                 "\n- Sharing NSFW in @Shokosupport will reward you banned/gbanned and reported to Telegram as well."
                 "\n\nFor any kind of help, related to this bot, Join @ShokoSupport."
                 "\n\n<i>Terms and Conditions will be changed anytime</i>"
                 "\nFollow @ShokoTM for Updates."
                 "\nFollow @spookyanii to get info about bots.",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Back", callback_data="aboutmanu_")]]),
        )
        
@run_async
@typing_action
def get_help(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:

        update.effective_message.reply_text(
            "Click the button below to get help manu in your pm.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Open in Private chat",
                            callback_data="gethelp_pr",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Support chat",
                            url="https://t.me/Shokosupport",
                        )
                    ]
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Back", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)

def gethelp(update, context):
    query = update.callback_query
    if query.data == "gethelp_pr":
        query.bot.send_message(
                    query.from_user.id,
                    text=HELP_STRINGS,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(
                        paginate_modules(0, HELPABLE, "help")
                    ),
                )
        query.message.edit_text(
            text="<i>I have sent you the requested information in a private message.</i>",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Go to the chat",
                            url=f"telegram.me/{context.bot.username}",
                            
                        )
                    ],
                    
                ]
            ),
        )
    
    
        
        

def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Which module would you like to check {}'s settings for?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any chat settings available :'(\nSend this "
                "in a group chat you're admin in to find its current settings!",
                parse_mode=ParseMode.MARKDOWN,
            )


@run_async
def settings_button(update, context):
    query = update.callback_query
    user = update.effective_user
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = context.bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Back",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = context.bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = context.bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = context.bot.get_chat(chat_id)
            query.message.reply_text(
                text="Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        query.message.delete()
        context.bot.answer_callback_query(query.id)
    except Exception as excp:
        if excp.message == "Message is not modified":
            pass
        elif excp.message == "Query_id_invalid":
            pass
        elif excp.message == "Message can't be deleted":
            pass
        else:
            query.message.edit_text(excp.message)
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))


@run_async
@typing_action
def get_settings(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]
    args = msg.text.split(None, 1)

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "Click here to get this chat's settings, as well as yours."
            msg.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Settings",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "Click here to check your settings."

    else:
        send_settings(chat.id, user.id, True)


def migrate_chats(update, context):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop


def is_chat_allowed(update, context):
    if len(WHITELIST_CHATS) != 0:
        chat_id = update.effective_message.chat_id
        if chat_id not in WHITELIST_CHATS:
            context.bot.send_message(
                chat_id=update.message.chat_id, text="Unallowed chat! Leaving..."
            )
            try:
                context.bot.leave_chat(chat_id)
            finally:
                raise DispatcherHandlerStop
    if len(BLACKLIST_CHATS) != 0:
        chat_id = update.effective_message.chat_id
        if chat_id in BLACKLIST_CHATS:
            context.bot.send_message(
                chat_id=update.message.chat_id, text="Unallowed chat! Leaving..."
            )
            try:
                context.bot.leave_chat(chat_id)
            finally:
                raise DispatcherHandlerStop
    if len(WHITELIST_CHATS) != 0 and len(BLACKLIST_CHATS) != 0:
        chat_id = update.effective_message.chat_id
        if chat_id in BLACKLIST_CHATS:
            context.bot.send_message(
                chat_id=update.message.chat_id, text="Unallowed chat, leaving"
            )
            try:
                context.bot.leave_chat(chat_id)
            finally:
                raise DispatcherHandlerStop
    else:
        pass


def main():
    # test_handler = CommandHandler("test", test)
    start_handler = CommandHandler("start", start, pass_args=True)
    start_p_handler = CallbackQueryHandler(start_p, pattern=r"start_")

    help_handler = CommandHandler("help", get_help)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_")
    
    gethelp_callback_handler = CallbackQueryHandler(gethelp, pattern=r"gethelp_")
    
    settings_handler = CommandHandler("settings", get_settings)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_")

    about_callback_handler = CallbackQueryHandler(Shoko_about_callback, pattern=r"aboutmanu_")
    
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)
    is_chat_allowed_handler = MessageHandler(Filters.group, is_chat_allowed)

    # dispatcher.add_handler(test_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(start_p_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(gethelp_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(is_chat_allowed_handler)

    dispatcher.add_error_handler(error_handler)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN, certificate=open(CERT_PATH, "rb"))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)
            client.run_until_disconnected()

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4)
        client.run_until_disconnected()

    updater.idle()



if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    client.start(bot_token=TOKEN)
    main()

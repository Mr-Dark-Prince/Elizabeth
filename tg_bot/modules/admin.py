import html
from typing import Optional, List

from telegram import Message, Chat, Update, Bot, User
from telegram import ParseMode
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters, RegexHandler
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import escape_markdown, mention_html

from tg_bot import dispatcher
import tg_bot.modules.sql.setlink_sql as sql
from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot.modules.helper_funcs.chat_status import bot_admin, can_promote, user_admin, can_pin
from tg_bot.modules.helper_funcs.extraction import extract_user
from tg_bot.modules.helper_funcs.string_handling import markdown_parser
from tg_bot.modules.log_channel import loggable


@run_async
@bot_admin
@can_promote
@user_admin
@loggable
def promote(bot: Bot, update: Update, args: List[str]) -> str:
    chat_id = update.effective_chat.id
    message = update.effective_message  # type: Optional[Message]
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text("മെസ്സേജിന് മറുപടിയായി മാത്രം കമാൻഡ് നൽകുക!.")
        return ""

    user_member = chat.get_member(user_id)
    if user_member.status == 'administrator' or user_member.status == 'creator':
        message.reply_text("അഡ്മിനായ ഒരാളെ വീണ്ടും എങ്ങനെ അഡ്മിൻ ആക്കും?")
        return ""

    if user_id == bot.id:
        message.reply_text("ഞാൻ എന്നെത്തന്നെ അഡ്മിൻ ആക്കുവാനോ.. നടക്കില്ല കേട്ടോ!.")
        return ""

    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = chat.get_member(bot.id)

    bot.promoteChatMember(chat_id, user_id,
                          can_change_info=bot_member.can_change_info,
                          can_post_messages=bot_member.can_post_messages,
                          can_edit_messages=bot_member.can_edit_messages,
                          can_delete_messages=bot_member.can_delete_messages,
                          # can_invite_users=bot_member.can_invite_users,
                          can_restrict_members=bot_member.can_restrict_members,
                          can_pin_messages=bot_member.can_pin_messages,
                          can_promote_members=bot_member.can_promote_members)

    message.reply_text("അഡ്മിൻ ആക്കിയിട്ടുണ്ട് 👍!")
    return "<b>{}:</b>" \
           "\n#PROMOTED" \
           "\n<b>Admin:</b> {}" \
           "\n<b>User:</b> {}".format(html.escape(chat.title),
                                      mention_html(user.id, user.first_name),
                                      mention_html(user_member.user.id, user_member.user.first_name))


@run_async
@bot_admin
@can_promote
@user_admin
@loggable
def demote(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    message = update.effective_message  # type: Optional[Message]
    user = update.effective_user  # type: Optional[User]

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text("You don't seem to be referring to a user.")
        return ""

    user_member = chat.get_member(user_id)
    if user_member.status == 'creator':
        message.reply_text("This person CREATED the chat, how would I demote them?")
        return ""

    if not user_member.status == 'administrator':
        message.reply_text("Can't demote what wasn't promoted!")
        return ""

    if user_id == bot.id:
        message.reply_text("I can't demote myself! Get an admin to do it for me.")
        return ""

    try:
        bot.promoteChatMember(int(chat.id), int(user_id),
                              can_change_info=False,
                              can_post_messages=False,
                              can_edit_messages=False,
                              can_delete_messages=False,
                              can_invite_users=False,
                              can_restrict_members=False,
                              can_pin_messages=False,
                              can_promote_members=False)
        message.reply_text("Successfully demoted!")
        return "<b>{}:</b>" \
               "\n#DEMOTED" \
               "\n<b>Admin:</b> {}" \
               "\n<b>User:</b> {}".format(html.escape(chat.title),
                                          mention_html(user.id, user.first_name),
                                          mention_html(user_member.user.id, user_member.user.first_name))

    except BadRequest:
        message.reply_text("Could not demote. I might not be admin, or the admin status was appointed by another "
                           "user, so I can't act upon them!")
        return ""


@run_async
@bot_admin
@can_pin
@user_admin
@loggable
def pin(bot: Bot, update: Update, args: List[str]) -> str:
    user = update.effective_user  # type: Optional[User]
    chat = update.effective_chat  # type: Optional[Chat]

    is_group = chat.type != "private" and chat.type != "channel"

    prev_message = update.effective_message.reply_to_message

    is_silent = True
    if len(args) >= 1:
        is_silent = not (args[0].lower() == 'notify' or args[0].lower() == 'loud' or args[0].lower() == 'violent')

    if prev_message and is_group:
        try:
            bot.pinChatMessage(chat.id, prev_message.message_id, disable_notification=is_silent)
        except BadRequest as excp:
            if excp.message == "Chat_not_modified":
                pass
            else:
                raise
        return "<b>{}:</b>" \
               "\n#PINNED" \
               "\n<b>Admin:</b> {}".format(html.escape(chat.title), mention_html(user.id, user.first_name))

    return ""


@run_async
@bot_admin
@can_pin
@user_admin
@loggable
def unpin(bot: Bot, update: Update) -> str:
    chat = update.effective_chat
    user = update.effective_user  # type: Optional[User]

    try:
        bot.unpinChatMessage(chat.id)
    except BadRequest as excp:
        if excp.message == "Chat_not_modified":
            pass
        else:
            raise

    return "<b>{}:</b>" \
           "\n#UNPINNED" \
           "\n<b>Admin:</b> {}".format(html.escape(chat.title),
                                       mention_html(user.id, user.first_name))

@run_async
@bot_admin
@user_admin
def invite(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    message = update.effective_message #type: Optional[Messages]
    
    if chat.username:
        update.effective_message.reply_text("@{}".format(chat.username))
    elif chat.type == chat.SUPERGROUP or chat.type == chat.CHANNEL:
        bot_member = chat.get_member(bot.id)
        if bot_member.can_invite_users:
            invitelink = bot.exportChatInviteLink(chat.id)
            linktext = "Successfully generated new link for *{}:*".format(chat.title)
            link = "`{}`".format(invitelink)
            message.reply_text(linktext, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
            message.reply_text(link, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        else:
            message.reply_text("I don't have access to the invite link, try changing my permissions!")
    else:
        message.reply_text("I can only give you invite links for supergroups and channels, sorry!")

@run_async
def link_public(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    message = update.effective_message #type: Optional[Messages]
    chat_id = update.effective_chat.id
    invitelink = sql.get_link(chat_id)
    
    if chat.type == chat.SUPERGROUP or chat.type == chat.CHANNEL:
        if invitelink:
            message.reply_text("Link of *{}*:\n`{}`".format(chat.title, invitelink), parse_mode=ParseMode.MARKDOWN)
        else:
            message.reply_text("The admins of *{}* haven't set link."
                               " \nLink can be set by following: `/setlink` and get link of chat "
                               "using /invitelink, paste the link after `/setlink` append.".format(chat.title), parse_mode=ParseMode.MARKDOWN)
    else:
        message.reply_text("I can only can save links for supergroups and channels, sorry!")

@run_async
@user_admin
def set_link(bot: Bot, update: Update):
    chat_id = update.effective_chat.id
    msg = update.effective_message  # type: Optional[Message]
    chat = update.effective_chat  # type: Optional[Chat]
    raw_text = msg.text
    args = raw_text.split(None, 1)  # use python's maxsplit to separate cmd and args
    
    if len(args) == 2:
        links_text = args[1]

        sql.set_link(chat_id, links_text)
        msg.reply_text("The link has been set for {}!\nRetrieve link by #link".format((chat.title)))


@run_async
@user_admin
def clear_link(bot: Bot, update: Update):
    chat_id = update.effective_chat.id
    sql.set_link(chat_id, "")
    update.effective_message.reply_text("Successfully cleared link!")


@run_async
def adminlist(bot: Bot, update: Update):
    administrators = update.effective_chat.get_administrators()
    text = "Admins in *{}*:".format(update.effective_chat.title or "this chat")
    for admin in administrators:
        user = admin.user
        name = "[{}](tg://user?id={})".format(user.first_name + (user.last_name or ""), user.id)
        if user.username:
            name = escape_markdown("@" + user.username)
        text += "\n - {}".format(name)

    update.effective_message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

def __stats__():
    return "{} chats have links set.".format(sql.num_chats())

def __chat_settings__(chat_id, user_id):
    return "You are *admin*: `{}`".format(
        dispatcher.bot.get_chat_member(chat_id, user_id).status in ("administrator", "creator"))


__help__ = """
*അഡ്മിൻ ക്രമീകരണം* ⚙️

 ➩ /adminlist: ഗ്രൂപ്പിൽ ഉള്ള അഡ്മിൻസിന്റെ ലിസ്റ്റ് ലഭിക്കുന്നു.
 ➩ /link: നിലവിലെ ഗ്രൂപ്പ്‌ ലിങ്ക് ലഭിക്കുന്നു.

*അഡ്മിൻ മാത്രം:*
 ➩ /pin: ഒരു സന്ദേശം ഗ്രൂപ്പിന് മുകളിൽ പിൻ ചെയ്യുന്നു.
 ➩ /unpin: നിലവിൽ പിൻ ചെയ്തിരിക്കുന്ന സന്ദേശം ഒഴിവാക്കുന്നു.
 ➩ /invitelink: ഗ്രൂപ്പിന്റെ ഇൻവിറ്റേഷൻ ലിങ്ക് ജെനറേറ്റ് ചെയ്യുന്നു.
 ➩ /setlink <ഗ്രൂപ്പ്‌ ലിങ്ക്>: ഗ്രൂപ്പ്‌ ലിങ്ക് സെറ്റ് ചെയ്യുന്നു.
 ➩ /clearlink: സെറ്റ് ചെയ്ത ഗ്രൂപ്പ്‌ ലിങ്ക് ഒഴിവാക്കുന്നു.
 ➩ /promote: ഒരു ഗ്രൂപ്പ്‌ മെമ്പറുടെ മെസ്സേജ്ന് മറുപടിയായി ഈ കമാൻഡ് നൽകിയാൽ അയാളെ ഗ്രൂപ്പ്‌ അഡ്മിൻ ആക്കുന്നു.
 ➩ /demote: ഒരു ഗ്രൂപ്പ്‌ അഡ്മിന്റെ മെസ്സേജ്ന് മറുപടിയായി ഈ കമാൻഡ് നൽകിയാൽ അയാളെ അഡ്മിൻ സ്ഥാനത്തു നിന്ന് നീക്കം ചെയ്യുന്നു.
 
➩ ഗ്രൂപ്പ്‌ ലിങ്ക് സെറ്റ് ചെയ്യുന്നതിന് ഒരു ഉദാഹരണം:
`/setlink https://t.me/joinchat/HwiIk1RADK5gRMr9FBdOrwtae`

➩ യൂസർനൈം ഉപയോഗിച്ച് ഒരു ഗ്രൂപ്പ്‌ മെമ്പറെ അഡ്മിൻ ആക്കുന്നതിന് ഒരു ഉദാഹരണം:
`/promote @username`; മെൻഷൻ ചെയ്ത മെമ്പറെ അഡ്മിൻ ആക്കുന്നു.
"""

__mod_name__ = "അഡ്മിൻ"

PIN_HANDLER = CommandHandler("pin", pin, pass_args=True, filters=Filters.group)
UNPIN_HANDLER = CommandHandler("unpin", unpin, filters=Filters.group)
LINK_HANDLER = DisableAbleCommandHandler("link", link_public)
SET_LINK_HANDLER = CommandHandler("setlink", set_link, filters=Filters.group)
RESET_LINK_HANDLER = CommandHandler("clearlink", clear_link, filters=Filters.group)
HASH_LINK_HANDLER = RegexHandler("#link", link_public)
INVITE_HANDLER = CommandHandler("invitelink", invite, filters=Filters.group)
PROMOTE_HANDLER = CommandHandler("promote", promote, pass_args=True, filters=Filters.group)
DEMOTE_HANDLER = CommandHandler("demote", demote, pass_args=True, filters=Filters.group)
ADMINLIST_HANDLER = DisableAbleCommandHandler(["adminlist", "staff"], adminlist, filters=Filters.group)

dispatcher.add_handler(PIN_HANDLER)
dispatcher.add_handler(UNPIN_HANDLER)
dispatcher.add_handler(INVITE_HANDLER)
dispatcher.add_handler(LINK_HANDLER)
dispatcher.add_handler(SET_LINK_HANDLER)
dispatcher.add_handler(RESET_LINK_HANDLER)
dispatcher.add_handler(HASH_LINK_HANDLER)
dispatcher.add_handler(PROMOTE_HANDLER)
dispatcher.add_handler(DEMOTE_HANDLER)
dispatcher.add_handler(ADMINLIST_HANDLER)

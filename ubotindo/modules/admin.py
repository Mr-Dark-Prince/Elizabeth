import html
import os

from telegram import ParseMode
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters, MessageHandler
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import mention_html

from ubotindo import dispatcher
from ubotindo.modules.connection import connected
from ubotindo.modules.disable import DisableAbleCommandHandler
from ubotindo.modules.helper_funcs.admin_rights import (
    user_can_changeinfo,
    user_can_pin,
    user_can_promote,
)
from ubotindo.modules.helper_funcs.alternate import typing_action
from ubotindo.modules.helper_funcs.chat_status import (
    bot_admin,
    can_pin,
    can_promote,
    user_admin,
)
from ubotindo.modules.helper_funcs.extraction import extract_user, extract_user_and_text
from ubotindo.modules.log_channel import loggable
from ubotindo.modules.sql import admin_sql as sql


@run_async
@bot_admin
@can_promote
@user_admin
@loggable
@typing_action
def promote(update, context):
    chat_id = update.effective_chat.id
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    args = context.args

    if user_can_promote(chat, user, context.bot.id) is False:
        message.reply_text("⚠️ക്ഷമിക്കണം..ആരെയും അഡ്മിൻ ആക്കുവാനുള്ള അധികാരം നിങ്ങൾക്ക് ഇല്ല..!")
        return ""

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text("ആരെയാണ് അഡ്മിൻ ആക്കേണ്ടത്?🤔")
        return ""

    user_member = chat.get_member(user_id)
    if user_member.status == "administrator" or user_member.status == "creator":
        message.reply_text("🙄 ആൾറെഡി അഡ്മിൻ ആണ്..!")
        return ""

    if user_id == context.bot.id:
        message.reply_text("🙄ഞാൻ എന്നെത്തന്നെ അഡ്മിൻ ആക്കുവാനോ?!")
        return ""

    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = chat.get_member(context.bot.id)

    context.bot.promoteChatMember(
        chat_id,
        user_id,
        can_change_info=bot_member.can_change_info,
        can_post_messages=bot_member.can_post_messages,
        can_edit_messages=bot_member.can_edit_messages,
        can_delete_messages=bot_member.can_delete_messages,
        can_invite_users=bot_member.can_invite_users,
        can_restrict_members=bot_member.can_restrict_members,
        can_pin_messages=bot_member.can_pin_messages,
    )

    message.reply_text("👍അഡ്മിൻ ആക്കിയിട്ടുണ്ട്...")
    return (
        "<b>{}:</b>"
        "\n#PROMOTED"
        "\n<b>Admin:</b> {}"
        "\n<b>User:</b> {}".format(
            html.escape(chat.title),
            mention_html(user.id, user.first_name),
            mention_html(user_member.user.id, user_member.user.first_name),
        )
    )


@run_async
@bot_admin
@can_promote
@user_admin
@loggable
@typing_action
def demote(update, context):
    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user
    args = context.args

    if user_can_promote(chat, user, context.bot.id) is False:
        message.reply_text("⚠️ നിങ്ങൾക്ക് അതിനുള്ള പെർമിഷൻ ഇല്ല..!")
        return ""

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text("🙄എന്തോന്നെടെ?.")
        return ""

    user_member = chat.get_member(user_id)
    if user_member.status == "creator":
        message.reply_text("ഗ്രൂപ്പ്‌ മുതലാളിയെ എങ്ങനെ അഡ്മിൻ സ്ഥാനത്ത് നിന്ന് മാറ്റും..😡")
        return ""

    if not user_member.status == "administrator":
        message.reply_text(
            "എടെ മണ്ണുണ്ണി..അഡ്മിൻ അല്ലാത്ത ഒരാളെ എങ്ങനെ അഡ്മിൻ അല്ലാതാക്കും..മണ്ടൻ ആണോ നീ..👻!"
        )
        return ""

    if user_id == context.bot.id:
        message.reply_text("😜 ഇല്ല...ഒരിക്കലും ഞാൻ ചെയ്യില്ല..!")
        return ""

    try:
        context.bot.promoteChatMember(
            int(chat.id),
            int(user_id),
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
        )
        message.reply_text("😁 അഡ്മിൻ സ്ഥാനത്തു നിന്ന് ഒഴിവാക്കിയിട്ടുണ്ട്!")
        return (
            "<b>{}:</b>"
            "\n#DEMOTED"
            "\n<b>Admin:</b> {}"
            "\n<b>User:</b> {}".format(
                html.escape(chat.title),
                mention_html(user.id, user.first_name),
                mention_html(user_member.user.id, user_member.user.first_name),
            )
        )

    except BadRequest:
        message.reply_text(
            "ഹായ് മണ്ണുണ്ണി... ഞാൻ അഡ്മിൻ അല്ലാതിരിക്കുകയോ , അല്ലെങ്കിൽ അയാളെ അഡ്മിൻ ആക്കിയത് വേറെ ആരെങ്കിലും ആയിരിക്കുകയോ "
            "ചെയ്താൽ എനിക്ക് ഒന്നും ചെയ്യാൻ പറ്റില്ല 😑!")
        return ""


@run_async
@bot_admin
@can_pin
@user_admin
@loggable
@typing_action
def pin(update, context):
    args = context.args
    user = update.effective_user
    chat = update.effective_chat
    message = update.effective_message

    is_group = chat.type != "private" and chat.type != "channel"

    prev_message = update.effective_message.reply_to_message

    if user_can_pin(chat, user, context.bot.id) is False:
        message.reply_text("⚠️ താങ്കൾക്ക് മെസ്സേജ് പിൻ ചെയ്യുന്നതിനുള്ള അധികാരമില്ല.. !")
        return ""

    is_silent = True
    if len(args) >= 1:
        is_silent = not (
            args[0].lower() == "notify"
            or args[0].lower() == "loud"
            or args[0].lower() == "violent"
        )

    if prev_message and is_group:
        try:
            context.bot.pinChatMessage(
                chat.id,
                prev_message.message_id,
                disable_notification=is_silent)
        except BadRequest as excp:
            if excp.message == "Chat_not_modified":
                pass
            else:
                raise
        return (
            "<b>{}:</b>"
            "\n#PINNED"
            "\n<b>Admin:</b> {}".format(
                html.escape(chat.title), mention_html(user.id, user.first_name)
            )
        )

    return ""


@run_async
@bot_admin
@can_pin
@user_admin
@loggable
@typing_action
def unpin(update, context):
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    if user_can_pin(chat, user, context.bot.id) is False:
        message.reply_text("⚠️ താങ്കൾക്ക് മെസ്സേജ് അൺപിൻ ചെയ്യുന്നതിനുള്ള അധികാരമില്ല !")
        return ""

    try:
        context.bot.unpinChatMessage(chat.id)
    except BadRequest as excp:
        if excp.message == "Chat_not_modified":
            pass
        else:
            raise

    return (
        "<b>{}:</b>"
        "\n#UNPINNED"
        "\n<b>Admin:</b> {}".format(
            html.escape(chat.title), mention_html(user.id, user.first_name)
        )
    )


@run_async
@bot_admin
@user_admin
@typing_action
def invite(update, context):
    user = update.effective_user
    msg = update.effective_message
    chat = update.effective_chat
    context.args

    conn = connected(context.bot, update, chat, user.id, need_admin=True)
    if conn:
        chat = dispatcher.bot.getChat(conn)
    else:
        if msg.chat.type == "private":
            msg.reply_text("ഈ കമാൻഡ് ഉപയോഗിക്കേണ്ടത് ഇവിടെ അല്ല.. ഗ്രൂപ്പിൽ ആണ്..")
            return ""
        chat = update.effective_chat

    if chat.username:
        msg.reply_text(chat.username)
    elif chat.type == chat.SUPERGROUP or chat.type == chat.CHANNEL:
        bot_member = chat.get_member(context.bot.id)
        if bot_member.can_invite_users:
            invitelink = context.bot.exportChatInviteLink(chat.id)
            msg.reply_text(invitelink)
        else:
            msg.reply_text(
                "എനിക്ക് ലിങ്ക് എടുക്കുവാനുള്ള അധികാരം ഇല്ല 😒!"
            )
    else:
        msg.reply_text(
            "സോറി.. ലിങ്ക് തരണമെങ്കിൽ ഒന്നുകിൽ സൂപ്പർ ഗ്രൂപ്പ്‌ ആയിരിക്കണം..അല്ലെങ്കിൽ ചാനൽ ആയിരിക്കണം..!"
        )


@run_async
@typing_action
def adminlist(update, context):
    administrators = update.effective_chat.get_administrators()
    text = "💡അഡ്മിൻസ് in <b>{}</b>:".format(
        update.effective_chat.title or "this chat")
    for admin in administrators:
        user = admin.user
        status = admin.status
        name = f"{(mention_html(user.id, user.first_name))}"
        if status == "creator":
            text += "\n 🌳 ഉടമസ്ഥൻ 🔥:"
            text += "\n • {} \n\n 🌱 മറ്റുള്ള അഡ്മിൻസ്:".format(name)
    for admin in administrators:
        user = admin.user
        status = admin.status
        name = f"{(mention_html(user.id, user.first_name))}"
        if status == "administrator":
            text += "\n • {}".format(name)
    update.effective_message.reply_text(text, parse_mode=ParseMode.HTML)


@run_async
@bot_admin
@can_promote
@user_admin
@typing_action
def set_title(update, context):
    args = context.args
    chat = update.effective_chat
    message = update.effective_message

    user_id, title = extract_user_and_text(message, args)
    try:
        user_member = chat.get_member(user_id)
    except Exception:
        return

    if not user_id:
        message.reply_text("ഒരാളെ സൂചിപ്പിച്ചു കമാൻഡ് നൽകുക.")
        return

    if user_member.status == "creator":
        message.reply_text(
            "ഗ്രൂപ്പ്‌ ഓണറുടെ അഡ്മിൻ ടൈറ്റിൽ മാറ്റുവാൻ എനിക്ക് സാധിക്കില്ല.."
        )
        return

    if not user_member.status == "administrator":
        message.reply_text(
            "അഡ്മിൻ അല്ലാത്ത ഒരാളിന് അഡ്മിൻ ടൈറ്റിൽ കൊടുക്കാൻ കഴിയില്ല മണ്ണുണ്ണി..!"
        )
        return

    if user_id == context.bot.id:
        message.reply_text(
            "എനിക്ക് എന്റെ തന്നെ അഡ്മിൻ ടൈറ്റിൽ ചേഞ്ച്‌ ചെയ്യാൻ സാധിക്കില്ല.."
        )
        return

    if not title:
        message.reply_text("എന്ത് ഉണ്ടയാണ് അഡ്മിൻ ടൈറ്റിൽ ആയി കൊടുക്കേണ്ടത് 😡!")
        return

    if len(title) > 16:
        message.reply_text(
            "ഇത്രയും നീളമുള്ള ടെക്സ്റ്റ്‌ അഡ്മിൻ ടൈറ്റിൽ ആയി നൽകാൻ സാധിക്കില്ല.."
        )

    try:
        context.bot.set_chat_administrator_custom_title(
            chat.id, user_id, title)
        message.reply_text(
            "അഡ്മിൻ ടൈറ്റിൽ വിജയകരമായി മാറ്റിയിരിക്കുന്നു.. <b>{}</b> to <code>{}</code>!".format(
                user_member.user.first_name or user_id, title[:16]
            ),
            parse_mode=ParseMode.HTML,
        )

    except BadRequest:
        message.reply_text(
            "ഞാൻ പ്രൊമോട്ട് ചെയ്യാത്ത ആളിന്റെ അഡ്മിൻ ടൈറ്റിൽ മാറ്റാൻ എനിക്ക് സാധിക്കില്ല..!")


@run_async
@bot_admin
@user_admin
@typing_action
def setchatpic(update, context):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        msg.reply_text("You are missing right to change group info!")
        return

    if msg.reply_to_message:
        if msg.reply_to_message.photo:
            pic_id = msg.reply_to_message.photo[-1].file_id
        elif msg.reply_to_message.document:
            pic_id = msg.reply_to_message.document.file_id
        else:
            msg.reply_text("You can only set some photo as chat pic!")
            return
        dlmsg = msg.reply_text("Just a sec...")
        tpic = context.bot.get_file(pic_id)
        tpic.download("gpic.png")
        try:
            with open("gpic.png", "rb") as chatp:
                context.bot.set_chat_photo(int(chat.id), photo=chatp)
                msg.reply_text("Successfully set new chatpic!")
        except BadRequest as excp:
            msg.reply_text(f"Error! {excp.message}")
        finally:
            dlmsg.delete()
            if os.path.isfile("gpic.png"):
                os.remove("gpic.png")
    else:
        msg.reply_text("Reply to some photo or file to set new chat pic!")


@run_async
@bot_admin
@user_admin
@typing_action
def rmchatpic(update, context):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        msg.reply_text("You don't have enough rights to delete group photo")
        return
    try:
        context.bot.delete_chat_photo(int(chat.id))
        msg.reply_text("Successfully deleted chat's profile photo!")
    except BadRequest as excp:
        msg.reply_text(f"Error! {excp.message}.")
        return


@run_async
@bot_admin
@user_admin
@typing_action
def setchat_title(update, context):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    args = context.args

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        msg.reply_text("You don't have enough rights to change chat info!")
        return

    title = " ".join(args)
    if not title:
        msg.reply_text("Enter some text to set new title in your chat!")
        return

    try:
        context.bot.set_chat_title(int(chat.id), str(title))
        msg.reply_text(
            f"Successfully set <b>{title}</b> as new chat title!",
            parse_mode=ParseMode.HTML,
        )
    except BadRequest as excp:
        msg.reply_text(f"Error! {excp.message}.")
        return


@run_async
@bot_admin
@user_admin
@typing_action
def set_sticker(update, context):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        return msg.reply_text("You're missing rights to change chat info!")

    if msg.reply_to_message:
        if not msg.reply_to_message.sticker:
            return msg.reply_text(
                "You need to reply to some sticker to set chat sticker set!"
            )
        stkr = msg.reply_to_message.sticker.set_name
        try:
            context.bot.set_chat_sticker_set(chat.id, stkr)
            msg.reply_text(
                f"Successfully set new group stickers in {chat.title}!")
        except BadRequest as excp:
            if excp.message == "Participants_too_few":
                return msg.reply_text(
                    "Sorry, due to telegram restrictions chat needs to have minimum 100 members before they can have group stickers!"
                )
            msg.reply_text(f"Error! {excp.message}.")
    else:
        msg.reply_text(
            "You need to reply to some sticker to set chat sticker set!")


@run_async
@bot_admin
@user_admin
@typing_action
def set_desc(update, context):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        return msg.reply_text("You're missing rights to change chat info!")

    tesc = msg.text.split(None, 1)
    if len(tesc) >= 2:
        desc = tesc[1]
    else:
        return msg.reply_text("Setting empty description won't do anything!")
    try:
        if len(desc) > 255:
            return msg.reply_text(
                "Description must needs to be under 255 characters!")
        context.bot.set_chat_description(chat.id, desc)
        msg.reply_text(
            f"Successfully updated chat description in {chat.title}!")
    except BadRequest as excp:
        msg.reply_text(f"Error! {excp.message}.")


def __chat_settings__(chat_id, user_id):
    return "You are *admin*: `{}`".format(
        dispatcher.bot.get_chat_member(chat_id, user_id).status
        in ("administrator", "creator")
    )


__help__ = """
Lazy to promote or demote someone for admins? Want to see basic information about chat? \
All stuff about chatroom such as admin lists, pinning or grabbing an invite link can be \
done easily using the bot.

 × /adminlist: list of admins in the chat

*Admin only:*
 × /invitelink: Gets private chat's invitelink.
 × /settitle: Sets a custom title for an admin which is promoted by bot.
 × /setgpic: As a reply to file or photo to set group profile pic!
 × /delgpic: Same as above but to remove group profile pic.
 × /setgtitle <newtitle>: Sets new chat title in your group.
 × /setsticker: As a reply to some sticker to set it as group sticker set!
 × /setdescription: <description> Sets new chat description in group.

*Note*: To set group sticker set chat must needs to have min 100 members.

An example of promoting someone to admins:
`/promote @username`; this promotes a user to admins.
"""

__mod_name__ = "⚙️GROUP INFO"

PIN_HANDLER = CommandHandler("pin", pin, pass_args=True, filters=Filters.group)
UNPIN_HANDLER = CommandHandler("unpin", unpin, filters=Filters.group)
INVITE_HANDLER = CommandHandler("invitelink", invite)
CHAT_PIC_HANDLER = CommandHandler("setgpic", setchatpic, filters=Filters.group)
DEL_CHAT_PIC_HANDLER = CommandHandler(
    "delgpic", rmchatpic, filters=Filters.group)
SETCHAT_TITLE_HANDLER = CommandHandler(
    "setgtitle", setchat_title, filters=Filters.group
)
SETSTICKET_HANDLER = CommandHandler(
    "setsticker", set_sticker, filters=Filters.group)
SETDESC_HANDLER = CommandHandler(
    "setdescription",
    set_desc,
    filters=Filters.group)

PROMOTE_HANDLER = CommandHandler(
    "promote", promote, pass_args=True, filters=Filters.group
)
DEMOTE_HANDLER = CommandHandler(
    "demote",
    demote,
    pass_args=True,
    filters=Filters.group)

SET_TITLE_HANDLER = DisableAbleCommandHandler(
    "settitle", set_title, pass_args=True)
ADMINLIST_HANDLER = DisableAbleCommandHandler(
    "adminlist", adminlist, filters=Filters.group
)

dispatcher.add_handler(PIN_HANDLER)
dispatcher.add_handler(UNPIN_HANDLER)
dispatcher.add_handler(INVITE_HANDLER)
dispatcher.add_handler(PROMOTE_HANDLER)
dispatcher.add_handler(DEMOTE_HANDLER)
dispatcher.add_handler(ADMINLIST_HANDLER)
dispatcher.add_handler(SET_TITLE_HANDLER)
dispatcher.add_handler(CHAT_PIC_HANDLER)
dispatcher.add_handler(DEL_CHAT_PIC_HANDLER)
dispatcher.add_handler(SETCHAT_TITLE_HANDLER)
dispatcher.add_handler(SETSTICKET_HANDLER)
dispatcher.add_handler(SETDESC_HANDLER)

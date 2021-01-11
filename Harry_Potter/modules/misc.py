import datetime
import html
import json
import random
import re
from io import BytesIO
from random import randint
from typing import Optional

import html2text
import requests
import wikipedia
from bs4 import BeautifulSoup
from requests import get
from telegram import (
    Chat,
    ChatAction,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    MessageEntity,
    ParseMode,
    TelegramError,
)
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters
from telegram.utils.helpers import escape_markdown, mention_html

from Harry_Potter import (
    OWNER_ID,
    SUDO_USERS,
    SUPPORT_USERS,
    WALL_API,
    WHITELIST_USERS,
    dispatcher,
    spamwtc,
)
from Harry_Potter.__main__ import GDPR, STATS, USER_INFO
from Harry_Potter.modules.disable import DisableAbleCommandHandler
from Harry_Potter.modules.helper_funcs.alternate import send_action
from Harry_Potter.modules.helper_funcs.extraction import extract_user
from Harry_Potter.modules.helper_funcs.filters import CustomFilters


def get_id(update, context):
    args = context.args
    user_id = extract_user(update.effective_message, args)
    if user_id:
        if (
            update.effective_message.reply_to_message
            and update.effective_message.reply_to_message.forward_from
        ):
            user1 = update.effective_message.reply_to_message.from_user
            user2 = update.effective_message.reply_to_message.forward_from
            update.effective_message.reply_text(
                "The original sender, {}, has an ID of `{}`.\nThe forwarder, {}, has an ID of `{}`.".format(
                    escape_markdown(user2.first_name),
                    user2.id,
                    escape_markdown(user1.first_name),
                    user1.id,
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            user = context.bot.get_chat(user_id)
            update.effective_message.reply_text(
                "{}'s id is `{}`.".format(escape_markdown(user.first_name), user.id),
                parse_mode=ParseMode.MARKDOWN,
            )
    else:
        chat = update.effective_chat  # type: Optional[Chat]
        if chat.type == "private":
            update.effective_message.reply_text(
                "Your id is `{}`.".format(chat.id), parse_mode=ParseMode.MARKDOWN
            )

        else:
            update.effective_message.reply_text(
                "This group's id is `{}`.".format(chat.id),
                parse_mode=ParseMode.MARKDOWN,
            )


def info(update, context):
    args = context.args
    msg = update.effective_message  # type: Optional[Message]
    user_id = extract_user(update.effective_message, args)
    chat = update.effective_chat

    if user_id:
        user = context.bot.get_chat(user_id)

    elif not msg.reply_to_message and not args:
        user = msg.from_user

    elif not msg.reply_to_message and (
        not args
        or (
            len(args) >= 1
            and not args[0].startswith("@")
            and not args[0].isdigit()
            and not msg.parse_entities([MessageEntity.TEXT_MENTION])
        )
    ):
        msg.reply_text("I can't extract a user from this.")
        return

    else:
        return

    del_msg = msg.reply_text(
        "Hold tight while I steal some data from <b>FBI Database</b>...",
        parse_mode=ParseMode.HTML,
    )

    text = (
        "<b>USER INFO</b>:"
        "\n\nID: <code>{}</code>"
        "\nFirst Name: {}".format(user.id, html.escape(user.first_name))
    )

    if user.last_name:
        text += "\nLast Name: {}".format(html.escape(user.last_name))

    if user.username:
        text += "\nUsername: @{}".format(html.escape(user.username))

    text += "\nPermanent user link: {}".format(mention_html(user.id, "link"))

    text += "\nNumber of profile pics: {}".format(
        context.bot.get_user_profile_photos(user.id).total_count
    )

    try:
        sw = spamwtc.get_ban(int(user.id))
        if sw:
            text += "\n\n<b>This person is banned in Spamwatch!</b>"
            text += f"\nResason: <pre>{sw.reason}</pre>"
    except BaseException:
        pass  # Don't break on exceptions like if api is down?

    if user.id == OWNER_ID:
        text += "\n\nAye this guy is my owner.\nI would never do anything against him!"

    elif user.id in SUDO_USERS:
        text += (
            "\n\nThis person is one of my sudo users! "
            "Nearly as powerful as my owner - so watch it."
        )

    elif user.id in SUPPORT_USERS:
        text += (
            "\n\nThis person is one of my support users! "
            "Not quite a sudo user, but can still gban you off the map."
        )

    elif user.id in WHITELIST_USERS:
        text += (
            "\n\nThis person has been whitelisted! "
            "That means I'm not allowed to ban/kick them."
        )

    elif user.id == int(1087968824):
        text += "\n\nThis person is anonymous admin in this group. "

    try:
        memstatus = chat.get_member(user.id).status
        if memstatus in ["administrator", "creator"]:
            result = context.bot.get_chat_member(chat.id, user.id)
            if result.custom_title:
                text += f"\n\nThis user has custom title <b>{result.custom_title}</b> in this chat."
    except BadRequest:
        pass

    for mod in USER_INFO:
        try:
            mod_info = mod.__user_info__(user.id).strip()
        except TypeError:
            mod_info = mod.__user_info__(user.id, chat.id).strip()
        if mod_info:
            text += "\n\n" + mod_info

    try:
        profile = context.bot.get_user_profile_photos(user.id).photos[0][-1]
        context.bot.sendChatAction(chat.id, "upload_photo")
        context.bot.send_photo(
            chat.id,
            photo=profile,
            caption=(text),
            parse_mode=ParseMode.HTML,
        )
    except IndexError:
        context.bot.sendChatAction(chat.id, "typing")
        msg.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    finally:
        del_msg.delete()


def echo(update, context):
    args = update.effective_message.text.split(None, 1)
    message = update.effective_message
    if message.reply_to_message:
        message.reply_to_message.reply_text(args[1])
    else:
        message.reply_text(args[1], quote=False)
    message.delete()


def gdpr(update, context):
    update.effective_message.reply_text("Deleting identifiable data...")
    for mod in GDPR:
        mod.__gdpr__(update.effective_user.id)

    update.effective_message.reply_text(
        "Your personal data has been deleted.\n\nNote that this will not unban "
        "you from any chats, as that is telegram data, not Harry Potter data. "
        "Flooding, warns, and gbans are also preserved, as of "
        "[this](https://ico.org.uk/for-organisations/guide-to-the-general-data-protection-regulation-gdpr/individual-rights/right-to-erasure/), "
        "which clearly states that the right to erasure does not apply "
        '"for the performance of a task carried out in the public interest", as is '
        "the case for the aforementioned pieces of data.",
        parse_mode=ParseMode.MARKDOWN,
    )


MARKDOWN_HELP = """
Markdown is a very powerful formatting tool supported by telegram. {} has some enhancements, to make sure that \
saved messages are correctly parsed, and to allow you to create buttons.

- <code>_italic_</code>: wrapping text with '_' will produce italic text
- <code>*bold*</code>: wrapping text with '*' will produce bold text
- <code>`code`</code>: wrapping text with '`' will produce monospaced text, also known as 'code'
- <code>~strike~</code> wrapping text with '~' will produce strikethrough text
- <code>--underline--</code> wrapping text with '--' will produce underline text
- <code>[sometext](someURL)</code>: this will create a link - the message will just show <code>sometext</code>, \
and tapping on it will open the page at <code>someURL</code>.
EG: <code>[test](example.com)</code>

- <code>[buttontext](buttonurl:someURL)</code>: this is a special enhancement to allow users to have telegram \
buttons in their markdown. <code>buttontext</code> will be what is displayed on the button, and <code>someurl</code> \
will be the url which is opened.
EG: <code>[This is a button](buttonurl:example.com)</code>

If you want multiple buttons on the same line, use :same, as such:
<code>[one](buttonurl://example.com)
[two](buttonurl://google.com:same)</code>
This will create two buttons on a single line, instead of one button per line.

Keep in mind that your message <b>MUST</b> contain some text other than just a button!
""".format(
    dispatcher.bot.first_name
)


def markdown_help(update, context):
    update.effective_message.reply_text(MARKDOWN_HELP, parse_mode=ParseMode.HTML)
    update.effective_message.reply_text(
        "Try forwarding the following message to me, and you'll see!"
    )
    update.effective_message.reply_text(
        "/save test This is a markdown test. _italics_, --underline--, *bold*, `code`, ~strike~ "
        "[URL](example.com) [button](buttonurl:github.com) "
        "[button2](buttonurl://google.com:same)"
    )


def wiki(update, context):
    kueri = re.split(pattern="wiki", string=update.effective_message.text)
    wikipedia.set_lang("en")
    if len(str(kueri[1])) == 0:
        update.effective_message.reply_text("Enter keywords!")
    else:
        try:
            pertama = update.effective_message.reply_text("🔄 Loading...")
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🔧 More Info...", url=wikipedia.page(kueri).url
                        )
                    ]
                ]
            )
            context.bot.editMessageText(
                chat_id=update.effective_chat.id,
                message_id=pertama.message_id,
                text=wikipedia.summary(kueri, sentences=10),
                reply_markup=keyboard,
            )
        except wikipedia.PageError as e:
            update.effective_message.reply_text(f"⚠ Error: {e}")
        except BadRequest as et:
            update.effective_message.reply_text(f"⚠ Error: {et}")
        except wikipedia.exceptions.DisambiguationError as eet:
            update.effective_message.reply_text(
                f"⚠ Error\n There are too many query! Express it more!\nPossible query result:\n{eet}"
            )


def ud(update, context):
    msg = update.effective_message
    args = context.args
    text = " ".join(args).lower()
    if not text:
        msg.reply_text("Please enter keywords to search!")
        return
    elif text == "starry":
        msg.reply_text("Fek off bitch!")
        return
    try:
        results = get(f"http://api.urbandictionary.com/v0/define?term={text}").json()
        reply_text = f'Word: {text}\nDefinition: {results["list"][0]["definition"]}'
        reply_text += f'\n\nExample: {results["list"][0]["example"]}'
    except IndexError:
        reply_text = (
            f"Word: {text}\nResults: Sorry could not find any matching results!"
        )
    ignore_chars = "[]"
    reply = reply_text
    for chars in ignore_chars:
        reply = reply.replace(chars, "")
    if len(reply) >= 4096:
        reply = reply[:4096]  # max msg lenth of tg.
    try:
        msg.reply_text(reply)
    except BadRequest as err:
        msg.reply_text(f"Error! {err.message}")


@send_action(ChatAction.UPLOAD_PHOTO)
def wall(update, context):
    chat_id = update.effective_chat.id
    msg = update.effective_message
    msg_id = update.effective_message.message_id
    args = context.args
    query = " ".join(args)
    if not query:
        msg.reply_text("Please enter a query!")
        return
    else:
        caption = query
        term = query.replace(" ", "%20")
        json_rep = requests.get(
            f"https://wall.alphacoders.com/api2.0/get.php?auth={WALL_API}&method=search&term={term}"
        ).json()
        if not json_rep.get("success"):
            msg.reply_text("An error occurred!")

        else:
            wallpapers = json_rep.get("wallpapers")
            if not wallpapers:
                msg.reply_text("No results found! Refine your search.")
                return
            else:
                index = randint(0, len(wallpapers) - 1)  # Choose random index
                wallpaper = wallpapers[index]
                wallpaper = wallpaper.get("url_image")
                wallpaper = wallpaper.replace("\\", "")
                context.bot.send_photo(
                    chat_id,
                    photo=wallpaper,
                    caption="Preview",
                    reply_to_message_id=msg_id,
                    timeout=60,
                )
                context.bot.send_document(
                    chat_id,
                    document=wallpaper,
                    filename="wallpaper",
                    caption=caption,
                    reply_to_message_id=msg_id,
                    timeout=60,
                )


def imdb(update, context):
    try:
        args = context.args
        movie_name = " ".join(args)
        remove_space = movie_name.split(" ")
        final_name = "+".join(remove_space)
        page = requests.get(
            "https://www.imdb.com/find?ref_=nv_sr_fn&q=" + final_name + "&s=all"
        )
        str(page.status_code)
        soup = BeautifulSoup(page.content, "lxml")
        odds = soup.findAll("tr", "odd")
        mov_title = odds[0].findNext("td").findNext("td").text
        mov_link = (
            "http://www.imdb.com/" + odds[0].findNext("td").findNext("td").a["href"]
        )
        page1 = requests.get(mov_link)
        soup = BeautifulSoup(page1.content, "lxml")
        if soup.find("div", "poster"):
            poster = soup.find("div", "poster").img["src"]
        else:
            poster = ""
        if soup.find("div", "title_wrapper"):
            pg = soup.find("div", "title_wrapper").findNext("div").text
            mov_details = re.sub(r"\s+", " ", pg)
        else:
            mov_details = ""
        credits = soup.findAll("div", "credit_summary_item")
        director = credits[0].a.text
        if len(credits) == 1:
            writer = "Not available"
            stars = "Not available"
        elif len(credits) > 2:
            writer = credits[1].a.text
            actors = [x.text for x in credits[2].findAll("a")]
            actors.pop()
            stars = actors[0] + "," + actors[1] + "," + actors[2]
        else:
            writer = "Not available"
            actors = [x.text for x in credits[1].findAll("a")]
            actors.pop()
            stars = actors[0] + "," + actors[1] + "," + actors[2]
        if soup.find("div", "inline canwrap"):
            story_line = soup.find("div", "inline canwrap").findAll("p")[0].text
        else:
            story_line = "Not available"
        info = soup.findAll("div", "txt-block")
        if info:
            mov_country = []
            mov_language = []
            for node in info:
                a = node.findAll("a")
                for i in a:
                    if "country_of_origin" in i["href"]:
                        mov_country.append(i.text)
                    elif "primary_language" in i["href"]:
                        mov_language.append(i.text)
        if soup.findAll("div", "ratingValue"):
            for r in soup.findAll("div", "ratingValue"):
                mov_rating = r.strong["title"]
        else:
            mov_rating = "Not available"
        msg = f"*Title :* {mov_title}\n{mov_details}\n*Rating :* {mov_rating} \n*Country :*  {mov_country}\n*Language :* {mov_language}\n*Director :* {director}\n*Writer :* {writer}\n*Stars :* {stars}\n*IMDB Url :* {mov_link}\n*Story Line :* {story_line}"
        update.effective_message.reply_photo(
            photo=poster, caption=msg, parse_mode=ParseMode.MARKDOWN
        )
    except IndexError:
        update.effective_message.reply_text("Plox enter **Valid movie name** kthx")


def getlink(update, context):
    args = context.args
    message = update.effective_message
    if args:
        pattern = re.compile(r"-\d+")
    else:
        message.reply_text("You don't seem to be referring to any chats.")
    links = "Invite link(s):\n"
    for chat_id in pattern.findall(message.text):
        try:
            chat = context.bot.getChat(chat_id)
            bot_member = chat.get_member(context.bot.id)
            if bot_member.can_invite_users:
                invitelink = context.bot.exportChatInviteLink(chat_id)
                links += str(chat_id) + ":\n" + invitelink + "\n"
            else:
                links += (
                    str(chat_id) + ":\nI don't have access to the invite link." + "\n"
                )
        except BadRequest as excp:
            links += str(chat_id) + ":\n" + excp.message + "\n"
        except TelegramError as excp:
            links += str(chat_id) + ":\n" + excp.message + "\n"

    message.reply_text(links)


@send_action(ChatAction.UPLOAD_PHOTO)
def rmemes(update, context):
    msg = update.effective_message
    chat = update.effective_chat

    SUBREDS = [
        "meirl",
        "dankmemes",
        "AdviceAnimals",
        "memes",
        "meme",
        "memes_of_the_dank",
        "PornhubComments",
        "teenagers",
        "memesIRL",
        "insanepeoplefacebook",
        "terriblefacebookmemes",
    ]

    subreddit = random.choice(SUBREDS)
    res = requests.get(f"https://meme-api.herokuapp.com/gimme/{subreddit}")

    if res.status_code != 200:  # Like if api is down?
        msg.reply_text("Sorry some error occurred :(")
        return
    else:
        res = res.json()

    rpage = res.get(str("subreddit"))  # Subreddit
    title = res.get(str("title"))  # Post title
    memeu = res.get(str("url"))  # meme pic url
    plink = res.get(str("postLink"))

    caps = f"× <b>Title</b>: {title}\n"
    caps += f"× <b>Subreddit:</b> <pre>r/{rpage}</pre>"

    keyb = [[InlineKeyboardButton(text="Subreddit Postlink 🔗", url=plink)]]
    try:
        context.bot.send_photo(
            chat.id,
            photo=memeu,
            caption=(caps),
            reply_markup=InlineKeyboardMarkup(keyb),
            timeout=60,
            parse_mode=ParseMode.HTML,
        )

    except BadRequest as excp:
        return msg.reply_text(f"Error! {excp.message}")


def covid(update, context):
    message = update.effective_message
    args = context.args
    query = " ".join(args)
    remove_space = query.split(" ")
    country = "%20".join(remove_space)
    if not country:
        url = "https://disease.sh/v3/covid-19/all?yesterday=false&twoDaysAgo=false&allowNull=true"
        country = "World"
    else:
        url = f"https://disease.sh/v3/covid-19/countries/{country}?yesterday=false&twoDaysAgo=false&strict=true&allowNull=true"
    request = requests.get(url).text
    case = json.loads(request)
    json_date = case["updated"]
    float_date = float(json_date) / 1000.0
    date = datetime.datetime.fromtimestamp(float_date).strftime("%d %b %Y %I:%M:%S %p")
    try:
        flag = case["countryInfo"]["flag"]
    except KeyError:
        pass
    text = f"*COVID-19 Statistics in {country} :*\n📅 Last Updated on {date}\n\n🔼 Confirmed Cases : `{case['cases']}` `+{case['todayCases']}` on today\n🔺 Active Cases : `{case['active']}`\n⚰️ Deaths : `{case['deaths']}` `+{case['todayDeaths']}` on today\n💹 Recovered Cases: `{case['recovered']}` `+{case['todayRecovered']}` on today\n💉 Total Tests : `{case['tests']}`\n👥 Populations : `{case['population']}`\n🌐 Source : [worldometers]({url})"
    try:
        message.reply_photo(photo=flag, caption=text, parse_mode=ParseMode.MARKDOWN)
    except BaseException:
        message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


def app(update, context):
    try:
        args = context.args
        app_name = " ".join(args)
        remove_space = app_name.split(" ")
        final_name = "+".join(remove_space)
        page = get("https://play.google.com/store/search?q=" + final_name + "&c=apps")
        soup = BeautifulSoup(page.content, "lxml", from_encoding="utf-8")
        results = soup.findAll("div", "ZmHEEd")
        app_name = (
            results[0].findNext("div", "Vpfmgd").findNext("div", "WsMG1c nnK0zc").text
        )
        app_dev = results[0].findNext("div", "Vpfmgd").findNext("div", "KoLSrc").text
        app_dev_link = (
            "https://play.google.com"
            + results[0].findNext("div", "Vpfmgd").findNext("a", "mnKHRc")["href"]
        )
        app_rating = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "pf5lIe")
            .find("div")["aria-label"]
        )
        app_link = (
            "https://play.google.com"
            + results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "vU6FJ p63iDd")
            .a["href"]
        )
        app_icon = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "uzcko")
            .img["data-src"]
        )
        app_details = "<a href='" + app_icon + "'>📲&#8203;</a>"
        app_details += " <b>" + app_name + "</b>"
        app_details += (
            "\n\n<code>Developer :</code> <a href='"
            + app_dev_link
            + "'>"
            + app_dev
            + "</a>"
        )
        app_details += "\n<code>Rating :</code> " + app_rating.replace(
            "Rated ", "⭐ "
        ).replace(" out of ", "/").replace(" stars", "", 1).replace(
            " stars", "⭐ "
        ).replace(
            "five", "5"
        )
        app_details += (
            "\n<code>Features :</code> <a href='"
            + app_link
            + "'>View in Play Store</a>"
        )
        update.effective_message.reply_text(app_details, parse_mode="HTML")
    except IndexError:
        update.effective_message.reply_text(
            "No result found in search. Please enter **Valid app name**"
        )
    except Exception as err:
        update.effective_message.reply_text("Exception Occured:- " + str(err))


def google(update, context):
    args = context.args
    query = " ".join(args)
    remove_space = query.split(" ")
    # + " -inurl:(htm|html|php|pls|txt) intitle:index.of \"last modified\" (mkv|mp4|avi|epub|pdf|mp3)"
    input_str = "%20".join(remove_space)
    input_url = "https://bots.shrimadhavuk.me/search/?q={}".format(input_str)
    headers = {"USER-AGENT": "UniBorg"}
    response = requests.get(input_url, headers=headers).json()
    output_str = " "
    for result in response["results"]:
        text = result.get("title")
        url = result.get("url")
        description = result.get("description")
        last = html2text.html2text(description)
        output_str += "[{}]({})\n{}\n".format(text, url, last)
    update.effective_message.reply_text("{}".format(output_str), parse_mode="MARKDOWN")


def staff_ids(update, context):
    sfile = "List of SUDO & SUPPORT users:\n"
    sfile += f"× SUDO USER IDs; {SUDO_USERS}\n"
    sfile += f"× SUPPORT USER IDs; {SUPPORT_USERS}"
    with BytesIO(str.encode(sfile)) as output:
        output.name = "staff-ids.txt"
        update.effective_message.reply_document(
            document=output,
            filename="staff-ids.txt",
            caption="Here is the list of SUDO & SUPPORTS users.",
        )


def stats(update, context):
    update.effective_message.reply_text(
        "Current stats:\n" + "\n".join(mod.__stats__() for mod in STATS)
    )


# /ip is for private use
__help__ = """
An "odds and ends" module for small, simple commands which don't really fit anywhere

 × /id: Get the current group id. If used by replying to a message, gets that user's id.
 × /info: Get information about a user.
 × /wiki : Search wikipedia articles.
 × /rmeme: Sends random meme scraped from reddit.
 × /ud <query> : Search stuffs in urban dictionary.
 × /wall <query> : Get random wallpapers directly from bot!
 × /gdpr: Deletes your information from the bot's database. Private chats only.
 *Last.FM*
 × /setuser <username>: sets your last.fm username.
 × /clearuser: removes your last.fm username from the bot's database.
 × /lastfm: returns what you're scrobbling on last.fm.
 *Google*
 × /google <query> : Search query on google
 × /reverse : Reverse searches image or stickers on google.
 × /paste: Saves replied content to nekobin.com and replies with a url
 × /lyrics <query>: search lyrics can be song name or artist name
 × /covid <country>: Get information about COVID-19 Stats, empty query = world
 × /app <query>: search an app on Play Store
 × /imdb <movie>: search movie info and other stuff
 × /markdownhelp: Quick summary of how markdown works in telegram - can only be called in private chats.
"""

__mod_name__ = "Miscs"

ID_HANDLER = DisableAbleCommandHandler("id", get_id, pass_args=True)
INFO_HANDLER = DisableAbleCommandHandler("info", info, pass_args=True)
ECHO_HANDLER = CommandHandler("echo", echo, filters=CustomFilters.sudo_filter)
MD_HELP_HANDLER = CommandHandler("markdownhelp", markdown_help, filters=Filters.private)
STATS_HANDLER = CommandHandler("stats", stats, filters=Filters.user(OWNER_ID))
GDPR_HANDLER = CommandHandler("gdpr", gdpr, filters=Filters.private)
WIKI_HANDLER = DisableAbleCommandHandler("wiki", wiki)
WALLPAPER_HANDLER = DisableAbleCommandHandler("wall", wall, pass_args=True)
IMDB_HANDLER = DisableAbleCommandHandler("imdb", imdb, pass_args=True)
UD_HANDLER = DisableAbleCommandHandler("ud", ud)
GETLINK_HANDLER = CommandHandler(
    "getlink", getlink, pass_args=True, filters=Filters.user(OWNER_ID)
)
COVID_HANDLER = DisableAbleCommandHandler("covid", covid)
APP_HANDLER = DisableAbleCommandHandler("app", app)
GOOGLE_HANDLER = DisableAbleCommandHandler("google", google)

STAFFLIST_HANDLER = CommandHandler(
    "staffids", staff_ids, filters=Filters.user(OWNER_ID)
)
REDDIT_MEMES_HANDLER = DisableAbleCommandHandler("rmeme", rmemes)

dispatcher.add_handler(WALLPAPER_HANDLER)
dispatcher.add_handler(UD_HANDLER)
dispatcher.add_handler(ID_HANDLER)
dispatcher.add_handler(INFO_HANDLER)
dispatcher.add_handler(ECHO_HANDLER)
dispatcher.add_handler(MD_HELP_HANDLER)
dispatcher.add_handler(STATS_HANDLER)
dispatcher.add_handler(GDPR_HANDLER)
dispatcher.add_handler(WIKI_HANDLER)
dispatcher.add_handler(GETLINK_HANDLER)
dispatcher.add_handler(COVID_HANDLER)
dispatcher.add_handler(APP_HANDLER)
dispatcher.add_handler(GOOGLE_HANDLER)
dispatcher.add_handler(STAFFLIST_HANDLER)
dispatcher.add_handler(REDDIT_MEMES_HANDLER)
dispatcher.add_handler(IMDB_HANDLER)

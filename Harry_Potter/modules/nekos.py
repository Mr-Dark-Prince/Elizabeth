import nekos
from telegram import ParseMode

from priscia import dispatcher
from priscia.modules.disable import DisableAbleCommandHandler


def nekoimage(update, context, site: str):
    message = update.effective_message
    img = nekos.img(site)
    message.reply_photo(photo=img, parse_mode=ParseMode.MARKDOWN)


def nekovideo(update, context, site: str):
    message = update.effective_message
    img = nekos.img(site)
    message.reply_video(video=img, parse_mode=ParseMode.MARKDOWN)


def nekodoc(update, context, site: str):
    message = update.effective_message
    img = nekos.img(site)
    message.reply_document(document=img, parse_mode=ParseMode.MARKDOWN)


def neko(update, context):
    nekodoc(update, context, "neko")


def erokemo(update, context):
    nekoimage(update, context, "erokemo")


def wallpaper(update, context):
    nekodoc(update, context, "wallpaper")


def ngif(update, context):
    nekovideo(update, context, "ngif")


def tickle(update, context):
    nekoimage(update, context, "tickle")


def feed(update, context):
    nekoimage(update, context, "feed")


def eroneko(update, context):
    nekoimage(update, context, "eron")


def kemonomimi(update, context):
    nekoimage(update, context, "kemonomimi")


def poke(update, context):
    nekovideo(update, context, "poke")


def avatar(update, context):
    nekoimage(update, context, "avatar")


def waifu(update, context):
    nekoimage(update, context, "waifu")


def pat(update, context):
    nekovideo(update, context, "pat")


def cuddle(update, context):
    nekovideo(update, context, "cuddle")


def foxgirl(update, context):
    nekoimage(update, context, "fox_girl")


def hug(update, context):
    nekovideo(update, context, "hug")


def smug(update, context):
    nekovideo(update, context, "smug")


def goose(update, context):
    nekoimage(update, context, "goose")


def baka(update, context):
    nekovideo(update, context, "baka")


def woof(update, context):
    nekoimage(update, context, "woof")


__help__ = """
Get random images from [Nekos API](nekos.life)
× /neko × /erokemo × /wallpaper × /ngif × /tickle
× /feed × /eron × /kemonomimi × /poke × /avatar
× /waifu × /pat × /cuddle × /foxgirl × /hug
× /smug × /goose × /baka × /woof
"""

__mod_name__ = "Nekos"

NEKO_HANDLER = DisableAbleCommandHandler("neko", neko)
EROKEMO_HANDLER = DisableAbleCommandHandler("erokemo", erokemo)
WALLPAPER_HANDLER = DisableAbleCommandHandler("wallpaper", wallpaper)
NGIF_HANDLER = DisableAbleCommandHandler("ngif", ngif)
TICKLE_HANDLER = DisableAbleCommandHandler("tickle", tickle)
FEED_HANDLER = DisableAbleCommandHandler("feed", feed)
ERONEKO_HANDLER = DisableAbleCommandHandler("eroneko", eroneko)
KEMONOMIMI_HANDLER = DisableAbleCommandHandler("kemonomimi", kemonomimi)
POKE_HANDLER = DisableAbleCommandHandler("poke", poke)
AVATAR_HANDLER = DisableAbleCommandHandler("avatar", avatar)
WAIFU_HANDLER = DisableAbleCommandHandler("waifu", waifu)
PAT_HANDLER = DisableAbleCommandHandler("pat", pat)
CUDDLE_HANDLER = DisableAbleCommandHandler("cuddle", cuddle)
FOXGIRL_HANDLER = DisableAbleCommandHandler("foxgirl", foxgirl)
HUG_HANDLER = DisableAbleCommandHandler("hug", hug)
SMUG_HANDLER = DisableAbleCommandHandler("smug", smug)
GOOSE_HANDLER = DisableAbleCommandHandler("goose", goose)
BAKA_HANDLER = DisableAbleCommandHandler("baka", baka)
WOOF_HANDLER = DisableAbleCommandHandler("woof", woof)

dispatcher.add_handler(NEKO_HANDLER)
dispatcher.add_handler(EROKEMO_HANDLER)
dispatcher.add_handler(WALLPAPER_HANDLER)
dispatcher.add_handler(NGIF_HANDLER)
dispatcher.add_handler(TICKLE_HANDLER)
dispatcher.add_handler(FEED_HANDLER)
dispatcher.add_handler(ERONEKO_HANDLER)
dispatcher.add_handler(KEMONOMIMI_HANDLER)
dispatcher.add_handler(POKE_HANDLER)
dispatcher.add_handler(AVATAR_HANDLER)
dispatcher.add_handler(WAIFU_HANDLER)
dispatcher.add_handler(PAT_HANDLER)
dispatcher.add_handler(CUDDLE_HANDLER)
dispatcher.add_handler(FOXGIRL_HANDLER)
dispatcher.add_handler(HUG_HANDLER)
dispatcher.add_handler(SMUG_HANDLER)
dispatcher.add_handler(GOOSE_HANDLER)
dispatcher.add_handler(BAKA_HANDLER)
dispatcher.add_handler(WOOF_HANDLER)

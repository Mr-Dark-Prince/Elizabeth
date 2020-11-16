from geopy.geocoders import Nominatim
from telegram import Location
from telegram import ParseMode
from telegram import Update
from telegram.ext import CommandHandler
from telegram.ext import run_async

from julia import dispatcher
from julia.modules.helper_funcs.chat_status import user_admin

GMAPS_LOC = "https://maps.googleapis.com/maps/api/geocode/json"


@run_async
@user_admin
def gps(update: Update, context):
    message = update.effective_message
    args = context.args
    if len(args) == 0:
        update.effective_message.reply_text(
            "That was a funny joke, but no really, put in a location")
    try:
        geolocator = Nominatim(user_agent="SkittBot")
        location = " ".join(args)
        geoloc = geolocator.geocode(location)
        chat_id = update.effective_chat.id
        lon = geoloc.longitude
        lat = geoloc.latitude
        the_loc = Location(lon, lat)
        gm = "https://www.google.com/maps/search/{},{}".format(lat, lon)
        context.bot.send_location(chat_id, location=the_loc)
        update.message.reply_text(
            "Open with: [Google Maps]({})".format(gm),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    except AttributeError:
        update.message.reply_text("I can't find that")


GPS_HANDLER = CommandHandler("gps", gps, pass_args=True)
dispatcher.add_handler(GPS_HANDLER)

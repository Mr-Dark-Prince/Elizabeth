import random
from telegram.ext import run_async, Filters
from telegram import Message, Chat, Update, Bot, MessageEntity
from Elizabeth import dispatcher
from Elizabeth.modules.disable import DisableAbleCommandHandler

KOZHI_STRINGS = (
    "എടാ കള്ളക്കോയീ ..😂😂😂",
    "കോയീ  ചിങ്കാര പൂങ്കോയീ . . . 🎶🎶😜 ",
    "ഡാ കോഴീ നിക്കെടാ അവിടേ..🤭🤭", 
    "ബ  ബ്ബാ ബ്ബാ ബ്ബാ കോയീ ബാ ബാ ..🤨🤨", 
    "നിനക്കല്ലേലും ഇതുങ്ങളെ കാണുമ്പോൾ ഒരിളക്കം ഉള്ളതാ 😜😬😬", 
    "ശ്ശോ പോ കോയീ..... ", 
    "പോയി  കൂട്ടിൽ കേറ് കോഴിയേ.... 😛😛😜", 
    "നിന്റെ കുണുങ്ങി കുണുങ്ങി ഉള്ള വരവ് കണ്ടാലേ അറിയാം നല്ല ഒന്നാന്തരം കാട്ടുകോഴിയാണെന്ന് ", 
    "കോയീ വാവാവോ എന്റെ കോയീ വാവാവോ 😂😂😂        ", 
    "എന്തൊലിപ്പീരാഡേയ് 😏😏😏", 
    "നീ പോടാ കാട്ടുകോഴീ ", 
    "കുണുക്കിട്ട കോഴീ കുളക്കോഴീ... 😂😂😜", 
  )

@run_async
def kozhi(bot: Bot, update: Update):
    bot.sendChatAction(update.effective_chat.id, "typing") # Bot typing before send messages
    message = update.effective_message
    if message.reply_to_message:
      message.reply_to_message.reply_text(random.choice(KOZHI_STRINGS))
    else:
      message.reply_text(random.choice(KOZHI_STRINGS))

__help__ = """
- /kozhi  🤬.
"""

__mod_name__ = "kozhi"

KOZHI_HANDLER = DisableAbleCommandHandler("kozhi",kozhi)

dispatcher.add_handler(KOZHI_HANDLER)

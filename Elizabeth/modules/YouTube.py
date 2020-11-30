from Elizabeth import client
import os
import time
from telethon import types
from telethon.tl import functions
from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import ContentTooShortError
from youtube_dl.utils import DownloadError
from youtube_dl.utils import ExtractorError
from youtube_dl.utils import GeoRestrictedError
from youtube_dl.utils import MaxDownloadsReached
from youtube_dl.utils import PostProcessingError
from youtube_dl.utils import UnavailableVideoError
from youtube_dl.utils import XAttrMetadataError
from Elizabeth.events import register


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (await client(functions.channels.GetParticipantRequest(chat, user))).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator)
        )
    elif isinstance(chat, types.InputPeerChat):

        ui = await client.get_peer_id(user)
        ps = (await client(functions.messages.GetFullChatRequest(chat.chat_id))) \
            .full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator)
        )
    else:
        return None


@register(pattern="^/yt(audio|video) (.*)")
async def download_video(v_url):

from telethon import events
import asyncio
from collections import deque
from Elizabeth.events import register

@register(pattern="^/earth")
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🌏🌍🌎🌎🌍🌏🌍🌎"))
	for _ in range(48):
		await asyncio.sleep(1)
		await event.reply("".join(deq))
		deq.rotate(1)

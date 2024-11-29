from pyrogram import filters
from pyrogram.types import Message

from AloneMusic import app
from AloneMusic.core.call import Alone

welcome = 20
close = 30


@app.on_message(filters.video_chat_started, group=welcome)
@app.on_message(filters.video_chat_ended, group=close)
async def welcome(_, message: Message):
    await Alone.stop_stream_force(message.chat.id)

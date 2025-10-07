import os
import asyncio
from telethon import TelegramClient, events
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import AudioPiped
from yt_dlp import YoutubeDL

API_ID = int(os.getenv("24816981"))
API_HASH = os.getenv("0396014dee5db7e657dcbda5e2158739")
SESSION = os.getenv("SESSION")

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
pytgcalls = PyTgCalls(client)

@client.on(events.NewMessage(pattern="/joinvc"))
async def joinvc(event):
    chat = await event.get_chat()
    await pytgcalls.join_group_call(chat.id, AudioPiped("join.mp3"))
    await event.reply("✅ Joined VC!")

@client.on(events.NewMessage(pattern=r"/play (.+)"))
async def play(event):
    query = event.pattern_match.group(1)
    await event.reply("🎵 Downloading audio...")

    ydl_opts = {'format': 'bestaudio', 'outtmpl': 'song.%(ext)s'}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        file = ydl.prepare_filename(info)

    chat = await event.get_chat()
    await pytgcalls.change_stream(chat.id, AudioPiped(file))
    await event.reply(f"▶️ Playing: {info['title']}")

@client.on(events.NewMessage(pattern="/stop"))
async def stop(event):
    chat = await event.get_chat()
    await pytgcalls.leave_group_call(chat.id)
    await event.reply("⏹️ Stopped & Left VC!")

async def main():
    await client.start()
    await pytgcalls.start()
    print("🎧 Userbot is online!")
    await idle()

with client:
    client.loop.run_until_complete(main())

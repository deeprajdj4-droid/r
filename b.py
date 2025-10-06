import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import AudioPiped
import asyncio

API_ID = 24816981  # apna api id
API_HASH = "0396014dee5db7e657dcbda5e2158739"
SESSION = "your_session_string"  # Pyrogram string session

app = Client(SESSION, api_id=API_ID, api_hash=API_HASH)
call = PyTgCalls(app)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.on_message(filters.private & (filters.voice | filters.audio))
async def play_audio(client, message):
    chat_id = message.chat.id
    msg = await message.reply("⏳ Audio download ho raha hai...")
    file_path = await message.download(file_name=f"{DOWNLOAD_DIR}/{message.id}.mp3")

    try:
        await call.join_group_call(
            chat_id,
            AudioPiped(file_path),
        )
        await msg.edit("🎧 Recording VC me play ho rahi hai!")
    except Exception as e:
        await msg.edit(f"❌ Error: {e}")

@app.on_message(filters.command("stop") & filters.me)
async def stop_audio(client, message):
    await call.leave_group_call(message.chat.id)
    await message.reply("🛑 VC playback stopped.")

@app.on_message(filters.command("leave") & filters.me)
async def leave_vc(client, message):
    await call.leave_group_call(message.chat.id)
    await message.reply("👋 VC se leave kar gaya.")

async def main():
    await app.start()
    await call.start()
    print("✅ Userbot ready! VC play feature active.")
    await idle()
    await app.stop()

asyncio.run(main())

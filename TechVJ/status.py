import sys
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from database.db import db  
from config import ADMINS   

# Bot start hote hi terminal mein print hoga agar file load hui
print("✅ status.py file successfully load ho gayi hai!")

@Client.on_message(filters.command("stats") & filters.user(ADMINS))
async def bot_stats(client: Client, message: Message):
    print(f"Stats command received from {message.from_user.id}")
    status_msg = await message.reply_text("<b>🔄 Statistics fetch kar raha hoon...</b>")
    try:
        total_users = await db.total_users_count()
        await status_msg.edit(f"<b>📊 Bot Statistics</b>\n\n<b>👤 Total Users:</b> <code>{total_users}</code>")
    except Exception as e:
        await status_msg.edit(f"<b>❌ Error:</b> <code>{e}</code>")

@Client.on_message(filters.command("restart") & filters.user(ADMINS))
async def restart_bot(client: Client, message: Message):
    print(f"Restart command received from {message.from_user.id}")
    try:
        msg = await message.reply_text("<b>♻️ Restarting system...</b>")
        await asyncio.sleep(2)
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as e:
        await message.reply_text(f"<b>❌ Restart Failed:</b> <code>{e}</code>")

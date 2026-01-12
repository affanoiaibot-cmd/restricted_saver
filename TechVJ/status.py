# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import sys
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from database.db import db  
from config import ADMINS   

@Client.on_message(filters.command(["stats", "restart"]) & filters.private)
async def status_and_restart_handler(client: Client, message: Message):
    # 1. Sabse pehle check karein ki user Admin hai ya nahi
    if message.from_user.id not in ADMINS:
        return await message.reply_text(f"<b>❌ Access Denied!</b>\n\nYour ID: <code>{message.from_user.id}</code> is not in Admin List.")

    cmd = message.command[0]

    # --- STATS COMMAND ---
    if cmd == "stats":
        sts_msg = await message.reply_text("<b>🔍 Fetching total users...</b>")
        try:
            # Yahan hum check kar rahe hain ki function name sahi hai ya nahi
            total_users = await db.total_users_count()
            await sts_msg.edit(f"<b>📊 <u>Bot Statistics</u></b>\n\n<b>👤 Total Users:</b> <code>{total_users}</code>")
        except Exception as e:
            await sts_msg.edit(f"<b>❌ Database Error:</b>\n<code>{e}</code>\n\n<i>Check if total_users_count() exists in db.py</i>")

    # --- RESTART COMMAND ---
    elif cmd == "restart":
        await message.reply_text("<b>♻️ Restarting bot system... Please wait.</b>")
        await asyncio.sleep(2)
        # Restart the process
        os.execl(sys.executable, sys.executable, *sys.argv)

# Don't Remove Credit @VJ_Bots

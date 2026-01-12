# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import sys
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from database.users_db import db
from info import ADMINS

# -----------------------------------------------------------
#   BOT STATISTICS COMMAND (ONLY TOTAL USERS)
# -----------------------------------------------------------
@Client.on_message(filters.command("stats") & filters.private & filters.user(ADMINS))
async def bot_stats(client: Client, message: Message):
    # Initial status message
    status_msg = await message.reply_text("<b>🔄 Fetching Stats...</b>", quote=True)
    
    try:
        # Database se sirf total users count lena
        total_users = await db.total_users_count()
        
        # Simple and Bold output with emoji
        await status_msg.edit(
            f"<b>📊 Bot Statistics</b>\n\n"
            f"<b>👤 Total Users:</b> <code>{total_users}</code>"
        )
    except Exception as e:
        # Error handling agar database fetch na ho paye
        await status_msg.edit(f"<b>❌ Error Fetching Stats:</b>\n<code>{e}</code>")

# -----------------------------------------------------------
#   RESTART BOT COMMAND
# -----------------------------------------------------------
@Client.on_message(filters.command("restart") & filters.private & filters.user(ADMINS))
async def restart_bot(client: Client, message: Message):
    try:
        msg = await message.reply_text("<b>♻️ Restarting the bot, please wait...</b>")
        await asyncio.sleep(2)
        await msg.edit("<b>✅ System Restart Initiated...\nI will be back in few seconds!</b>")
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as e:
        print(f"Restart Error: {e}")
        await message.reply_text(f"<b>❌ Error while restarting:</b> <code>{e}</code>")

# Don't Remove Credit @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

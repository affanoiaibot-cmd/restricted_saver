
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

# -----------------------------------------------------------
#  STATISTICS COMMAND (ONLY TOTAL USERS)
# -----------------------------------------------------------
@Client.on_message(filters.command("stats") & filters.private & filters.user(ADMINS))
async def bot_stats(client: Client, message: Message):
    status_msg = await message.reply_text("<b>🔄 Statistics fetch kar raha hoon...</b>")
    
    try:
        # Database se total users count lena
        total_users = await db.total_users_count()
        
        # Professional UI
        await status_msg.edit(
            f"<b>📊 <u>Bot Statistics</u></b>\n\n"
            f"<b>👤 Total Users:</b> <code>{total_users}</code>"
        )
    except Exception as e:
        await status_msg.edit(f"<b>❌ Error:</b> <code>{e}</code>")

# -----------------------------------------------------------
#  RESTART COMMAND
# -----------------------------------------------------------
@Client.on_message(filters.command("restart") & filters.private & filters.user(ADMINS))
async def restart_bot(client: Client, message: Message):
    try:
        msg = await message.reply_text("<b>♻️ Restarting system...</b>")
        await asyncio.sleep(2)
        await msg.edit("<b>✅ Restart successful!\nBot wapas online aa raha hai...</b>")
        
        # Current process ko terminate karke naya process start karna
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as e:
        await message.reply_text(f"<b>❌ Restart Failed:</b> <code>{e}</code>")

# Don't Remove Credit @VJ_Bots

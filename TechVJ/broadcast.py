# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ

import os
import sys
import asyncio
import datetime
import time
import psutil
import shutil
from pyrogram import Client, filters
from pyrogram.errors import InputUserDeactivated, FloodWait, UserIsBlocked, PeerIdInvalid
from database.db import db
from config import ADMINS

# --- Helper for Statistics Display ---
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

# --- Core Broadcast Logic ---
async def broadcast_messages(user_id, message, is_pin):
    try:
        # Message ko user ke chat mein copy karna
        msg = await message.copy(chat_id=user_id)
        if is_pin:
            try: 
                await msg.pin(both_sides=True)
            except: 
                pass
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages(user_id, message, is_pin)
    except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid):
        # Invalid users ko DB se remove karna
        await db.delete_user(int(user_id))
        return False, "Deleted"
    except Exception:
        return False, "Error"

async def process_broadcast(bot, message, is_pin):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    if not b_msg: 
        return await message.reply_text("<b>⚠️ Please reply to a message to start broadcast!</b>")
    
    sts = await message.reply_text("<b>📢 Broadcasting started...</b>")
    
    total_users = await db.total_users_count()
    done = success = blocked = deleted = failed = 0
    
    async for user in users:
        if 'id' in user:
            pti, sh = await broadcast_messages(int(user['id']), b_msg, is_pin)
            if pti: 
                success += 1
            elif sh == "Blocked": 
                blocked += 1
            elif sh == "Deleted": 
                deleted += 1
            else: 
                failed += 1
            done += 1
            
            # Har 20 messages ke baad status update (Floodwait se bachne ke liye)
            if not done % 20:
                await sts.edit(f"<b>⏳ Broadcast Progress:</b> <code>{done}/{total_users}</code>")
    
    await sts.edit(
        f"<b>✅ Broadcast Completed!</b>\n\n"
        f"<b>Total:</b> <code>{total_users}</code>\n"
        f"<b>Success:</b> <code>{success}</code>\n"
        f"<b>Blocked:</b> <code>{blocked}</code>\n"
        f"<b>Failed:</b> <code>{failed}</code>"
    )

# --- ADMIN COMMANDS ---

# /broadcast command
@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def bc_handler(bot, message):
    await process_broadcast(bot, message, is_pin=False)

# /stats command
@Client.on_message(filters.command("stats") & filters.private & filters.user(ADMINS))
async def stats_handler(client, message):
    m = await message.reply_text("<b>📊 Fetching Bot Statistics...</b>")
    total_users = await db.total_users_count()
    
    # System resources info
    total, used, free = shutil.disk_usage(".")
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    
    await m.edit(
        f"<b>📊 <u>Bot Statistics</u></b>\n\n"
        f"<b>👤 Total Users:</b> <code>{total_users}</code>\n"
        f"<b>🖥️ CPU Usage:</b> <code>{cpu_usage}%</code>\n"
        f"<b>💾 RAM Usage:</b> <code>{ram_usage}%</code>\n"
        f"<b>💽 Disk Free:</b> <code>{get_size(free)}</code>"
    )

# /restart command
@Client.on_message(filters.command("restart") & filters.private & filters.user(ADMINS))
async def restart_handler(client, message):
    await message.reply_text("<b>♻️ Restarting System...</b>")
    await asyncio.sleep(2)
    # Bot process ko restart karna
    os.execl(sys.executable, sys.executable, *sys.argv)

# Notification Logic (Used in bot.py)
async def send_restart_notification(bot):
    users = await db.get_all_users()
    async for user in users:
        if 'id' in user:
            try:
                # Aapki request ke mutabik bold small text
                await bot.send_message(chat_id=int(user['id']), text="<b>bot restart</b>")
                await asyncio.sleep(0.05)
            except: 
                continue

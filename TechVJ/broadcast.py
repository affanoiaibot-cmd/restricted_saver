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

# --- Helper for Stats ---
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

# --- Broadcast Logic ---
async def broadcast_messages(user_id, message, is_pin):
    try:
        msg = await message.copy(chat_id=user_id)
        if is_pin:
            try: await msg.pin(both_sides=True)
            except: pass
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages(user_id, message, is_pin)
    except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid):
        await db.delete_user(int(user_id))
        return False, "Deleted"
    except Exception:
        return False, "Error"

async def process_broadcast(bot, message, is_pin):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    if not b_msg: return await message.reply_text("<b>Reply to a message to broadcast!</b>")
    sts = await message.reply_text("<b>Broadcasting started...</b>")
    
    total_users = await db.total_users_count()
    done = success = blocked = deleted = failed = 0
    async for user in users:
        if 'id' in user:
            pti, sh = await broadcast_messages(int(user['id']), b_msg, is_pin)
            if pti: success += 1
            elif sh == "Blocked": blocked += 1
            elif sh == "Deleted": deleted += 1
            else: failed += 1
            done += 1
            if not done % 20:
                await sts.edit(f"<b>Broadcast:</b> {done}/{total_users}")
    await sts.edit(f"<b>Broadcast Done!</b>\nSuccess: {success}\nBlocked: {blocked}")

# --- COMMANDS ---

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def bc_handler(bot, message):
    await process_broadcast(bot, message, is_pin=False)

@Client.on_message(filters.command("stats") & filters.private & filters.user(ADMINS))
async def stats_handler(client, message):
    m = await message.reply_text("<b>Checking Stats...</b>")
    total_users = await db.total_users_count()
    total, used, free = shutil.disk_usage(".")
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    
    await m.edit(
        f"<b>📊 Bot Statistics</b>\n\n"
        f"<b>👤 Total Users:</b> <code>{total_users}</code>\n"
        f"<b>🖥️ CPU Usage:</b> <code>{cpu_usage}%</code>\n"
        f"<b>💾 RAM Usage:</b> <code>{ram_usage}%</code>\n"
        f"<b>💽 Disk Free:</b> <code>{get_size(free)}</code>"
    )

@Client.on_message(filters.command("restart") & filters.private & filters.user(ADMINS))
async def restart_handler(client, message):
    await message.reply_text("<b>♻️ Restarting System...</b>")
    await asyncio.sleep(2)
    os.execl(sys.executable, sys.executable, *sys.argv)

# Notification function for bot.py
async def send_restart_notification(bot):
    users = await db.get_all_users()
    async for user in users:
        if 'id' in user:
            try:
                await bot.send_message(chat_id=int(user['id']), text="<b>bot restart</b>")
                await asyncio.sleep(0.05)
            except: continue

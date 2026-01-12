

import os
import sys
import asyncio
import datetime
import time
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
from database.db import db
from config import ADMINS

async def broadcast_messages(user_id, message, is_pin):
    try:
        # Message copy karna
        msg = await message.copy(chat_id=user_id)
        
        # Agar is_pin True hai, toh pin karega
        if is_pin:
            try:
                await msg.pin(both_sides=True)
            except Exception:
                pass # Pin fail hone par broadcast chalta rahega
                
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages(user_id, message, is_pin)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        return False, "Deleted"
    except UserIsBlocked:
        await db.delete_user(int(user_id))
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        return False, "Error"
    except Exception:
        return False, "Error"

async def process_broadcast(bot, message, is_pin):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    
    if not b_msg:
        return await message.reply_text("<b>⚠️ Reply to a message to start broadcast!</b>")
    
    sts = await message.reply_text(
        text=f"<b>🚀 Broadcasting {'with Pin' if is_pin else ''} started...</b>"
    )
    
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    blocked = 0
    deleted = 0
    failed = 0
    success = 0

    async for user in users:
        if 'id' in user:
            pti, sh = await broadcast_messages(int(user['id']), b_msg, is_pin)
            if pti:
                success += 1
            elif pti == False:
                if sh == "Blocked":
                    blocked += 1
                elif sh == "Deleted":
                    deleted += 1
                elif sh == "Error":
                    failed += 1
            done += 1
            
            # Progress status update
            if not done % 20:
                await sts.edit(
                    f"<b>**📢 Broadcast in progress:**</b>\n\n"
                    f"<b>Total Users:</b> {total_users}\n"
                    f"<b>Completed:</b> {done} / {total_users}\n"
                    f"<b>✅ Success:</b> {success}\n"
                    f"<b>🚫 Blocked:</b> {blocked}\n"
                    f"<b>🗑️ Deleted:</b> {deleted}"
                )    
        else:
            done += 1
            failed += 1
    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    
    # Final Result Message
    await sts.edit(
        f"<b>**✨ {'Pin ' if is_pin else ''}Broadcast Completed**</b>\n"
        f"<b>⏱️ Time: {time_taken} seconds.</b>\n\n"
        f"<b>Total Users:</b> {total_users}\n"
        f"<b>Success:</b> {success}\n"
        f"<b>Blocked:</b> {blocked}\n"
        f"<b>Deleted:</b> {deleted}"
    )

# --- COMMANDS ---

# Command: /broadcast
@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_only(bot, message):
    await process_broadcast(bot, message, is_pin=False)

# Command: /pin_broadcast
@Client.on_message(filters.command("pin_broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_with_pin(bot, message):
    await process_broadcast(bot, message, is_pin=True)

# Command: /stats
@Client.on_message(filters.command("stats") & filters.private & filters.user(ADMINS))
async def bot_stats(client: Client, message: Message):
    status_msg = await message.reply_text("<b>🔄 Fetching Statistics...</b>")
    try:
        total_users = await db.total_users_count()
        await status_msg.edit(
            f"<b>📊 <u>Bot Statistics</u></b>\n\n"
            f"<b>👤 Total Users:</b> <code>{total_users}</code>"
        )
    except Exception as e:
        await status_msg.edit(f"<b>❌ Error:</b> <code>{e}</code>")

# Command: /restart
@Client.on_message(filters.command("restart") & filters.private & filters.user(ADMINS))
async def restart_bot(client: Client, message: Message):
    try:
        msg = await message.reply_text("<b>♻️ Restarting bot system...</b>")
        await asyncio.sleep(2)
        await msg.edit("<b>✅ Restart successful!</b>")
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as e:
        await message.reply_text(f"<b>❌ Restart Failed:</b> <code>{e}</code>")

# Don't Remove Credit @VJ_Bots
# --- RESTART NOTIFICATION FUNCTION ---
async def send_restart_notification(bot):
    """Bot start hone par sabhi users ko 'bot restart' ka message bhejta hai"""
    users = await db.get_all_users()
    # Aapki request ke mutabik: bold aur lowercase (small) text
    restart_text = "<b>ʙᴏᴛ ʀᴇsᴛᴀʀᴛᴇᴅ !!</b>"
    
    async for user in users:
        if 'id' in user:
            try:
                await bot.send_message(chat_id=int(user['id']), text=restart_text)
                # Rate limit (FloodWait) se bachne ke liye thoda gap
                await asyncio.sleep(0.05) 
            except Exception:
                continue # Blocked ya invalid users ke liye skip

# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
from database.db import db
from pyrogram import Client, filters
from config import ADMINS
import asyncio
import datetime
import time

async def broadcast_messages(user_id, message):
    try:
        # Copying the message to the user
        msg = await message.copy(chat_id=user_id)
        try:
            # Pinning the broadcasted message
            await msg.pin(disable_notification=False)
        except Exception:
            # If pinning fails (e.g., user blocked or internal error), we skip it
            pass
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        return False, "Deleted"
    except UserIsBlocked:
        await db.delete_user(int(user_id))
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        return False, "Error"
    except Exception as e:
        return False, "Error"

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast(bot, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    if not b_msg:
        return await message.reply_text("<b>**Reply This Command To Your Broadcast Message**</b>")
    
    sts = await message.reply_text(
        text='<b>Broadcasting your messages...</b>'
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
            pti, sh = await broadcast_messages(int(user['id']), b_msg)
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
            
            # Progress update every 20 users
            if not done % 20:
                await sts.edit(
                    f"<b>**Broadcast in progress:**</b>\n\n"
                    f"<b>Total Users:</b> {total_users}\n"
                    f"<b>Completed:</b> {done} / {total_users}\n"
                    f"<b>Success:</b> {success}\n"
                    f"<b>Blocked:</b> {blocked}\n"
                    f"<b>Deleted:</b> {deleted}"
                )    
        else:
            done += 1
            failed += 1
    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    
    # Final Bold Message
    await sts.edit(
        f"<b>**Broadcast Completed**</b>\n"
        f"<b>Completed in {time_taken} seconds.</b>\n\n"
        f"<b>Total Users:</b> {total_users}\n"
        f"<b>Completed:</b> {done} / {total_users}\n"
        f"<b>Success:</b> {success}\n"
        f"<b>Blocked:</b> {blocked}\n"
        f"<b>Deleted:</b> {deleted}"
    )

# Don't Remove Credit @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

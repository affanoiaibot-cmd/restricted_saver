# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import asyncio 
import pyrogram
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message 
from config import API_ID, API_HASH, ERROR_MESSAGE, LOGIN_SYSTEM, STRING_SESSION, CHANNEL_ID, WAITING_TIME
from database.db import db
from TechVJ.strings import HELP_TXT
from bot import TechVJUser

class batch_temp(object):
    IS_BATCH = {}

# Download status writer
async def downstatus(client, statusfile, message, chat):
    while True:
        if os.path.exists(statusfile):
            break
        await asyncio.sleep(3)
      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as downread:
            txt = downread.read()
        try:
            await client.edit_message_text(chat, message.id, f"<b>📥 Downloaded:</b> <b>{txt}</b>")
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(5)

# Upload status writer
async def upstatus(client, statusfile, message, chat):
    while True:
        if os.path.exists(statusfile):
            break
        await asyncio.sleep(3)      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as upread:
            txt = upread.read()
        try:
            await client.edit_message_text(chat, message.id, f"<b>📤 Uploaded:</b> <b>{txt}</b>")
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(5)

# Progress percentage calculator
def progress(current, total, message, type):
    with open(f'{message.id}{type}status.txt', "w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")

# --- COMMANDS ---

@Client.on_message(filters.command(["start"]))
async def send_start(client: Client, message: Message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
    
    buttons = [
        [InlineKeyboardButton("🕸️ Developer", url="https://t.me/mineheartO")],
        [
            InlineKeyboardButton('🔍 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/restricted_unlock'),
            InlineKeyboardButton('🤖 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://t.me/restricted_unlock')
        ],
        [InlineKeyboardButton('🤖 Another Bot', url='https://t.me/affanoiupload_bot')]
    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
        chat_id=message.chat.id, 
        text=f"<b>👋 Hi {message.from_user.mention},</b>\n\n"
             f"<b>🚀 I am Restricted Content Saver Bot.</b>\n\n"
             f"<b>📦 I can help you to download restricted content via post links.</b>\n\n"
             f"<b>🔑 Please /login first to start downloading.</b>\n\n"
             f"<b>❓ Use /help to know how to use me.</b>", 
        reply_markup=reply_markup, 
        reply_to_message_id=message.id
    )

@Client.on_message(filters.command(["help"]))
async def send_help(client: Client, message: Message):
    await client.send_message(
        chat_id=message.chat.id, 
        text=f"<b>{HELP_TXT}</b>"
    )

@Client.on_message(filters.command(["cancel"]))
async def send_cancel(client: Client, message: Message):
    batch_temp.IS_BATCH[message.from_user.id] = True
    await client.send_message(
        chat_id=message.chat.id, 
        text="<b>❌ Batch Successfully Cancelled!</b>"
    )

# --- LINK HANDLING ---

@Client.on_message(filters.text & filters.private)
async def save(client: Client, message: Message):
    # Handling invite links
    if ("https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text) and LOGIN_SYSTEM == False:
        if TechVJUser is None:
            await client.send_message(message.chat.id, "<b>⚠️ String Session is not Set!</b>", reply_to_message_id=message.id)
            return
        try:
            try:
                await TechVJUser.join_chat(message.text)
            except Exception as e: 
                await client.send_message(message.chat.id, f"<b>❌ Error:</b> <code>{e}</code>", reply_to_message_id=message.id)
                return
            await client.send_message(message.chat.id, "<b>✅ Chat Joined Successfully!</b>", reply_to_message_id=message.id)
        except UserAlreadyParticipant:
            await client.send_message(message.chat.id, "<b>ℹ️ Chat already Joined.</b>", reply_to_message_id=message.id)
        except InviteHashExpired:
            await client.send_message(message.chat.id, "<b>🚫 Invalid Link or Expired.</b>", reply_to_message_id=message.id)
        return
    
    # Handling post links
    if "https://t.me/" in message.text:
        if batch_temp.IS_BATCH.get(message.from_user.id) == False:
            return await message.reply_text("<b>⚠️ One Task Is Already Processing!</b>\n\n<b>Please wait for it to complete or use /cancel.</b>")
        
        datas = message.text.split("/")
        temp_data = datas[-1].replace("?single","").split("-")
        fromID = int(temp_data[0].strip())
        try:
            toID = int(temp_data[1].strip())
        except:
            toID = fromID

        if LOGIN_SYSTEM == True:
            user_data = await db.get_session(message.from_user.id)
            if user_data is None:
                await message.reply("<b>🔒 For Downloading Restricted Content You Have To /login First.</b>")
                return
            api_id = int(await db.get_api_id(message.from_user.id))
            api_hash = await db.get_api_hash(message.from_user.id)
            try:
                acc = Client("saverestricted", session_string=user_data, api_hash=api_hash, api_id=api_id)
                await acc.connect()
            except:
                return await message.reply("<b>⚠️ Your Session Expired! Please /logout and /login again.</b>")
        else:
            if TechVJUser is None:
                await client.send_message(message.chat.id, f"<b>⚠️ String Session is not Set!</b>", reply_to_message_id=message.id)
                return
            acc = TechVJUser
                
        batch_temp.IS_BATCH[message.from_user.id] = False
        for msgid in range(fromID, toID+1):
            if batch_temp.IS_BATCH.get(message.from_user.id): break
            
            # Private Channel Link
            if "https://t.me/c/" in message.text:
                chatid = int("-100" + datas[4])
                try:
                    await handle_private(client, acc, message, chatid, msgid)
                except Exception as e:
                    if ERROR_MESSAGE == True:
                        await client.send_message(message.chat.id, f"<b>❌ Error:</b> <code>{e}</code>", reply_to_message_id=message.id)
    
            # Bot Link
            elif "https://t.me/b/" in message.text:
                username = datas[4]
                try:
                    await handle_private(client, acc, message, username, msgid)
                except Exception as e:
                    if ERROR_MESSAGE == True:
                        await client.send_message(message.chat.id, f"<b>❌ Error:</b> <code>{e}</code>", reply_to_message_id=message.id)
            
            # Public Channel Link
            else:
                username = datas[3]
                try:
                    msg = await client.get_messages(username, msgid)
                except UsernameNotOccupied: 
                    await client.send_message(message.chat.id, "<b>🚫 Username not occupied!</b>", reply_to_message_id=message.id)
                    return
                try:
                    await client.copy_message(message.chat.id, msg.chat.id, msg.id, reply_to_message_id=message.id)
                except:
                    try:    
                        await handle_private(client, acc, message, username, msgid)               
                    except Exception as e:
                        if ERROR_MESSAGE == True:
                            await client.send_message(message.chat.id, f"<b>❌ Error:</b> <code>{e}</code>", reply_to_message_id=message.id)

            await asyncio.sleep(WAITING_TIME)
            
        if LOGIN_SYSTEM == True:
            try:
                await acc.disconnect()
            except:
                pass                        
        batch_temp.IS_BATCH[message.from_user.id] = True

# --- MEDIA HANDLER ---

async def handle_private(client: Client, acc, message: Message, chatid, msgid: int):
    msg: Message = await acc.get_messages(chatid, msgid)
    if msg.empty: return 
    msg_type = get_message_type(msg)
    if not msg_type: return 
    
    chat = int(CHANNEL_ID) if CHANNEL_ID else message.chat.id
    
    if batch_temp.IS_BATCH.get(message.from_user.id): return 
    if "Text" == msg_type:
        try:
            await client.send_message(chat, msg.text, entities=msg.entities, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
            return 
        except Exception as e:
            if ERROR_MESSAGE == True:
                await client.send_message(message.chat.id, f"<b>❌ Error:</b> <code>{e}</code>", reply_to_message_id=message.id)
            return 

    smsg = await client.send_message(message.chat.id, '<b>⏳ Downloading...</b>', reply_to_message_id=message.id)
    asyncio.create_task(downstatus(client, f'{message.id}downstatus.txt', smsg, message.chat.id))
    
    try:
        file = await acc.download_media(msg, progress=progress, progress_args=[message,"down"])
        if os.path.exists(f'{message.id}downstatus.txt'):
            os.remove(f'{message.id}downstatus.txt')
    except Exception as e:
        if ERROR_MESSAGE == True:
            await client.send_message(message.chat.id, f"<b>❌ Download Error:</b> <code>{e}</code>", reply_to_message_id=message.id) 
        return await smsg.delete()
    
    if batch_temp.IS_BATCH.get(message.from_user.id): return 
    asyncio.create_task(upstatus(client, f'{message.id}upstatus.txt', smsg, message.chat.id))

    caption = msg.caption if msg.caption else None
    
    try:
        if "Document" == msg_type:
            thumb = await acc.download_media(msg.document.thumbs[0].file_id) if msg.document.thumbs else None
            await client.send_document(chat, file, thumb=thumb, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
            if thumb: os.remove(thumb)

        elif "Video" == msg_type:
            thumb = await acc.download_media(msg.video.thumbs[0].file_id) if msg.video.thumbs else None
            await client.send_video(chat, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=thumb, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
            if thumb: os.remove(thumb)

        elif "Animation" == msg_type:
            await client.send_animation(chat, file, reply_to_message_id=message.id)
            
        elif "Sticker" == msg_type:
            await client.send_sticker(chat, file, reply_to_message_id=message.id)     

        elif "Voice" == msg_type:
            await client.send_voice(chat, file, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])

        elif "Audio" == msg_type:
            thumb = await acc.download_media(msg.audio.thumbs[0].file_id) if msg.audio.thumbs else None
            await client.send_audio(chat, file, thumb=thumb, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
            if thumb: os.remove(thumb)

        elif "Photo" == msg_type:
            await client.send_photo(chat, file, caption=caption, reply_to_message_id=message.id)

    except Exception as e:
        if ERROR_MESSAGE == True:
            await client.send_message(message.chat.id, f"<b>❌ Upload Error:</b> <code>{e}</code>", reply_to_message_id=message.id)
    
    if os.path.exists(f'{message.id}upstatus.txt'): 
        os.remove(f'{message.id}upstatus.txt')
    
    if os.path.exists(file):
        os.remove(file)
        
    await smsg.delete()

def get_message_type(msg: pyrogram.types.Message):
    if msg.document: return "Document"
    if msg.video: return "Video"
    if msg.animation: return "Animation"
    if msg.sticker: return "Sticker"
    if msg.voice: return "Voice"
    if msg.audio: return "Audio"
    if msg.photo: return "Photo"
    if msg.text: return "Text"
    return None

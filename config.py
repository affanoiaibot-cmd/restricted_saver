# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os

# Login feature, if you want then True , if you don't want then False
LOGIN_SYSTEM = bool(os.environ.get('LOGIN_SYSTEM', True)) 

if LOGIN_SYSTEM == False:
    # if login system is False then fill your tg account session below 
    STRING_SESSION = os.environ.get("STRING_SESSION", "")
else:
    STRING_SESSION = None

# Bot token @Botfather
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Your API ID from my.telegram.org
API_ID = int(os.environ.get("API_ID", "35554205"))

# Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "7b56a1a17366fb67ba913ff0cbac6e67")

# --- IMPORTANT CHANGE: ADMINS must be a list ---
ADMINS = [8281644724] 

# Your Channel Id In Which Bot Uploads
CHANNEL_ID = os.environ.get("CHANNEL_ID", "")

# Your Mongodb Database Url
DB_URI = os.environ.get("DB_URI", "mongodb+srv://jaffernova21_db_user:kdcxktjJo6dEXEWm@cluster0.rdci8wh.mongodb.net/?appName=Cluster0")
DB_NAME = os.environ.get("DB_NAME", "vjsavecontentbot")

# Increase time to avoid floodwait
WAITING_TIME = int(os.environ.get("WAITING_TIME", "10")) 

# Error Message setting
ERROR_MESSAGE = bool(os.environ.get('ERROR_MESSAGE', True))

# --- NEW: Port for Koyeb Health Check ---
PORT = int(os.environ.get("PORT", "8080"))

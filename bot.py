# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ

import asyncio
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, STRING_SESSION, LOGIN_SYSTEM
from TechVJ.broadcast import send_restart_notification 
from threading import Thread
from app import run_web # app.py se function import kiya

# Global variable define kar rahe hain taaki dusre files me import ho sake
TechVJUser = None 

class Bot(Client):

    def __init__(self):
        super().__init__(
            "techvj login",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="TechVJ"),
            workers=150,
            sleep_threshold=5
        )

    async def start(self):
        await super().start()
        print('Bot Started Powered By @VJ_Bots')
        
        # User Client Session Check & Start (Async tareeqe se)
        global TechVJUser
        if STRING_SESSION is not None and LOGIN_SYSTEM == False:
            try:
                TechVJUser = Client("TechVJ", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)
                await TechVJUser.start()
                print("Userbot (String Session) globally start ho gaya hai!")
            except Exception as e:
                print(f"Userbot Start hone mein error aayi: {e}")
        else:
            TechVJUser = None
        
        # Background task for restart notification
        try:
            # Isse bot commands ke liye turant ready ho jayega
            asyncio.create_task(send_restart_notification(self))
            print("Restart notification background loop mein start ho gayi hai!")
        except Exception as e:
            print(f"Notification Error: {e}")

    async def stop(self, *args):
        global TechVJUser
        if TechVJUser:
            try:
                await TechVJUser.stop()
            except:
                pass
        await super().stop()
        print('Bot Stopped. Bye!')

if __name__ == "__main__":
    # 1. Flask server ko alag thread mein start karein (Daemon = True)
    # Ye Koyeb ko "Healthy" signal bhejne ke liye zaroori hai
    print("Starting Health Check Web Server...")
    t = Thread(target=run_web)
    t.daemon = True # Isse bot ke saath server properly manage hoga
    t.start()
    
    # 2. Pyrogram Bot ko start karein
    bot = Bot()
    bot.run()

from flask import Flask
import logging
from config import PORT # config.py se PORT import kiya

# Flask ke faltu pings (health checks) logs mein na dikhein, uske liye:
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/')
def hello_world():
    # Jab Koyeb is link par aayega, use ye message milega
    return 'VJ Bots - Bot is Running Live and Healthy!'

def run_web():
    # '0.0.0.0' isliye zaroori hai taaki Koyeb bot ko internet se connect kar sake
    # Port ko ab config.py se dynamically liya ja raha hai
    app.run(host='0.0.0.0', port=PORT)

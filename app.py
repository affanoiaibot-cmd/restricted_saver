from flask import Flask
import logging

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
    # Port 8080 Koyeb ki default setting hoti hai
    app.run(host='0.0.0.0', port=8080)

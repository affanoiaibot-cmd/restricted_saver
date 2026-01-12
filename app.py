from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    # Ye text Koyeb ke logs mein dikhega
    return 'VJ Bots - Bot is Running Live and Healthy!'

def run_web():
    # Koyeb ke liye 0.0.0.0 aur port 8080 zaroori hai
    app.run(host='0.0.0.0', port=8080)

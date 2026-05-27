import subprocess
from threading import Thread
from flask import Flask
import os
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram Bots are running perfectly!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    print("Starting Web Server...")
    t = Thread(target=run_flask)
    t.start()
    
    time.sleep(2)
    print("Starting Telegram Bots...")
    p1 = subprocess.Popen(["python3", "tele/bot.py"])
    p2 = subprocess.Popen(["python3", "JF BOT/bot.py"])
    
    try:
        p1.wait()
        p2.wait()
    except KeyboardInterrupt:
        p1.terminate()
        p2.terminate()

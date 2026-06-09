import os
import shutil

os.makedirs("/Users/cashify/Desktop/NewClientBot", exist_ok=True)
src = "/Users/cashify/Desktop/jf_bot_deploy/JF BOT/bot.py"
dst = "/Users/cashify/Desktop/NewClientBot/bot.py"

shutil.copy(src, dst)
print("Folder and file created successfully.")

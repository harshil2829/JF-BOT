import asyncio
from telegram import Bot
import os
from pymongo import MongoClient

TOKEN = "7994962595:AAGOZdezJAetEVJPCpbOVqAds7AYaypWlRY"
MONGO_URI = "mongodb+srv://admin:HARSHIL2829@cluster0.6kcmggh.mongodb.net/?appName=Cluster0"

async def main():
    client = MongoClient(MONGO_URI)
    db = client['TelegramBotDB']
    jf_col = db['jf_data']

    doc = jf_col.find_one({"_id": "balances"})
    balances = doc.get("data", {}) if doc else {}

    sorted_bals = sorted(balances.items(), key=lambda x: x[1], reverse=True)
    
    bot = Bot(TOKEN)
    
    print("Fetching Telegram names for top 5 balances...")
    for uid_str, bal in sorted_bals[:5]:
        uid = int(uid_str)
        try:
            chat = await bot.get_chat(uid)
            name = chat.first_name
            if chat.last_name:
                name += f" {chat.last_name}"
            username = f" (@{chat.username})" if chat.username else ""
            print(f"User: {name}{username} | ID: {uid} | Balance: ₹{bal}")
        except Exception as e:
            print(f"User ID: {uid} (Name Unknown - {e}) | Balance: ₹{bal}")

if __name__ == "__main__":
    asyncio.run(main())

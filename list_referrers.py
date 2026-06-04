import asyncio
import os
import sys
from telegram import Bot
sys.path.append(os.path.abspath("JF BOT"))
import bot

async def main():
    bot_client = Bot(token="7994962595:AAGOZdezJAetEVJPCpbOVqAds7AYaypWlRY")
    refs = bot.load_referrals()
    users = refs.get("users", {})
    
    print("=== ALL REFERRAL EARNINGS ===")
    
    # Sort users by count descending
    sorted_users = sorted(users.items(), key=lambda x: x[1]['count'], reverse=True)
    
    for uid, stats in sorted_users:
        if stats["count"] > 0:
            name = "Unknown"
            uname = ""
            try:
                chat = await bot_client.get_chat(int(uid))
                name = chat.first_name
                if chat.username:
                    uname = f"(@{chat.username})"
            except Exception:
                pass
                
            print(f"User: {name} {uname} (ID: {uid})")
            print(f"  Referrals: {stats['count']}")
            print(f"  Earnings: ₹{stats['earnings']}")
            print("-" * 30)

asyncio.run(main())

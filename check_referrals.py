import os
import sys
sys.path.append(os.path.abspath("JF BOT"))
import bot

refs = bot.load_referrals()
referred = refs.get("referred", [])
print("Total referred users:", len(referred))
print("Unique referred users:", len(set(referred)))

users = refs.get("users", {})
for uid, stats in users.items():
    if stats["count"] > 10:
        print(f"User {uid} has {stats['count']} referrals.")

import os
import sys
sys.path.append(os.path.abspath("JF BOT"))
import bot

bals = bot.load_balances()
refs = bot.load_referrals()

restored_count = 0
if "users" in refs:
    for uid, stats in refs["users"].items():
        earnings = stats.get("earnings", 0.0)
        if earnings > 0:
            uid_str = str(uid)
            # Add earnings to their balance
            bals[uid_str] = bals.get(uid_str, 0.0) + earnings
            restored_count += 1
            print(f"Restored ₹{earnings} to user {uid_str}. New balance: ₹{bals[uid_str]}")

    bot.save_balances(bals)
    print(f"\\nSuccessfully restored referral balances for {restored_count} users!")
else:
    print("No referral users found.")

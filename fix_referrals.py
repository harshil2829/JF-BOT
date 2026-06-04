import os
import sys
sys.path.append(os.path.abspath("JF BOT"))
import bot

bals = bot.load_balances()
refs = bot.load_referrals()

print("Current Balances:", bals)
if "users" in refs:
    print("Referral Stats:", refs["users"])
else:
    print("No referral users found.")

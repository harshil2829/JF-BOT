import os
import sys
sys.path.append(os.path.abspath("JF BOT"))
import bot

bals = bot.load_balances()
print("Balances:", bals)

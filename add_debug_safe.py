import os
import re

with open("JF BOT/bot.py", "r") as f:
    code = f.read()

debug_func = """def debug_log(msg):
    logs = jf_col.find_one({"_id": "debug_logs"})
    data = logs["data"] if logs else []
    data.append(msg)
    jf_col.update_one({"_id": "debug_logs"}, {"$set": {"data": data[-100:]}}, upsert=True)
"""

if "def debug_log" not in code:
    code = code.replace("def load_balances():", debug_func + "\ndef load_balances():")

# Replace walletpay_
old_wallet = """    elif data.startswith("walletpay_"):
        order_id = data.split("_")[1]"""
new_wallet = """    elif data.startswith("walletpay_"):
        debug_log(f"Clicked walletpay: {data}")
        order_id = data.split("_")[1]"""
code = code.replace(old_wallet, new_wallet)

old_check = """            if delivered_key:
                resellers_check = load_resellers()"""
new_check = """            debug_log(f"Delivered key: {delivered_key}")
            if delivered_key:
                resellers_check = load_resellers()"""
code = code.replace(old_check, new_check)

old_bal = """        if user_bal >= amount:
            balances[user_id_str] -= amount"""
new_bal = """        debug_log(f"user_bal: {user_bal}, amount: {amount}")
        if user_bal >= amount:
            debug_log("Sufficient balance")
            balances[user_id_str] -= amount"""
code = code.replace(old_bal, new_bal)

old_log = """                    log_reseller_action(username_str, user_id_str, product, delivered_key)
                
                success_msg = ("""
new_log = """                    debug_log("Calling log_reseller_action")
                    log_reseller_action(username_str, user_id_str, product, delivered_key)
                    debug_log("log_reseller_action finished")
                
                success_msg = ("""
code = code.replace(old_log, new_log)

old_edit = """                await query.edit_message_text(text=success_msg, parse_mode="HTML")
            else:"""
new_edit = """                debug_log("Editing success msg")
                await query.edit_message_text(text=success_msg, parse_mode="HTML")
                debug_log("Edited success msg")
            else:"""
code = code.replace(old_edit, new_edit)

with open("JF BOT/bot.py", "w") as f:
    f.write(code)

print("Debug added safely")

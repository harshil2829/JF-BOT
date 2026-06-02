import os
import re

with open("JF BOT/bot.py", "r") as f:
    code = f.read()

debug_func = """def debug_log(msg):
    logs = jf_col.find_one({"_id": "debug_logs"})
    data = logs["data"] if logs else []
    data.append(msg)
    jf_col.update_one({"_id": "debug_logs"}, {"$set": {"data": data}}, upsert=True)
"""

if "def debug_log" not in code:
    code = code.replace("def load_balances():", debug_func + "\ndef load_balances():")

# Replace walletpay_
old_wallet = """    elif data.startswith("walletpay_"):
        order_id = data.split("_")[1]
        amount = float(context.user_data.get("amount", "0"))"""
new_wallet = """    elif data.startswith("walletpay_"):
        debug_log(f"Clicked walletpay: {data}")
        try:
            order_id = data.split("_")[1]
            amount = float(context.user_data.get("amount", "0"))
            debug_log(f"Amount: {amount}")"""

if "debug_log(f\"Clicked walletpay" not in code:
    code = code.replace(old_wallet, new_wallet)

old_check = """            if delivered_key:
                resellers_check = load_resellers()"""
new_check = """            debug_log(f"Delivered key: {delivered_key}")
            if delivered_key:
                resellers_check = load_resellers()"""
if "debug_log(f\"Delivered key" not in code:
    code = code.replace(old_check, new_check)

old_edit = """                await query.edit_message_text(text=success_msg, parse_mode="HTML")
            else:"""
new_edit = """                debug_log("Editing success msg")
                await query.edit_message_text(text=success_msg, parse_mode="HTML")
                debug_log("Edited success msg")
            else:"""
if "debug_log(\"Editing success msg\")" not in code:
    code = code.replace(old_edit, new_edit)

old_refund = """                await query.edit_message_text("❌ Payment refunded due to out-of-stock. Please contact Admin.")
        else:"""
new_refund = """                debug_log("Editing refunded msg")
                await query.edit_message_text("❌ Payment refunded due to out-of-stock. Please contact Admin.")
                debug_log("Edited refunded msg")
        else:"""
if "debug_log(\"Editing refunded msg\")" not in code:
    code = code.replace(old_refund, new_refund)
    
old_except = """            await query.answer("❌ Insufficient balance!", show_alert=True)"""
new_except = """            debug_log("Insufficient balance")
            await query.answer("❌ Insufficient balance!", show_alert=True)
        except Exception as e:
            debug_log(f"EXCEPTION in walletpay: {e}")"""
if "EXCEPTION in walletpay" not in code:
    code = code.replace(old_except, new_except)

with open("JF BOT/bot.py", "w") as f:
    f.write(code)

print("Debug added")

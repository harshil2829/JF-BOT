import os

with open("JF BOT/bot.py", "r") as f:
    code = f.read()

# 1. Add History Functions at the top
history_funcs = """
def load_user_history(user_id):
    doc = jf_col.find_one({"_id": f"history_{user_id}"})
    if doc and isinstance(doc.get("data"), list):
        return doc["data"]
    return []

def log_user_action(user_id, product, key):
    from datetime import datetime
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_str = f"• {time_str}\\n🏺 {product.upper()}\\n🔑 <code>{key}</code>\\n"
    logs = load_user_history(user_id)
    logs.append(log_str)
    if len(logs) > 50: logs = logs[-50:]
    jf_col.update_one({"_id": f"history_{user_id}"}, {"$set": {"data": logs}}, upsert=True)
"""
# Insert after save_reseller_logs
code = code.replace("def log_reseller_action(username, user_id, product, key):", history_funcs + "\ndef log_reseller_action(username, user_id, product, key):")

# 2. Add to walletpay_
old_wallet = '                    log_reseller_action(username_str, user_id_str, product, delivered_key)\n                    debug_log("log_reseller_action finished")'
new_wallet = old_wallet + '\n                log_user_action(user_id_str, product, delivered_key)'
code = code.replace(old_wallet, new_wallet)

# 3. Add to approve_
old_approve = """            if target_str in resellers_check:
                # We don't have their username easily here, so we just use "Reseller"
                log_reseller_action("Reseller", target_str, product, delivered_key)
                
            # Send Key to User"""
new_approve = """            if target_str in resellers_check:
                # We don't have their username easily here, so we just use "Reseller"
                log_reseller_action("Reseller", target_str, product, delivered_key)
            log_user_action(target_user_id, product, delivered_key)
                
            # Send Key to User"""
code = code.replace(old_approve, new_approve)

# 4. Modify 'history' callback
old_history = """    elif data == "history":
        await query.edit_message_text(
            "💰 <b>ORDER HISTORY</b>\\n"
            "━━━━━━━━━━━━━━━━━━\\n"
            "❌ <b>No orders found!</b>\\n\\n"
            "Your previous purchases will appear here once they are verified.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Back", callback_data="main_menu")]]),
            parse_mode="HTML"
        )"""

# Wait, old_history text was actually:
old_history_real = """    elif data == "history":
        await query.edit_message_text(
            "📋 <b>ORDER HISTORY</b>\\n"
            "━━━━━━━━━━━━━━━━━━\\n"
            "❌ <b>No orders found!</b>\\n\\n"
            "Your previous purchases will appear here once they are verified.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Back", callback_data="main_menu")]]),
            parse_mode="HTML"
        )"""

new_history = """    elif data == "history":
        logs = load_user_history(query.from_user.id)
        if logs:
            history_text = "\\n".join(logs[-10:])
            text = f"📋 <b>YOUR ORDER HISTORY</b>\\n━━━━━━━━━━━━━━━━━━\\n{history_text}\\n<i>Showing your last 10 purchases.</i>"
        else:
            text = (
                "📋 <b>ORDER HISTORY</b>\\n"
                "━━━━━━━━━━━━━━━━━━\\n"
                "❌ <b>No orders found!</b>\\n\\n"
                "Your previous purchases will appear here once they are verified."
            )
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Back", callback_data="main_menu")]]), parse_mode="HTML")"""
code = code.replace(old_history_real, new_history)

with open("JF BOT/bot.py", "w") as f:
    f.write(code)

print("Patch 8 applied")

import os

with open("JF BOT/bot.py", "r") as f:
    code = f.read()

# 1. Update load_reseller_logs to strictly return list
old_load = """def load_reseller_logs():
    doc = jf_col.find_one({"_id": "reseller_logs"})
    return doc["data"] if doc else []"""

new_load = """def load_reseller_logs():
    doc = jf_col.find_one({"_id": "reseller_logs"})
    if doc and isinstance(doc.get("data"), list):
        return doc["data"]
    return []"""
code = code.replace(old_load, new_load)

# 2. Fix len(logs[target_id]) to len(user_logs) in /rlogs
old_rlogs = """    text += f"\\n<i>Total keys generated: {len(logs[target_id])}</i>"
    await update.message.reply_text(text, parse_mode="HTML")"""

new_rlogs = """    text += f"\\n<i>Total keys generated: {len(user_logs)}</i>"
    await update.message.reply_text(text, parse_mode="HTML")"""
code = code.replace(old_rlogs, new_rlogs)

# 3. Fix len(logs[target_id]) to len(user_logs) in admin_panel_cb
old_adminlogs = """        text += f"\\n<i>Total keys generated: {len(logs[target_id])}</i>"
        kb = [[InlineKeyboardButton("« Back", callback_data="admin_panel_cb")]]; await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")"""

new_adminlogs = """        text += f"\\n<i>Total keys generated: {len(user_logs)}</i>"
        kb = [[InlineKeyboardButton("« Back", callback_data="admin_panel_cb")]]; await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")"""
code = code.replace(old_adminlogs, new_adminlogs)

with open("JF BOT/bot.py", "w") as f:
    f.write(code)

print("Patch 6 applied")

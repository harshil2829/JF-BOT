import sys

file_path = "/Users/cashify/Desktop/jf_bot_deploy/JF BOT/bot.py"
with open(file_path, "r") as f:
    code = f.read()

helpers = """
def load_web_settings():
    doc = jf_col.find_one({"_id": "web_settings"})
    return doc.get("data", {}) if doc else {}

def load_web_staff():
    doc = jf_col.find_one({"_id": "web_staff"})
    return doc.get("data", []) if doc else []

def load_web_products():
    doc = jf_col.find_one({"_id": "web_products"})
    return doc.get("data", []) if doc else []

def log_activity(user_id, action):
    doc = jf_col.find_one({"_id": "bot_activity_logs"})
    logs = doc.get("data", []) if doc else []
    import datetime
    logs.append({"uid": str(user_id), "action": action, "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    if len(logs) > 50: logs = logs[-50:]
    jf_col.update_one({"_id": "bot_activity_logs"}, {"$set": {"data": logs}}, upsert=True)

"""

if "def log_activity" not in code:
    code = code.replace("def load_settings():", helpers + "def load_settings():")

# Patch Start Command
if "log_activity(user_id, 'started the bot')" not in code:
    code = code.replace("save_user(user_id)", "save_user(user_id)\n    log_activity(user_id, 'started the bot')")

# Patch /ban command
if "log_activity(update.effective_user.id, f'banned user {target_id}')" not in code:
    code = code.replace("await update.message.reply_text(f\"✅ User {target_id} has been banned.\")",
                        "await update.message.reply_text(f\"✅ User {target_id} has been banned.\")\n        log_activity(update.effective_user.id, f'banned user {target_id}')")

# Patch Key Generation (Trial & Reseller & Buying)
if "log_activity(user_id, f'generated {product} key')" not in code:
    code = code.replace("log_user_action(user_id, product, key)", "log_user_action(user_id, product, key)\n    log_activity(user_id, f'generated {product} key')")
    code = code.replace("log_reseller_action(username, user_id, product, key)", "log_reseller_action(username, user_id, product, key)\n    log_activity(user_id, f'reseller generated {product} key')")

with open(file_path, "w") as f:
    f.write(code)

print("Patched bot.py successfully!")

import os

with open("JF BOT/bot.py", "r") as f:
    code = f.read()

# 1. Update load_reseller_perms & save_reseller_perms
old_perms = """def load_reseller_perms():
    if not os.path.exists("reseller_perms.json"): return {}
    with open("reseller_perms.json", "r") as f: return json.load(f)

def save_reseller_perms(perms):
    with open("reseller_perms.json", "w") as f: json.dump(perms, f, indent=4)"""

new_perms = """def load_reseller_perms():
    doc = jf_col.find_one({"_id": "reseller_perms"})
    return doc["data"] if doc else {}

def save_reseller_perms(perms):
    jf_col.update_one({"_id": "reseller_perms"}, {"$set": {"data": perms}}, upsert=True)"""
code = code.replace(old_perms, new_perms)

# 2. Update load_referrals & save_referrals
old_refs = """def load_referrals():
    if not os.path.exists("referrals.json"): return {}
    with open("referrals.json", "r") as f: return json.load(f)

def save_referrals(refs):
    with open("referrals.json", "w") as f: json.dump(refs, f, indent=4)"""

new_refs = """def load_referrals():
    doc = jf_col.find_one({"_id": "referrals"})
    return doc["data"] if doc else {}

def save_referrals(refs):
    jf_col.update_one({"_id": "referrals"}, {"$set": {"data": refs}}, upsert=True)"""
code = code.replace(old_refs, new_refs)

# 3. Add Download APK to get_main_menu_keyboard
old_menu = """    keyboard = [
        [
            InlineKeyboardButton("🛒 Shop Store Now", callback_data="shop"),
            InlineKeyboardButton("🎁 My Profile", callback_data="profile")
        ],"""
new_menu = """    keyboard = [
        [
            InlineKeyboardButton("🛒 Shop Store Now", callback_data="shop"),
            InlineKeyboardButton("🎁 My Profile", callback_data="profile")
        ],
        [InlineKeyboardButton("📥 Download APK", url="https://t.me/JFFREEAPK")],"""
code = code.replace(old_menu, new_menu)

# 4. Add remove_balance_cmd
old_add_bal = """async def add_balance_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):"""
new_remove_bal = """async def remove_balance_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]: return
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /remove_balance [user_id] [amount]")
        return
    
    target_id = context.args[0]
    try: amount = float(context.args[1])
    except: return await update.message.reply_text("Invalid amount.")
    
    balances = load_balances()
    current = balances.get(target_id, 0.0)
    balances[target_id] = max(0.0, current - amount)
    save_balances(balances)
    
    await update.message.reply_text(f"✅ Removed ₹{amount} from user {target_id}. New Balance: ₹{balances[target_id]}")
    try:
        await context.bot.send_message(chat_id=target_id, text=f"💰 <b>Admin removed ₹{amount} from your wallet.</b>\\nNew Balance: ₹{balances[target_id]}", parse_mode="HTML")
    except: pass

async def add_balance_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):"""
code = code.replace(old_add_bal, new_remove_bal)

old_handlers = """    application.add_handler(CommandHandler("add_balance", add_balance_cmd))"""
new_handlers = """    application.add_handler(CommandHandler("add_balance", add_balance_cmd))
    application.add_handler(CommandHandler("remove_balance", remove_balance_cmd))"""
code = code.replace(old_handlers, new_handlers)

with open("JF BOT/bot.py", "w") as f:
    f.write(code)

print("Patch 3 applied")

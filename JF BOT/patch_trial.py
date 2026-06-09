import re

with open("bot.py", "r") as f:
    content = f.read()

# 1. Imports
if "from telegram.ext import" in content and "ChatMemberHandler" not in content:
    content = content.replace(
        "from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler",
        "from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, ChatMemberHandler"
    )
if "from telegram import" in content and "ChatMemberUpdated" not in content:
    content = content.replace(
        "from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup",
        "from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ChatMemberUpdated"
    )

# 2. File Constants
if "TRIAL_LOGS_FILE" not in content:
    content = content.replace(
        "RESELLER_LOGS_FILE = \"reseller_logs.json\"",
        "RESELLER_LOGS_FILE = \"reseller_logs.json\"\nTRIAL_LOGS_FILE = \"trial_logs.json\""
    )

# 3. Functions
funcs = """
def load_trials():
    if not os.path.exists(TRIAL_LOGS_FILE): return {}
    with open(TRIAL_LOGS_FILE, "r") as f:
        try: return json.load(f)
        except: return {}

def save_trials(data):
    with open(TRIAL_LOGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def is_banned(user_id):
    trials = load_trials()
    return trials.get(str(user_id), {}).get("banned", False)

async def chat_member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member
    if not result: return
    user_id = str(result.new_chat_member.user.id)
    if result.new_chat_member.status in ['left', 'kicked']:
        trials = load_trials()
        if user_id not in trials:
            trials[user_id] = {"last_trial": 0, "strikes": 0, "banned": False}
        trials[user_id]["strikes"] += 1
        if trials[user_id]["strikes"] >= 3:
            trials[user_id]["banned"] = True
        save_trials(trials)

"""
if "def load_trials():" not in content:
    content = content.replace(
        "def load_users():",
        funcs + "def load_users():"
    )

# 4. Handlers Check logic
# Start
if "def start" in content and "if is_banned(user_id):" not in content:
    content = re.sub(
        r'(async def start.*?user_id = update\.effective_user\.id\n)',
        r'\1    if is_banned(user_id):\n        await update.message.reply_text("🚫 You are banned from this bot for abusing the trial system.")\n        return\n',
        content,
        flags=re.DOTALL
    )

# Message handler
if "def message_handler" in content and "if is_banned" not in content:
    content = re.sub(
        r'(async def message_handler.*?settings = load_settings\(\)\n)',
        r'\1    if is_banned(update.effective_user.id):\n        return\n',
        content,
        flags=re.DOTALL
    )

# 5. Button logic for trials
trial_logic = """
    if is_banned(update.effective_user.id):
        await query.answer("🚫 You are banned.", show_alert=True)
        return

    if data == "trial_key":
        keyboard = [
            [InlineKeyboardButton("𖤍 HXN CHEAT", callback_data="claim_trial_hxn"), InlineKeyboardButton("♆ LK TEAM", callback_data="claim_trial_lk")],
            [InlineKeyboardButton("⚔️ HEX BLADE", callback_data="claim_trial_hex"), InlineKeyboardButton("🐺 ALPHA X", callback_data="claim_trial_alpha")],
            [InlineKeyboardButton("☢️ BOYYAH MOD", callback_data="claim_trial_boyyah"), InlineKeyboardButton("❂ NGO TRAN", callback_data="claim_trial_ngo")],
            [InlineKeyboardButton("⛃ GREED CHEAT", callback_data="claim_trial_greed")],
            [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="main_menu")]
        ]
        await query.edit_message_text("🎁 <b>TRIAL KEYS</b>\n\nSelect a product to get a 1-Day Trial Key.\n⚠️ <i>You can only claim ONE trial key every 3 days. Leaving the channel to cheat will result in a PERMANENT BAN.</i>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
        return
        
    if data.startswith("claim_trial_"):
        product = data.split("_")[2]
        user_id = str(update.effective_user.id)
        
        # Check channel
        if not await check_force_sub(update.effective_user.id, context):
            await query.answer("⚠️ You must join the channel first!", show_alert=True)
            return
            
        trials = load_trials()
        user_trial = trials.get(user_id, {"last_trial": 0, "strikes": 0, "banned": False})
        
        # 3 day check
        three_days = 3 * 24 * 60 * 60
        time_since_last = time.time() - user_trial["last_trial"]
        if time_since_last < three_days:
            wait_time = int((three_days - time_since_last) / 3600)
            await query.answer(f"⏳ You must wait {wait_time} hours before claiming another trial.", show_alert=True)
            return
            
        # Give key
        keys = load_keys()
        dict_key = f"{product}_1d"
        if dict_key in keys and len(keys[dict_key]) > 0:
            delivered_key = keys[dict_key].pop(0)
            save_keys(keys)
            
            user_trial["last_trial"] = time.time()
            trials[user_id] = user_trial
            save_trials(trials)
            
            await query.edit_message_text(f"✅ <b>TRIAL KEY GENERATED</b>\n━━━━━━━━━━━━━━━━━━\n🏺 <b>Product:</b> {product.upper()}\n🔑 <b>Key:</b> <code>{delivered_key}</code>\n\n<i>Enjoy your trial! Do not leave the channel, or you will be banned.</i>", parse_mode="HTML")
        else:
            await query.answer(f"❌ No trial keys available for {product.upper()} right now. Ask Admin to restock.", show_alert=True)
        return
"""

if "if data == \"trial_key\":" not in content:
    content = content.replace(
        "    if data == \"shop\":",
        trial_logic + "\n    if data == \"shop\":"
    )

# 6. Add handler in main()
if "ChatMemberHandler(chat_member_update" not in content:
    content = content.replace(
        "application.add_handler(CallbackQueryHandler(button_handler))",
        "application.add_handler(CallbackQueryHandler(button_handler))\n    application.add_handler(ChatMemberHandler(chat_member_update, ChatMemberHandler.CHAT_MEMBER))"
    )

with open("bot.py", "w") as f:
    f.write(content)

print("Patched successfully!")

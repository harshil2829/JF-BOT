import logging
import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://admin:HARSHIL2829@cluster0.6kcmggh.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI, connectTimeoutMS=5000, socketTimeoutMS=5000, maxIdleTimeMS=30000, retryWrites=True)
db = client['TelegramBotDB']
jf_col = db['jf_data']

import asyncio
import json
import random
import string
import time
import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ChatMemberUpdated
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, ChatMemberHandler, ChatJoinRequestHandler
import httpx

# Enable logging
import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# CONFIGURATION
TOKEN = "7994962595:AAGOZdezJAetEVJPCpbOVqAds7AYaypWlRY"
UPI_GATEWAY_TOKEN = "7994962595:AAGOZdezJAetEVJPCpbOVqAds7AYaypWlRY" 
IS_AUTO_MODE = False

import time
_CACHE = {}
_CACHE_TTL = 10 # 10 seconds TTL to drastically reduce DB load

def get_cached(key, default):
    now = time.time()
    if key in _CACHE:
        data, ts = _CACHE[key]
        if now - ts < _CACHE_TTL:
            return data
    doc = jf_col.find_one({"_id": key})
    if doc and "data" in doc:
        data = doc["data"]
    else:
        data = default
    _CACHE[key] = (data, now)
    return data

def set_cached(key, data):
    _CACHE[key] = (data, time.time())
    jf_col.update_one({"_id": key}, {"$set": {"data": data}}, upsert=True)

def load_web_settings():
    return get_cached("web_settings", {})

def load_web_staff():
    return get_cached("web_staff", [])

def load_web_products():
    return get_cached("web_products", [])

def save_web_products(products):
    set_cached("web_products", products)

def check_use_api(product):
    try:
        products = load_web_products()
        for p in products:
            if p.get("name", "").lower() == product.lower():
                if p.get("use_api") is not None:
                    return p.get("use_api")
    except Exception as e:
        logger.error(f"Error checking check_use_api: {e}")
    return product.lower() in ["hxn", "prime", "harshil", "hxnmodule"]

def log_activity(user_id, action):
    doc = jf_col.find_one({"_id": "bot_activity_logs"})
    logs = doc.get("data", []) if doc else []
    import datetime
    logs.append({"uid": str(user_id), "action": action, "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    if len(logs) > 50: logs = logs[-50:]
    jf_col.update_one({"_id": "bot_activity_logs"}, {"$set": {"data": logs}}, upsert=True)

def load_settings():
    settings = get_cached("settings", {"admin_ids": [12345678]})
    web_staff = load_web_staff()
    staff_ids = [int(s.get("telegram_id")) for s in web_staff if s.get("telegram_id") and str(s.get("telegram_id")).isdigit()]
    admin_ids = settings.get("admin_ids", [])
    for sid in staff_ids:
        if sid not in admin_ids:
            admin_ids.append(sid)
    settings["admin_ids"] = admin_ids
    return settings

def save_settings(settings):
    set_cached("settings", settings)

def load_trials():
    return get_cached("trials", {})

def save_trials(data):
    set_cached("trials", data)

def load_global_stats():
    return get_cached("global_stats", {"total_keys_used": 0})

def save_global_stats(stats):
    set_cached("global_stats", stats)

def load_waitlists():
    doc = jf_col.find_one({"_id": "waitlists"})
    return doc.get("data", {}) if doc else {}

def save_waitlists(wl):
    jf_col.update_one({"_id": "waitlists"}, {"$set": {"data": wl}}, upsert=True)

def increment_total_keys():
    stats = load_global_stats()
    stats["total_keys_used"] = stats.get("total_keys_used", 0) + 1
    save_global_stats(stats)

def load_balances():
    return get_cached("balances", {})

def save_balances(balances):
    set_cached("balances", balances)

def load_keys():
    return get_cached("keys", {})

def save_keys(keys):
    set_cached("keys", keys)

def load_users():
    doc = jf_col.find_one({"_id": "users"})
    return doc["data"] if doc else []

def save_user(user_id, username=None):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        jf_col.update_one({"_id": "users"}, {"$set": {"data": users}}, upsert=True)
    if username:
        save_username_mapping(user_id, username)

def save_username_mapping(user_id, username):
    if not username: return
    user_id = str(user_id)
    username = username.lower().replace("@", "").strip()
    
    doc = jf_col.find_one({"_id": "username_mappings"})
    mappings = doc["data"] if doc else {}
    if mappings.get(username) != user_id:
        mappings[username] = user_id
        jf_col.update_one({"_id": "username_mappings"}, {"$set": {"data": mappings}}, upsert=True)

def get_user_id_by_username(username):
    username = username.lower().replace("@", "").strip()
    doc = jf_col.find_one({"_id": "username_mappings"})
    mappings = doc["data"] if doc else {}
    return mappings.get(username)

def load_verified_users():
    doc = jf_col.find_one({"_id": "verified_users"})
    return doc["data"] if doc else []

def load_trial_history():
    doc = jf_col.find_one({"_id": "trial_history"})
    return doc["data"] if doc else []

def save_trial_history(hist):
    jf_col.update_one({"_id": "trial_history"}, {"$set": {"data": hist}}, upsert=True)

def save_verified_user(user_id):
    verified = load_verified_users()
    if user_id not in verified:
        verified.append(user_id)
        jf_col.update_one({"_id": "verified_users"}, {"$set": {"data": verified}}, upsert=True)

def load_utr_log():
    doc = jf_col.find_one({"_id": "utr_log"})
    return doc["data"] if doc else []

def save_utr(utr):
    log = load_utr_log()
    if utr not in log:
        log.append(utr)
        jf_col.update_one({"_id": "utr_log"}, {"$set": {"data": log}}, upsert=True)

def debug_log(msg):
    logs = jf_col.find_one({"_id": "debug_logs"})
    data = logs["data"] if logs else []
    data.append(msg)
    jf_col.update_one({"_id": "debug_logs"}, {"$set": {"data": data[-100:]}}, upsert=True)

def load_resellers():
    doc = jf_col.find_one({"_id": "resellers"})
    return doc["data"] if doc else {}

def save_resellers(resellers):
    jf_col.update_one({"_id": "resellers"}, {"$set": {"data": resellers}}, upsert=True)

def load_reseller_logs():
    doc = jf_col.find_one({"_id": "reseller_logs"})
    if doc and isinstance(doc.get("data"), list):
        return doc["data"]
    return []

def save_reseller_logs(username, user_id, product, key):
    logs = load_reseller_logs()
    from datetime import datetime
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logs.append(f"{time_str} - {username} ({user_id}) gen {product}: {key}")
    if len(logs) > 50: logs = logs[-50:]
    jf_col.update_one({"_id": "reseller_logs"}, {"$set": {"data": logs}}, upsert=True)

def load_referrals():
    doc = jf_col.find_one({"_id": "referrals"})
    return doc["data"] if doc else {}

def save_referrals(refs):
    jf_col.update_one({"_id": "referrals"}, {"$set": {"data": refs}}, upsert=True)

def load_reseller_perms():
    doc = jf_col.find_one({"_id": "reseller_perms"})
    return doc["data"] if doc else {}

def save_reseller_perms(perms):
    jf_col.update_one({"_id": "reseller_perms"}, {"$set": {"data": perms}}, upsert=True)

def load_wallet_purchases():
    doc = jf_col.find_one({"_id": "wallet_purchases"})
    return doc["data"] if doc else {}

def save_wallet_purchases(data):
    jf_col.update_one({"_id": "wallet_purchases"}, {"$set": {"data": data}}, upsert=True)

def load_order_messages(order_id):
    doc = jf_col.find_one({"_id": f"ordermsg_{order_id}"})
    return doc.get("data", {}) if doc else {}

def save_order_messages(order_id, data):
    jf_col.update_one({"_id": f"ordermsg_{order_id}"}, {"$set": {"data": data}}, upsert=True)


def load_user_history(user_id):
    doc = jf_col.find_one({"_id": f"history_{user_id}"})
    if doc and isinstance(doc.get("data"), list):
        return doc["data"]
    return []

def log_user_action(user_id, product, key):
    from datetime import datetime
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_str = f"• {time_str}\n🏺 {product.upper()}\n🔑 <code>{key}</code>\n"
    logs = load_user_history(user_id)
    logs.append(log_str)
    if len(logs) > 50: logs = logs[-50:]
    jf_col.update_one({"_id": f"history_{user_id}"}, {"$set": {"data": logs}}, upsert=True)

def log_reseller_action(username, user_id, product, key):
    save_reseller_logs(username, user_id, product, key)

import os

from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://admin:HARSHIL2829@cluster0.6kcmggh.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client['TelegramBotDB']
jf_col = db['jf_data']

import asyncio
import json
import random
import string
import time
import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ChatMemberUpdated
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, ChatMemberHandler, ChatJoinRequestHandler
import httpx

# Enable logging
import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# CONFIGURATION
TOKEN = "7994962595:AAGOZdezJAetEVJPCpbOVqAds7AYaypWlRY"
UPI_GATEWAY_TOKEN = "7994962595:AAGOZdezJAetEVJPCpbOVqAds7AYaypWlRY" 
IS_AUTO_MODE = False








































# Default settings if file is missing
DEFAULT_SETTINGS = {
    "welcome_text": "\n<b>━━━━━━━━━━━━━━━━━━</b>\n✨ <b>WELCOME TO OUR STORE</b> ✨\n👋 <b>Hello, {name}!</b>\n<b>━━━━━━━━━━━━━━━━━━</b>\n\n🛍️ <b>Store:</b> Buy premium services. Instant Delivery !!\n👤 <b>Profile:</b> Your Account Details.\n💰 <b>Deposit:</b> Add Funds to Wallet.\n📋 <b>History:</b> Track your Orders.\n🎁 <b>Referral:</b> Earn by inviting Friends.\n🎬 <b>How to Use:</b> How to buy Key\n📞 <b>Help:</b> Get Support from Owner.\n🎰 <b>Lucky Spin:</b> Win Exciting Prizes\n",
    "admin_ids": [] # Add your Telegram User ID here (e.g., [12345678])
}










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
        trials[user_id]["strikes"] = trials[user_id].get("strikes", 0) + 1
        if trials[user_id]["strikes"] >= 3:
            trials[user_id]["banned"] = True
        save_trials(trials)






























async def get_unjoined_channels(user_id, context):
    settings = load_settings()
    channels = settings.get("force_channels", [])
    if not channels and settings.get("force_channel"):
        channels = [{"id": settings["force_channel"], "link": settings.get("invite_link", f"https://t.me/{settings['force_channel'].replace('@', '')}")}]
    
    if not channels:
        return []
        
    unjoined = []
    for ch in channels:
        try:
            member = await context.bot.get_chat_member(chat_id=ch["id"], user_id=user_id)
            if member.status in ['left', 'kicked']:
                unjoined.append(ch)
        except Exception as e:
            logger.error(f"Force Sub Error for {ch['id']}: {e}")
            unjoined.append(ch)
            
    return unjoined

async def check_force_sub(user_id, context):
    settings = load_settings()
    channels = settings.get("force_channels", [])
    
    # Backwards compatibility
    if not channels and settings.get("force_channel"):
        channels = [{"id": settings["force_channel"], "link": settings.get("invite_link", f"https://t.me/{settings['force_channel'].replace('@', '')}")}]
        
    if not channels:
        return True
        
    for ch in channels:
        try:
            member = await context.bot.get_chat_member(chat_id=ch["id"], user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception as e:
            logger.error(f"Force Sub Error for {ch['id']}: {e}")
            
    return True

async def verify_utr_api(client_txn_id, amount):
    """Checks the order status on UPIGateway.com."""
    if not IS_AUTO_MODE:
        return "manual"
        
    api_url = "https://merchant.upigateway.com/api/check_order_status"
    params = {
        "key": UPI_GATEWAY_TOKEN,
        "client_txn_id": client_txn_id
    }
    
    async with httpx.AsyncClient() as client:
        try:
            # Use POST as per UPIGateway docs usually
            response = await client.post(api_url, data=params, timeout=10)
            data = response.json()
            if data.get("status") is True and data.get("data", {}).get("status") == "COMPLETED":
                return "success"
        except Exception as e:
            logger.error(f"Status Check Error: {e}")
    
    return "pending"

async def create_upigateway_order(amount, order_id, user_name):
    """Creates a dynamic order/QR on UPIGateway."""
    api_url = "https://merchant.upigateway.com/api/create_order"
    payload = {
        "key": UPI_GATEWAY_TOKEN,
        "client_txn_id": order_id,
        "amount": amount,
        "p_info": "Mod Menu Subscription",
        "customer_name": user_name,
        "customer_email": "customer@hxnstore.com",
        "customer_mobile": "9999999999",
        "redirect_url": "https://t.me/HXNSHOP_bot"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(api_url, data=payload, timeout=10)
            data = response.json()
            if data.get("status") is True:
                return data.get("data", {}).get("payment_url")
        except Exception as e:
            logger.error(f"Order Creation Error: {e}")
            
    return None

async def generate_key_from_api(product, duration_label, product_id=None):
    """Calls the Alwaysdata API to generate a real key."""
    api_url = "https://harshilexe.alwaysdata.net/api/generate.php"
    api_secret = "hxn_secret_12345"
    
    # Map durations from bot format to website format
    duration_map = {
        "1d": "1 Day",
        "3d": "3 Days",
        "7d": "7 Days",
        "15d": "15 Days",
        "30d": "30 Days"
    }
    site_duration = duration_map.get(duration_label, "1 Day")
    
    # All API queries use product_id = 1 as per user's instructions
    params = {
        "secret": api_secret,
        "product_id": 1,
        "duration": site_duration,
        "amount": 1,
        "max_devices": 1
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url, params=params, timeout=10)
            data = response.json()
            if data.get("status") is True and data.get("keys"):
                return data["keys"][0]
        except Exception as e:
            logger.error(f"API Error: {e}")
            
    return None

# --- HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_banned(user_id):
        await update.message.reply_text("🚫 You are banned from this bot for abusing the trial system.")
        return
    save_user(user_id, update.effective_user.username)
    log_activity(user_id, 'started the bot')
    
    # Referral System
    if context.args and len(context.args) > 0:
        referrer_id = context.args[0]
        settings = load_settings()
        if not settings.get("refer_locked", False) and str(referrer_id).isdigit() and str(referrer_id) != str(user_id):
            refs = load_referrals()
            if "referred" not in refs: refs["referred"] = []
            if "users" not in refs: refs["users"] = {}
            if user_id not in refs["referred"]:
                refs["referred"].append(user_id)
                
                if referrer_id not in refs["users"]: 
                    refs["users"][referrer_id] = {"count": 0, "earnings": 0.0, "daily_count": 0, "date": ""}
                
                from datetime import datetime
                today_str = datetime.now().strftime("%Y-%m-%d")
                
                user_data = refs["users"][referrer_id]
                if user_data.get("date") != today_str:
                    user_data["date"] = today_str
                    user_data["daily_count"] = 0
                
                if user_data.get("daily_count", 0) < 5:
                    user_data["count"] = user_data.get("count", 0) + 1
                    user_data["daily_count"] = user_data.get("daily_count", 0) + 1
                    user_data["earnings"] = user_data.get("earnings", 0.0) + 10.0
                    save_referrals(refs)
                    
                    bals = load_balances()
                    bals[str(referrer_id)] = bals.get(str(referrer_id), 0.0) + 10.0
                    save_balances(bals)
                    
                    try:
                        await context.bot.send_message(chat_id=int(referrer_id), text=f"🎉 <b>New Referral!</b>\nSomeone joined using your link. You earned ₹10.00! (Daily Limit: {user_data['daily_count']}/5)", parse_mode="HTML")
                    except:
                        pass
                else:
                    # Over daily limit, still save that they referred so the new user isn't prompted again
                    save_referrals(refs)
                    try:
                        await context.bot.send_message(chat_id=int(referrer_id), text=f"⚠️ <b>Referral Limit Reached!</b>\nSomeone joined using your link, but you have reached the maximum limit of 5 paid referrals per day. You did not earn ₹10 for this one.", parse_mode="HTML")
                    except:
                        pass
    
    verified_users = load_verified_users()
    settings = load_settings()
    
    if True: # user_id in verified_users:
        settings = load_settings()
        if not await check_force_sub(user_id, context):
            channels = settings.get("force_channels", [])
            if not channels and settings.get("force_channel"):
                channels = [{"id": settings["force_channel"], "link": settings.get("invite_link", f"https://t.me/{settings['force_channel'].replace('@', '')}")}]
                
            keyboard = []
            for i, ch in enumerate(channels):
                keyboard.append([InlineKeyboardButton(f"📢 Join Channel {i+1}", url=ch["link"])])
            keyboard.append([InlineKeyboardButton("✅ I Joined All", callback_data="check_joined")])
            
            await update.message.reply_text(
                f"⚠️ <b>Access Denied!</b>\n\nYou must join all our channels to use this bot.\nPlease click the buttons below to join.",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="HTML"
            )
            return
            
        reply_markup = None
        if user_id in settings["admin_ids"]:
            reply_markup = ReplyKeyboardMarkup([[KeyboardButton("👑 Admin Panel")]], resize_keyboard=True)
            
        await update.message.reply_text(
            settings["welcome_text"].format(name=update.effective_user.first_name),
            reply_markup=get_main_menu_keyboard(),
            parse_mode="HTML"
        )
        if reply_markup:
            await update.message.reply_text("Admin recognized.", reply_markup=reply_markup)
        return

    # Not verified, ask for contact
    contact_keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("🛡️ Verify Identity (Share Contact)", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await update.message.reply_text(
        f"To ensure security, please share your contact.",
        reply_markup=contact_keyboard
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.effective_user and update.effective_user.username:
        save_username_mapping(user_id, update.effective_user.username)
    web_settings = load_web_settings()
    web_staff = load_web_staff()
    admin_ids = load_settings().get("admin_ids", [])
    all_admins = [str(x) for x in admin_ids] + [str(s.get("telegram_id")) for s in web_staff if s.get("telegram_id")]
    is_admin = str(user_id) in all_admins

    if web_settings.get("maintenance_mode", False) and not is_admin:
        if update.message.text and not update.message.text.startswith("/"):
            await update.message.reply_text("🛠 <b>Maintenance Mode</b>\nThe bot is currently undergoing maintenance. Please try again later.", parse_mode="HTML")
            return
    """Handles text and photo messages."""
    settings = load_settings()
    
    # Check if this is a forwarded message (to get channel ID)
    chat_id = None
    if getattr(update.message, 'forward_origin', None):
        origin = update.message.forward_origin
        if hasattr(origin, 'chat'):
            chat_id = origin.chat.id
    elif getattr(update.message, 'forward_from_chat', None):
        chat_id = update.message.forward_from_chat.id
        
    if chat_id and update.effective_user.id in settings["admin_ids"]:
        await update.message.reply_text(f"📢 <b>Forwarded Channel ID:</b> <code>{chat_id}</code>\n\nUse this in:\n<code>/add_channel {chat_id} [link]</code>", parse_mode="HTML")
        return

    # Check if user is in a specific state (like waiting for a receipt)
    state = context.user_data.get("state") if context.user_data else None
    settings = load_settings()
    
    
    if state == "awaiting_balance_amount":
        if update.message.text in ["👑 Admin Panel", "/start", "/help", "cancel"]:
            context.user_data["state"] = None
        else:
            try:
                amount = float(update.message.text.strip())
                if amount <= 0:
                    raise ValueError
                
                context.user_data["state"] = None
                context.user_data["balance_amount"] = amount
                import uuid
                order_id = str(uuid.uuid4().hex)[:8]
                
                reply_text = (
                    "💰 <b>ADD BALANCE REQUEST</b>\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    f"💵 <b>Amount:</b> ₹{amount:.2f}\n"
                    f"🆔 <b>Order ID:</b> <code>{order_id}</code>\n\n"
                    "<i>Scan the QR code below to pay, then click '✅ I Have Paid'.</i>"
                )
                keyboard = [
                    [InlineKeyboardButton("✅ I Have Paid", callback_data=f"balconfirm_{order_id}_{amount}")],
                    [InlineKeyboardButton("« Cancel", callback_data="main_menu")]
                ]
                import os
                if os.path.exists("qr.png"):
                    await update.message.reply_photo(photo=open("qr.png", "rb"), caption=reply_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
                else:
                    await update.message.reply_text(reply_text + "\n\n⚠️ <i>(QR Code missing)</i>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
                return
            except:
                await update.message.reply_text("❌ Please enter a valid positive number.")
                return

    if state == "awaiting_new_product_name":
        if update.effective_user.id not in settings["admin_ids"]: return
        prod_name = update.message.text.strip().lower() if update.message.text else ""
        if not prod_name:
            await update.message.reply_text("❌ Invalid name. Please send a valid product name:")
            return
        
        web_products = load_web_products()
        exists = any(wp.get("name", "").lower() == prod_name for wp in web_products)
        if exists:
            await update.message.reply_text(f"⚠️ <b>{prod_name.upper()}</b> already exists in the product list.\n\nEnter another name or cancel:")
            return
        
        context.user_data["new_product_name"] = prod_name
        context.user_data["state"] = None
        
        keyboard = [
            [InlineKeyboardButton("Trial Only", callback_data="admin_add_product_sec_trial")],
            [InlineKeyboardButton("Selling Only", callback_data="admin_add_product_sec_selling")],
            [InlineKeyboardButton("Both", callback_data="admin_add_product_sec_both")],
            [InlineKeyboardButton("« Cancel", callback_data="admin_prod_mgmt")]
        ]
        await update.message.reply_text(
            f"🛒 <b>Product:</b> {prod_name.upper()}\n\n"
            "Select which section this product belongs to:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
        return

    if state == "awaiting_bulk_keys":
        if update.effective_user.id not in settings["admin_ids"]: return
        product = context.user_data.get("bulk_product")
        duration = context.user_data.get("bulk_duration")
        raw_text = update.message.text
        if raw_text:
            new_keys = [k.strip() for k in raw_text.split() if k.strip()]
            if new_keys:
                keys_db = load_keys()
                dict_key = f"{product}_{duration}"
                if dict_key not in keys_db: keys_db[dict_key] = []
                keys_db[dict_key].extend(new_keys)
                save_keys(keys_db)
                await update.message.reply_text(f"✅ <b>Successfully added {len(new_keys)} keys to {product.upper()} ({duration})!</b>\n\nNew Stock Count: {len(keys_db[dict_key])}", parse_mode="HTML")
            else:
                await update.message.reply_text("❌ No valid keys found.")
        context.user_data["state"] = None
        return

    if state == "awaiting_receipt":
        user = update.effective_user
        order_id = context.user_data.get("order_id")
        if not order_id or order_id == "Unknown":
            order_id = "OID" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        product = context.user_data.get("product", "Unknown")
        amount = context.user_data.get("amount", "0")
        duration = context.user_data.get("duration", "1d")
        utr = update.message.text
        
        # 1. Prevent Double Use of UTR
        utr_log = load_utr_log()
        if utr and utr in utr_log:
            await update.message.reply_text("❌ <b>Error:</b> This Transaction ID (UTR) has already been used!")
            return

        # 2. Check if Auto-Mode is ON
        if IS_AUTO_MODE and utr and utr.isdigit() and len(utr) == 12:
            status_msg = await update.message.reply_text("⏳ <b>Verifying your payment...</b> Please wait.", parse_mode="HTML")
            api_status = await verify_utr_api(utr, amount)
            
            if api_status == "success":
                save_utr(utr)
                # Delivery Key
                keys = load_keys()
                prod_key = product.lower()
                if prod_key in keys and len(keys[prod_key]) > 0:
                    delivered_key = keys[prod_key].pop(0)
                    save_keys(keys)
                    await status_msg.edit_text(
                        "✅ <b>AUTO-VERIFIED!</b>\n"
                        "━━━━━━━━━━━━━━━━━━\n"
                        f"🔑 <b>YOUR KEY:</b>\n<code>{delivered_key}</code>\n\n"
                        "<i>Thank you for shopping!</i>",
                        parse_mode="HTML"
                    )
                    return
                else:
                    await status_msg.edit_text("✅ <b>Payment Verified!</b>\nBut we are out of stock. Admin will send your key manually soon.")
                    # Continue to notify admin...
            else:
                await status_msg.edit_text("❌ <b>Payment not found!</b>\nIf you have paid, please wait 1 minute and send the UTR again. Or wait for Admin.")

        # 3. Fallback: Notify Admin with buttons
        admin_msg = (
            "🔔 <b>NEW PAYMENT RECEIPT</b>\n"
            "━━━━━━━━━━━━━━\n"
            f"👤 <b>User:</b> {user.first_name} (@{user.username})\n"
            f"🆔 <b>User ID:</b> <code>{user.id}</code>\n"
            f"🏺 <b>Product:</b> {product}\n"
            f"⏳ <b>Duration:</b> {duration}\n"
            f"📦 <b>Order ID:</b> <code>{order_id}</code>\n"
            f"💵 <b>Amount:</b> ₹{amount}\n"
            f"💬 <b>UTR/Proof:</b> {utr or 'Photo attached'}"
        )
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}_{product}_{order_id}_{duration}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}_{order_id}")
            ]
        ])
        
        admin_messages = {}
        for admin_id in settings["admin_ids"]:
            try:
                if update.message.photo:
                    sent_msg = await context.bot.send_photo(chat_id=admin_id, photo=update.message.photo[-1].file_id, caption=admin_msg, reply_markup=keyboard, parse_mode="HTML")
                else:
                    sent_msg = await context.bot.send_message(chat_id=admin_id, text=admin_msg, reply_markup=keyboard, parse_mode="HTML")
                admin_messages[str(admin_id)] = sent_msg.message_id
            except Exception as e:
                logger.error(f"Could not notify admin {admin_id}: {e}")
        
        save_order_messages(order_id, {
            "status": "pending",
            "messages": admin_messages,
            "text": admin_msg,
            "is_photo": bool(update.message.photo)
        })
        
        await update.message.reply_text("✅ <b>Receipt Received!</b>\nOur admin is verifying your payment. You will receive your key soon.", parse_mode="HTML")
        context.user_data["state"] = None # Reset state
    else:
        if getattr(update.message, "text", None) == "👑 Admin Panel":
            if update.effective_user.id in settings["admin_ids"]:
                keyboard = [
                    [InlineKeyboardButton("➕ Add Reseller", callback_data="admin_guide_add"), InlineKeyboardButton("➖ Remove Reseller", callback_data="admin_guide_remove")],
                    [InlineKeyboardButton("📋 Active Resellers", callback_data="admin_listresellers"), InlineKeyboardButton("🔍 View Reseller Logs", callback_data="admin_logsmode")],
                    [InlineKeyboardButton("💰 Add Balance", callback_data="admin_guide_bal"), InlineKeyboardButton("📦 Check Stock", callback_data="admin_stock")],
                    [InlineKeyboardButton("🔑 Add Keys (Bulk)", callback_data="admin_add_keys"), InlineKeyboardButton("📜 Trial Logs", callback_data="admin_trial_logs")],
                    [InlineKeyboardButton("📦 Product Management", callback_data="admin_prod_mgmt")],
                    [InlineKeyboardButton("🔄 Reset Trial Cooldown", callback_data="admin_reset_trial")],
                    [InlineKeyboardButton("❓ Help Commands", callback_data="admin_help_commands")]
                ]
                await update.message.reply_text("👑 <b>Admin Dashboard</b>\nSelect an option below:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
            return

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles shared contact and shows the main menu."""
    contact = update.message.contact
    user = update.effective_user
    settings = load_settings()
    
    # Save to verified list
    save_verified_user(user.id)
    
    # Notify Admin about new verification (but don't notify the user about themselves if they are the admin)
    admin_notify_text = (
        "👤 <b>NEW USER VERIFIED</b>\n"
        "━━━━━━━━━━━━━━\n"
        f"<b>Name:</b> {user.first_name} {user.last_name or ''}\n"
        f"<b>Username:</b> @{user.username or 'None'}\n"
        f"<b>ID:</b> <code>{user.id}</code>\n"
        f"<b>Phone:</b> <code>+{contact.phone_number}</code>"
    )
    
    for admin_id in settings["admin_ids"]:
        # Don't send notification to the user who just verified if they are the admin
        if admin_id == user.id:
            continue
            
        try:
            await context.bot.send_message(chat_id=admin_id, text=admin_notify_text, parse_mode="HTML")
        except Exception as e:
            logger.error(f"Failed to notify admin {admin_id}: {e}")

    # 1. Identity Verified Message to User
    await update.message.reply_text(
        f"<b>{user.first_name}</b>\nContact\n\n✅ <b>IDENTITY VERIFIED</b>\n"
        "━━━━━━━━━━━━━━\n"
        "Your account is now fully active.",
        parse_mode="HTML"
    )
    
    unjoined = await get_unjoined_channels(user.id, context)
    if unjoined:
        keyboard = []
        for i, ch in enumerate(unjoined):
            keyboard.append([InlineKeyboardButton(f"📢 Join Channel {i+1}", url=ch["link"])])
        keyboard.append([InlineKeyboardButton("✅ I Joined All", callback_data="check_joined")])
        
        await update.message.reply_text(
            f"⚠️ <b>Access Denied!</b>\n\nYou have {len(unjoined)} channel(s) remaining to join.\nPlease click the buttons below to join them.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
        return
        
    reply_markup = None
    if user.id in settings["admin_ids"]:
        reply_markup = ReplyKeyboardMarkup([[KeyboardButton("👑 Admin Panel")]], resize_keyboard=True)
    
    await update.message.reply_text(
        settings["welcome_text"].format(name=user.first_name),
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML"
    )
    if reply_markup:
        await update.message.reply_text("Admin recognized.", reply_markup=reply_markup)

def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🛍️ Shop Store Now", callback_data="shop")],
        [
            InlineKeyboardButton("👤 My Profile", callback_data="profile"),
            InlineKeyboardButton("💰 Add Balance", callback_data="add_balance")
        ],
        [
            InlineKeyboardButton("📋 All History", callback_data="history"),
            InlineKeyboardButton("🎁 Referral", callback_data="referral")
        ],
        [
            InlineKeyboardButton("🎬 How To Use Bot", callback_data="how_to_use"),
            InlineKeyboardButton("📞 Connect Helpline", callback_data="helpline")
        ],
        [InlineKeyboardButton("🎁 Get Trial Key", callback_data="trial_key")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_shop_keyboard(user_id=None):
    web_products = load_web_products()
    if not web_products:
        all_buttons = [
            InlineKeyboardButton("HXN CHEAT", callback_data="product_hxn"),
            InlineKeyboardButton("LK TEAM", callback_data="product_lk"),
            InlineKeyboardButton("HEX BLADE", callback_data="product_hex"),
            InlineKeyboardButton("ALPHA-X STORE", callback_data="product_alpha"),
            InlineKeyboardButton("PRIME X CHEAT", callback_data="product_prime"),
            InlineKeyboardButton("HARSHIL MODS", callback_data="product_harshil"),
            InlineKeyboardButton("TRINITY X ROOT", callback_data="product_trinity"),
            InlineKeyboardButton("FLUORITE ANDROID", callback_data="product_fluorite"),
            InlineKeyboardButton("SVJ CHEATS", callback_data="product_svj"),
            InlineKeyboardButton("BR MODS", callback_data="product_brmods"),
            InlineKeyboardButton("BEYOND CHEATS", callback_data="product_beyond"),
            InlineKeyboardButton("ROGERIO MODS", callback_data="product_rogerio"),
            InlineKeyboardButton("HAWK CHEATS", callback_data="product_hawk"),
            InlineKeyboardButton("RAPID CORE", callback_data="product_rapid"),
            InlineKeyboardButton("DAEMON PHONK", callback_data="product_daemon"),
            InlineKeyboardButton("HXN STREAMER (.SH)", callback_data="product_streamerxsh"),
            InlineKeyboardButton("BS SECURE LOADER", callback_data="product_bssecure"),
            InlineKeyboardButton("HYDRA ENGINE 8BP", callback_data="product_hydra"),
            InlineKeyboardButton("XTFFH4X STREAMER", callback_data="product_xtffh4x_streamer"),
            InlineKeyboardButton("STREAMER X", callback_data="product_streamerx"),
            InlineKeyboardButton("BOOYAH PANEL", callback_data="product_boyyah"),
            InlineKeyboardButton("ELITE TEAM", callback_data="product_eliteteam"),
            InlineKeyboardButton("NGO TRAN", callback_data="product_ngo"),
            InlineKeyboardButton("GREED PANEL", callback_data="product_greed"),
            InlineKeyboardButton("LK TEAM PRO", callback_data="product_lkpro"),
            InlineKeyboardButton("KIWMODZ EXE", callback_data="product_kiwmodz"),
            InlineKeyboardButton("XYZ SUPREME", callback_data="product_xyz")
        ]
    else:
        all_buttons = []
        for wp in web_products:
            section = wp.get("section", "Both")
            if section in ["Selling Only", "Both", "selling", "both"]:
                name = wp.get("display_name") or wp.get("name", "").upper().replace("_", " ")
                callback = f"product_{wp.get('name', '').lower()}"
                all_buttons.append(InlineKeyboardButton(name, callback_data=callback))
    
    if user_id:
        resellers = load_resellers()
        if str(user_id) in resellers:
            perms = load_reseller_perms().get(str(user_id), [])
            if not perms:
                all_buttons = []
            else:
                all_buttons = [b for b in all_buttons if b.callback_data.replace("product_", "") in perms]
                
    keyboard = []
    for i in range(0, len(all_buttons), 2):
        keyboard.append(all_buttons[i:i+2])
    keyboard.append([InlineKeyboardButton("« Main Menu", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

# --- ADMIN COMMANDS ---

async def get_my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Helpful command to get user ID for admin setup."""
    await update.message.reply_text(f"Your Telegram ID is: <code>{update.effective_user.id}</code>", parse_mode="HTML")

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show admin options to authorized users."""
    user_id = update.effective_user.id
    settings = load_settings()
    
    if user_id not in settings["admin_ids"]:
        await update.message.reply_text("❌ You are not authorized to use admin commands.")
        return

    admin_text = (
        "👑 <b>Admin Panel</b>\n\n"
        "Commands:\n"
        "/set_welcome [text] - Update the store menu text\n"
        "/add_admin [id] - Authorize another admin\n"
        "/add_balance [id] [amt] - Add balance to user\n"
        "/add_reseller [id] [days] - Add a reseller\n"
        "/remove_reseller [id] - Remove a reseller\n"
        "/resellers - List all active resellers\n"
        "/rlogs [id] - View reseller activity\n"
        "/broadcast [msg] - Send a message to all users\n"
        "/add_key [prod] [duration] [key] - Add a single license key\n"
        "/stock - Check remaining keys stock"
    )
    await update.message.reply_text(admin_text, parse_mode="HTML")

async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    
    if user_id not in settings["admin_ids"]: return

    if not context.args:
        await update.message.reply_text("Usage: /set_welcome [New Menu Text]")
        return

    new_text = " ".join(context.args)
    settings["welcome_text"] = new_text
    save_settings(settings)
    await update.message.reply_text("✅ <b>Welcome message updated!</b>", parse_mode="HTML")

async def remove_balance_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        await context.bot.send_message(chat_id=target_id, text=f"💰 <b>Admin removed ₹{amount} from your wallet.</b>\nNew Balance: ₹{balances[target_id]}", parse_mode="HTML")
    except: pass


async def set_trial_days_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = load_settings()
    if update.effective_user.id not in settings["admin_ids"]:
        return
        
    if not context.args:
        await update.message.reply_text("Usage: /set_trial_days [number of days] [optional: product_name]\nExample: /set_trial_days 1\nExample: /set_trial_days 1 brmods")
        return
        
    try:
        days = float(context.args[0])
        if days < 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text("Please provide a valid positive number.")
        return
        
    if "trial_cooldowns" not in settings or not isinstance(settings["trial_cooldowns"], dict):
        settings["trial_cooldowns"] = {}
        
    if len(context.args) > 1:
        product_name = context.args[1].lower()
        settings["trial_cooldowns"][product_name] = days
        save_settings(settings)
        await update.message.reply_text(f"✅ Trial key cooldown for '{product_name.upper()}' has been set to {days} days.")
    else:
        settings["trial_cooldowns"]["default"] = days
        save_settings(settings)
        await update.message.reply_text(f"✅ Global Trial key cooldown has been set to {days} days.")

async def ban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = load_settings()
    if update.effective_user.id not in settings["admin_ids"]: return
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /ban [user_id]")
        return
    
    target_id = str(context.args[0])
    trials = load_trials()
    if target_id not in trials:
        trials[target_id] = {"last_trial": 0, "strikes": 0, "history": {}}
    trials[target_id]["banned"] = True
    save_trials(trials)
    await update.message.reply_text(f"✅ User {target_id} has been BANNED.")

async def unban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = load_settings()
    if update.effective_user.id not in settings["admin_ids"]: return
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /unban [user_id]")
        return
    
    target_id = str(context.args[0])
    trials = load_trials()
    if target_id in trials:
        trials[target_id]["banned"] = False
        trials[target_id]["strikes"] = 0
        save_trials(trials)
    await update.message.reply_text(f"✅ User {target_id} has been UNBANNED and strikes reset to 0.")

async def check_history_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = load_settings()
    if update.effective_user.id not in settings.get("admin_ids", []): return
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /check_history [user_id]")
        return
        
    target_id = str(context.args[0])
    logs = load_user_history(target_id)
    
    if not logs:
        await update.message.reply_text(f"❌ No history found for user {target_id}.")
        return
        
    history_text = "\n".join(logs[-20:])
    text = f"📋 <b>ORDER HISTORY: {target_id}</b>\n━━━━━━━━━━━━━━━━━━\n{history_text}\n<i>Showing the last 20 purchases.</i>"
    
    if len(text) > 4096:
        text = text[:4000] + "... [TRUNCATED]"
        
    await update.message.reply_text(text, parse_mode="HTML")

async def check_balance_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]: return
    
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /check_balance [user_id]")
        return
        
    target_id = str(context.args[0])
    balances = load_balances()
    current = balances.get(target_id, 0.0)
    await update.message.reply_text(f"💰 Balance for user {target_id}: ₹{current:.2f}")

async def check_user_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]: return
    
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /check_user [user_id_or_username]")
        return
        
    target_input = str(context.args[0]).strip()
    
    if target_input.startswith("@") or not target_input.isdigit():
        username_clean = target_input.replace("@", "").lower().strip()
        target_id = get_user_id_by_username(username_clean)
        if not target_id:
            try:
                chat = await context.bot.get_chat(f"@{username_clean}")
                target_id = str(chat.id)
                save_username_mapping(target_id, username_clean)
            except Exception as e:
                await update.message.reply_text(
                    f"❌ <b>Username Not Found</b>\n"
                    f"Could not find a user ID associated with @{username_clean}.\n\n"
                    f"<i>Note: The bot can only find users by username after they have messaged or interacted with the bot.</i>",
                    parse_mode="HTML"
                )
                return
    else:
        target_id = target_input
        
    balances = load_balances()
    balance = balances.get(target_id, 0.0)
    
    resellers = load_resellers()
    is_reseller = target_id in resellers
    reseller_expiry = resellers.get(target_id, 0.0)
    reseller_status = "❌ No"
    if is_reseller:
        if time.time() < reseller_expiry:
            import datetime
            exp_date = datetime.datetime.fromtimestamp(reseller_expiry).strftime('%Y-%m-%d %H:%M:%S')
            reseller_status = f"✅ Yes (Expires: {exp_date})"
        else:
            reseller_status = "❌ Expired"
            
    perms = load_reseller_perms().get(target_id, [])
    perms_str = ", ".join(perms) if perms else "None"
    
    trials = load_trials()
    trial_data = trials.get(target_id, {})
    is_banned = trial_data.get("banned", False)
    strikes = trial_data.get("strikes", 0)
    last_trial_time = trial_data.get("last_trial", 0)
    last_trial_str = "Never"
    if last_trial_time > 0:
        import datetime
        last_trial_str = datetime.datetime.fromtimestamp(last_trial_time).strftime('%Y-%m-%d %H:%M:%S')
        
    refs = load_referrals()
    ref_data = refs.get("users", {}).get(target_id, {"count": 0, "earnings": 0.0})
    ref_count = ref_data.get("count", 0)
    ref_earnings = ref_data.get("earnings", 0.0)
    
    display_name = "Unknown User"
    try:
        chat = await context.bot.get_chat(int(target_id))
        display_name = chat.first_name
        if chat.last_name:
            display_name += f" {chat.last_name}"
        if chat.username:
            display_name += f" (@{chat.username})"
    except:
        pass
        
    user_info_text = (
        f"👤 <b>USER PROFILE INFO</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>Name:</b> {display_name}\n"
        f"🆔 <b>User ID:</b> <code>{target_id}</code>\n"
        f"💰 <b>Wallet Balance:</b> ₹{balance:.2f}\n"
        f"🚫 <b>Banned Status:</b> {'❌ BANNED' if is_banned else '✅ Active'}\n"
        f"⚠️ <b>Strikes Count:</b> {strikes}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👑 <b>Reseller:</b> {reseller_status}\n"
        f"🔑 <b>Reseller Permissions:</b> {perms_str}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🎁 <b>Referred Count:</b> {ref_count} users\n"
        f"💸 <b>Referral Earnings:</b> ₹{ref_earnings:.2f}\n"
        f"⏳ <b>Last Trial Claimed:</b> {last_trial_str}\n"
    )
    
    await update.message.reply_text(user_info_text, parse_mode="HTML")

async def add_balance_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]: return

    if len(context.args) < 2:
        await update.message.reply_text("Usage: /add_balance [user_id] [amount]")
        return
        
    try:
        target_id = str(context.args[0])
        amount = float(context.args[1])
    except ValueError:
        await update.message.reply_text("Invalid amount.")
        return
        
    balances = load_balances()
    current = balances.get(target_id, 0.0)
    balances[target_id] = current + amount
    save_balances(balances)
    
    await update.message.reply_text(f"✅ Added ₹{amount} to user {target_id}. New Balance: ₹{balances[target_id]}")
    try:
        await context.bot.send_message(chat_id=target_id, text=f"💰 <b>Admin added ₹{amount} to your wallet!</b>\nNew Balance: ₹{balances[target_id]}", parse_mode="HTML")
    except:
        pass

async def add_reseller_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]: return

    if len(context.args) < 2:
        await update.message.reply_text("Usage: /add_reseller [user_id] [days]")
        return
        
    try:
        target_id = str(context.args[0])
        days = int(context.args[1])
    except ValueError:
        await update.message.reply_text("Invalid format. Days must be an integer.")
        return
        
    resellers = load_resellers()
    expiry = time.time() + (days * 86400)
    resellers[target_id] = expiry
    save_resellers(resellers)
    
    await update.message.reply_text(f"✅ Added VIP Reseller {target_id} for {days} days.\nThey now have UNLIMITED credit until it expires.")
    try:
        await context.bot.send_message(chat_id=target_id, text=f"🎉 <b>You are now a VIP RESELLER!</b>\nYour access is valid for {days} days.\nYou can generate unlimited keys using the <code>/gen</code> command.\n\nUsage: <code>/gen [product] [1d/3d/7d/15d/30d]</code>\nExample: <code>/gen greed 1d</code>", parse_mode="HTML")
    except:
        pass

async def remove_reseller_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]: return
    
    if not context.args:
        await update.message.reply_text("Usage: /remove_reseller [user_id]")
        return
        
    target_id = str(context.args[0])
    resellers = load_resellers()
    if target_id in resellers:
        del resellers[target_id]
        save_resellers(resellers)
        await update.message.reply_text(f"✅ Removed reseller {target_id}.")
        try:
            await context.bot.send_message(chat_id=target_id, text="❌ Your VIP RESELLER access has been revoked by an Admin.")
        except:
            pass
    else:
        await update.message.reply_text("❌ User is not a reseller.")

async def list_resellers_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]: return
    
    resellers = load_resellers()
    if not resellers:
        await update.message.reply_text("No active resellers found.")
        return
        
    text = "👑 <b>ACTIVE RESELLERS</b>\n━━━━━━━━━━━━━━━━━━\n"
    for r_id, exp in resellers.items():
        if time.time() < exp:
            days_left = (exp - time.time()) / 86400
            text += f"👤 <code>{r_id}</code> - Expires in {days_left:.1f} days\n"
        else:
            text += f"👤 <code>{r_id}</code> - ❌ EXPIRED\n"
            
    await update.message.reply_text(text, parse_mode="HTML")

async def rlogs_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]: return
    
    if not context.args:
        await update.message.reply_text("Usage: /rlogs [user_id]")
        return
        
    target_id = str(context.args[0])
    logs = load_reseller_logs()
    
    user_logs = [log for log in logs if f"({target_id})" in log][-20:]
    if not user_logs:
        await update.message.reply_text("❌ No activity found for this reseller.")
        return
    
    text = f"📋 <b>RESELLER LOGS: {target_id}</b>\n━━━━━━━━━━━━━━━━━━\n"
    for log in user_logs:
        text += f"• {log}\n"
        
    text += f"\n<i>Total keys generated: {len(user_logs)}</i>"
    await update.message.reply_text(text, parse_mode="HTML")

async def gen_key_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    resellers = load_resellers()
    
    if user_id not in resellers:
        await update.message.reply_text("❌ You are not a Reseller.")
        return
        
    if time.time() > resellers[user_id]:
        await update.message.reply_text("❌ Your Reseller subscription has expired.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Usage: /gen [product] [duration]\nExample: /gen greed 1d")
        return
        
    product = context.args[0].lower()
    duration_label = context.args[1].lower()
    
    delivered_key = None
    
    status_msg = await update.message.reply_text("🔄 Generating key...")
    
    if check_use_api(product):
        delivered_key = await generate_key_from_api(product, duration_label)
    else:
        dict_key = f"{product}_{duration_label}"
        keys = load_keys()
        if dict_key in keys and len(keys[dict_key]) > 0:
            delivered_key = keys[dict_key].pop(0)
            save_keys(keys)
            
    if delivered_key:
        username = f"@{update.effective_user.username}" if update.effective_user.username else str(update.effective_user.first_name)
        log_reseller_action(username, user_id, product, delivered_key)
        log_activity(user_id, f'reseller generated {product} key')
        success_msg = (
            "✅ <b>RESELLER KEY GENERATED</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"🏺 <b>Product:</b> {product.upper()}\n"
            f"⏳ <b>Duration:</b> {duration_label.upper()}\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"🔑 <code>{delivered_key}</code>\n"
        )
        await status_msg.edit_text(success_msg, parse_mode="HTML")
    else:
        await status_msg.edit_text(f"❌ ERROR! Out of stock or generation failed for {product.upper()} ({duration_label}).")

async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    
    # If list is empty, allow first person to become admin
    if len(settings["admin_ids"]) > 0 and user_id not in settings["admin_ids"]:
        return

    if not context.args:
        await update.message.reply_text("Usage: /add_admin [Telegram ID]")
        return

    try:
        new_admin_id = int(context.args[0])
        if new_admin_id not in settings["admin_ids"]:
            settings["admin_ids"].append(new_admin_id)
            save_settings(settings)
            await update.message.reply_text(f"✅ Admin {new_admin_id} added.")
    except ValueError:
        await update.message.reply_text("Invalid ID format.")

async def add_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]: return

    if len(context.args) < 3:
        await update.message.reply_text("Usage: /add_key [product] [duration] [key]\nExample: /add_key lk 7d LK-XYZ-123")
        return

    product = context.args[0].lower()
    duration = context.args[1].lower()
    key = context.args[2]
    
    dict_key = f"{product}_{duration}"
    
    keys = load_keys()
    if dict_key not in keys: keys[dict_key] = []
    keys[dict_key].append(key)
    save_keys(keys)
    
    wl = load_waitlists()
    if product in wl and len(wl[product]) > 0:
        msg = f"🔔 <b>RESTOCK ALERT!</b> 🔔\n\nKeys for <b>{product.upper()}</b> are back in stock! Buy now before they run out!"
        import asyncio
        notified = 0
        for uid in wl[product]:
            try:
                await context.bot.send_message(chat_id=int(uid), text=msg, parse_mode="HTML")
                notified += 1
            except: pass
            await asyncio.sleep(0.05)
        wl[product] = []
        save_waitlists(wl)
        if notified > 0:
            await update.message.reply_text(f"✅ <b>Waitlist Notified:</b> Alerted {notified} users waiting for {product.upper()}!", parse_mode="HTML")
            
    await update.message.reply_text(f"✅ <b>Key added for {product.upper()} ({duration.upper()})!</b>\nCurrent Stock: {len(keys[dict_key])}", parse_mode="HTML")

async def check_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]: return

    keys = load_keys()
    if not keys:
        await update.message.reply_text("📦 <b>Stock is empty!</b>", parse_mode="HTML")
        return

    web_products = load_web_products()
    active_names = {wp.get("name", "").lower() for wp in web_products}

    stock_text = "📦 <b>CURRENT STOCK:</b>\n━━━━━━━━━━━━━━\n"
    for prod_dur, klist in keys.items():
        parts = prod_dur.split("_")
        prod_prefix = parts[0].lower()
        if prod_prefix in active_names:
            stock_text += f"┠ <b>{prod_dur.upper()}:</b> {len(klist)} keys\n"
    
    await update.message.reply_text(stock_text, parse_mode="HTML")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message to all users."""
    user_id = update.effective_user.id
    settings = load_settings()
    
    if user_id not in settings["admin_ids"]:
        await update.message.reply_text("❌ You are not authorized to broadcast.")
        return

    is_reply = bool(update.message.reply_to_message)
    if not context.args and not is_reply:
        await update.message.reply_text("Usage: /bc [Your Message]\nOR reply to an image/video/message with /bc [optional caption]")
        return

    # Extract raw text including newlines directly from the update message
    msg_to_send = None
    if update.message.text:
        text_content = update.message.text
        if text_content.startswith("/broadcast"):
            msg_to_send = text_content[10:].strip()
        elif text_content.startswith("/bc"):
            msg_to_send = text_content[3:].strip()
        if not msg_to_send:
            msg_to_send = None

    users = load_users()
    
    count = 0
    await update.message.reply_text(f"🚀 <b>Starting Broadcast to {len(users)} users...</b>", parse_mode="HTML")
    
    for uid in users:
        try:
            if is_reply:
                await context.bot.copy_message(
                    chat_id=uid, 
                    from_chat_id=update.effective_chat.id, 
                    message_id=update.message.reply_to_message.message_id, 
                    caption=msg_to_send, 
                    parse_mode="HTML"
                )
            else:
                await context.bot.send_message(chat_id=uid, text=msg_to_send, parse_mode="HTML")
            count += 1
            await asyncio.sleep(0.05) # Small delay to avoid flooding
        except Exception as e:
            pass # Ignore users who blocked the bot

    await update.message.reply_text(f"✅ <b>Broadcast Completed!</b>\nSuccessfully sent to {count} users.", parse_mode="HTML")

async def lock_refer_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]: return
    
    settings["refer_locked"] = True
    save_settings(settings)
    await update.message.reply_text("🔒 <b>Referral System Locked!</b>\nNobody can earn money from referrals now.", parse_mode="HTML")

async def unlock_refer_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]: return
    
    settings["refer_locked"] = False
    save_settings(settings)
    await update.message.reply_text("🔓 <b>Referral System Unlocked!</b>\nBroadcasting notification to all users...", parse_mode="HTML")
    
    users = load_users()
    msg = "🎉 <b>THE REFERRAL SYSTEM IS BACK ONLINE!</b> 🎉\n\nInvite your friends to our bot and earn ₹10 per invite instantly to your wallet! Use the '🎁 Referral' button in the bot to get your link."
    success, failed = 0, 0
    import asyncio
    for uid in users:
        try:
            await context.bot.send_message(chat_id=uid, text=msg, parse_mode="HTML")
            success += 1
        except:
            failed += 1
        await asyncio.sleep(0.05)
    await update.message.reply_text(f"✅ <b>Broadcast Complete!</b>\nSent to: {success}\nFailed: {failed}", parse_mode="HTML")

async def lock_wallet_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]: return
    
    if context.args:
        full_text = " ".join(context.args).lower().strip()
        raw_parts = [p.strip() for p in full_text.split(",")]
        
        targets = []
        current_product = None
        for part in raw_parts:
            if " " in part:
                sub_parts = part.split()
                if sub_parts[0] not in ["1d", "7d", "15d", "30d"] and sub_parts[1] in ["1d", "7d", "15d", "30d"]:
                    current_product = sub_parts[0]
                    targets.append(f"{sub_parts[0]}_{sub_parts[1]}")
                else:
                    targets.append("_".join(sub_parts))
            else:
                if "_" in part:
                    sub_parts = part.split("_")
                    if len(sub_parts) == 2 and sub_parts[1] in ["1d", "7d", "15d", "30d"]:
                        current_product = sub_parts[0]
                    targets.append(part)
                elif part in ["1d", "7d", "15d", "30d"] and current_product:
                    targets.append(f"{current_product}_{part}")
                else:
                    targets.append(part)
                    
        if "wallet_locked_products" not in settings or not isinstance(settings["wallet_locked_products"], list):
            settings["wallet_locked_products"] = []
            
        for target in targets:
            if target not in settings["wallet_locked_products"]:
                settings["wallet_locked_products"].append(target)
        save_settings(settings)
        
        locked_display = ", ".join([t.upper().replace("_", " ") for t in targets])
        await update.message.reply_text(f"🔒 <b>Wallet purchases for [{locked_display}] have been locked for normal users!</b> Resellers can still buy.", parse_mode="HTML")
    else:
        settings["wallet_buy_locked"] = True
        save_settings(settings)
        await update.message.reply_text("🔒 <b>All wallet purchases have been locked for normal users!</b> Resellers can still buy.", parse_mode="HTML")

async def unlock_wallet_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]: return
    
    if context.args:
        full_text = " ".join(context.args).lower().strip()
        raw_parts = [p.strip() for p in full_text.split(",")]
        
        targets = []
        current_product = None
        for part in raw_parts:
            if " " in part:
                sub_parts = part.split()
                if sub_parts[0] not in ["1d", "7d", "15d", "30d"] and sub_parts[1] in ["1d", "7d", "15d", "30d"]:
                    current_product = sub_parts[0]
                    targets.append(f"{sub_parts[0]}_{sub_parts[1]}")
                else:
                    targets.append("_".join(sub_parts))
            else:
                if "_" in part:
                    sub_parts = part.split("_")
                    if len(sub_parts) == 2 and sub_parts[1] in ["1d", "7d", "15d", "30d"]:
                        current_product = sub_parts[0]
                    targets.append(part)
                elif part in ["1d", "7d", "15d", "30d"] and current_product:
                    targets.append(f"{current_product}_{part}")
                else:
                    targets.append(part)
                    
        if "wallet_locked_products" in settings and isinstance(settings["wallet_locked_products"], list):
            for target in targets:
                if target in settings["wallet_locked_products"]:
                    settings["wallet_locked_products"].remove(target)
            save_settings(settings)
            
        unlocked_display = ", ".join([t.upper().replace("_", " ") for t in targets])
        await update.message.reply_text(f"🔓 <b>Wallet purchases for [{unlocked_display}] have been unlocked!</b>", parse_mode="HTML")
    else:
        settings["wallet_buy_locked"] = False
        settings["wallet_locked_products"] = []
        save_settings(settings)
        await update.message.reply_text("🔓 <b>All wallet purchases have been unlocked!</b>", parse_mode="HTML")

async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]: return
    
    users = load_users()
    balances = load_balances()
    trials = load_trials()
    resellers = load_resellers()
    keys = load_keys()
    
    total_users = len(users)
    total_balance = sum(balances.values())
    total_banned = sum(1 for t in trials.values() if t.get("banned", False))
    total_resellers = len(resellers)
    total_keys = sum(len(k) for k in keys.values())
    
    global_stats = load_global_stats()
    total_keys_used = global_stats.get("total_keys_used", 0)
    
    msg = f"📊 <b>BOT STATISTICS</b> 📊\n━━━━━━━━━━━━━━\n"
    msg += f"👥 <b>Total Users:</b> {total_users}\n"
    msg += f"💰 <b>Total User Balances:</b> ₹{total_balance:.2f}\n"
    msg += f"🚫 <b>Banned Users (Trials):</b> {total_banned}\n"
    msg += f"💼 <b>Active Resellers:</b> {total_resellers}\n"
    msg += f"📦 <b>Total Keys in Stock:</b> {total_keys}\n"
    msg += f"🔑 <b>Total Keys Generated:</b> {total_keys_used}\n"
    
    await update.message.reply_text(msg, parse_mode="HTML")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if update.effective_user and update.effective_user.username:
        save_username_mapping(update.effective_user.id, update.effective_user.username)
    try:
        await query.answer()
    except:
        pass
    data = query.data
    settings = load_settings()
    

    if is_banned(update.effective_user.id):
        await query.answer("🚫 You are banned.", show_alert=True)
        return

    if data == "trial_key":
        settings = load_settings()
        if settings.get("trial_locked", False):
            msg = settings.get("trial_locked_msg", "🚫 <b>TRIAL SECTION LOCKED</b> 🚫\n\n<b>NO FEEDBACK AND SUPPORT KEY</b>\n<b>STOP ASK OWNER :-</b>@JFHAXX01\n<b>OR DEVLOPER :-</b>@rajput_harshil")
            kb = [[InlineKeyboardButton("« Back", callback_data="main_menu")]]
            await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
            return
        web_products = load_web_products()
        if not web_products:
            keyboard = [
                [InlineKeyboardButton("HXN CHEAT", callback_data="claim_trial_hxn"), InlineKeyboardButton("LK TEAM", callback_data="claim_trial_lk")],
                [InlineKeyboardButton("HEX BLADE", callback_data="claim_trial_hex"), InlineKeyboardButton("ALPHA-X-STORE", callback_data="claim_trial_alpha")],
                [InlineKeyboardButton("BR MODS", callback_data="claim_trial_brmods"), InlineKeyboardButton("XTFFH4X STREAMER", callback_data="claim_trial_xtffh4x")],
                [InlineKeyboardButton("HOT STREAMER", callback_data="claim_trial_hotstreamer"), InlineKeyboardButton("STREAMER X", callback_data="claim_trial_streamerx")],
                [InlineKeyboardButton("BOOYAH PANEL", callback_data="claim_trial_boyyah"), InlineKeyboardButton("ELITE TEAM", callback_data="claim_trial_eliteteam")],
                [InlineKeyboardButton("NGO TRAN", callback_data="claim_trial_ngo"), InlineKeyboardButton("GREED PANEL", callback_data="claim_trial_greed")],
                [InlineKeyboardButton("LK TEAM PRO", callback_data="claim_trial_lkpro"), InlineKeyboardButton("KIWMODZ EXE", callback_data="claim_trial_kiwmodz")],
                [InlineKeyboardButton("XYZ SUPREME", callback_data="claim_trial_xyz"), InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="main_menu")]
            ]
            await query.edit_message_text("🎁 <b>TRIAL KEYS</b>\n\nSelect a product to get a 1-Day Trial Key.\n⚠️ <i>You can only claim ONE trial key every 24 hours. Leaving the channel to cheat will result in a PERMANENT BAN.</i>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
            return

        all_buttons = []
        for wp in web_products:
            section = wp.get("section", "Both")
            if section in ["Trial Only", "Both", "trial", "both"]:
                name = (wp.get("display_name") or wp.get("name", "").upper().replace("_", " ")) + " TRIAL"
                callback = f"claim_trial_{wp.get('name', '').lower()}"
                all_buttons.append(InlineKeyboardButton(name, callback_data=callback))
                
        keyboard = []
        for i in range(0, len(all_buttons), 2):
            keyboard.append(all_buttons[i:i+2])
        keyboard.append([InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="main_menu")])
        await query.edit_message_text("🎁 <b>TRIAL KEYS</b>\n\nSelect a product to get a 1-Day Trial Key.\n⚠️ <i>You can only claim ONE trial key every 24 hours. Leaving the channel to cheat will result in a PERMANENT BAN.</i>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
        return
        
    if data.startswith("claim_trial_"):
        settings = load_settings()
        if settings.get("trial_locked", False):
            msg = settings.get("trial_locked_msg", "🚫 <b>TRIAL SECTION LOCKED</b> 🚫\n\n<b>NO FEEDBACK AND SUPPORT KEY</b>\n<b>STOP ASK OWNER :-</b>@JFHAXX01\n<b>OR DEVLOPER :-</b>@rajput_harshil")
            kb = [[InlineKeyboardButton("« Back", callback_data="main_menu")]]
            await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
            return

        product = data.split("_")[2]
        user_id = str(update.effective_user.id)
        
        locked_products = settings.get("locked_products", {})
        if product in locked_products:
            msg = locked_products[product]
            kb = [[InlineKeyboardButton("« Back", callback_data="trial_key")]]
            await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
            return
            
        # Check channel
        if not await check_force_sub(update.effective_user.id, context):
            await query.answer("⚠️ You must join the channel first!", show_alert=True)
            return
            
        trials = load_trials()
        user_trial = trials.get(user_id, {"last_trial": 0, "strikes": 0, "banned": False})
        
        # Determine cooldown time for this product
        settings = load_settings()
        trial_cooldowns = settings.get("trial_cooldowns", {})
        
        if product in trial_cooldowns:
            cooldown_days = float(trial_cooldowns[product])
        elif "default" in trial_cooldowns:
            cooldown_days = float(trial_cooldowns["default"])
        else:
            cooldown_days = float(settings.get("trial_cooldown_days", 1.0))
            
        cooldown_time = cooldown_days * 24 * 60 * 60
        
        # Global trial history
        product_last_trial = user_trial.get("last_trial", 0)
        time_since_last = time.time() - product_last_trial
        
        if time_since_last < cooldown_time:
            remaining_seconds = int(cooldown_time - time_since_last)
            h, remainder = divmod(remaining_seconds, 3600)
            m, s = divmod(remainder, 60)
            keyboard = [[InlineKeyboardButton("« Back", callback_data="trial_key")]]
            
            last_key = user_trial.get("last_key", "None")
            last_prod = user_trial.get("last_product", "Any Product").upper()
                
            msg = f"⏳ <b>TRIAL COOLDOWN</b>\n━━━━━━━━━━━━━━\nPlease wait for {h}h {m}m {s}s.\nYou can claim your next {last_prod} trial key after this time."
            if last_key != "None":
                msg += f"\n\n🔑 <b>Your Last Key ({last_prod}):</b>\n<code>{last_key}</code>"
                
            await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
            return
            
        # Give key
        keys = load_keys()
        dict_key = f"{product}_trial"
        
        delivered_key = None
        if product == "hxn":
            delivered_key = await generate_key_from_api("hxn", "1d")
        elif dict_key in keys and len(keys[dict_key]) > 0:
            delivered_key = keys[dict_key].pop(0)
            save_keys(keys)
            
        if delivered_key:
            user_trial["last_trial"] = time.time()
            user_trial["last_key"] = delivered_key
            user_trial["last_product"] = product.upper()
            
            if "history" not in user_trial:
                user_trial["history"] = {}
            user_trial["history"][product] = {
                "last_trial": time.time(),
                "last_key": delivered_key
            }
            
            trials[user_id] = user_trial
            save_trials(trials)
            
            try:
                hist = load_trial_history()
                hist.append({
                    "user_id": user_id,
                    "username": update.effective_user.username or update.effective_user.first_name,
                    "product": product,
                    "key": delivered_key,
                    "time": time.time()
                })
                save_trial_history(hist[-50:])
            except:
                pass
            
            await query.edit_message_text(f"✅ <b>TRIAL KEY GENERATED</b>\n━━━━━━━━━━━━━━━━━━\n🏺 <b>Product:</b> {product.upper()}\n🔑 <b>Key:</b> <code>{delivered_key}</code>\n\n<i>Enjoy your trial! Do not leave the channel, or you will be banned.</i>\n\nhttps://t.me/JFFREEAPK\njoin this for apk", parse_mode="HTML")
        else:
            keyboard = [[InlineKeyboardButton("« Back", callback_data="trial_key")]]
            await query.edit_message_text(f"❌ <b>OUT OF STOCK</b>\n━━━━━━━━━━━━━━\nNo trial keys available for {product.upper()} right now.\n\nPlease ask the Admin to restock them.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
        return


    if data == "admin_add_keys":
        if update.effective_user.id not in settings["admin_ids"]: return
        web_products = load_web_products()
        if not web_products:
            keyboard = [
                [InlineKeyboardButton("HXN", callback_data="bulk_prod_hxn"), InlineKeyboardButton("LK", callback_data="bulk_prod_lk")],
                [InlineKeyboardButton("HEX", callback_data="bulk_prod_hex"), InlineKeyboardButton("ALPHA", callback_data="bulk_prod_alpha")],
                [InlineKeyboardButton("PRIME", callback_data="bulk_prod_prime"), InlineKeyboardButton("HARSHIL", callback_data="bulk_prod_harshil")],
                [InlineKeyboardButton("TRINITY X", callback_data="bulk_prod_trinity"), InlineKeyboardButton("FLUORITE", callback_data="bulk_prod_fluorite")],
                [InlineKeyboardButton("SVJ", callback_data="bulk_prod_svj"), InlineKeyboardButton("BR MODS", callback_data="bulk_prod_brmods")],
                [InlineKeyboardButton("BEYOND", callback_data="bulk_prod_beyond"), InlineKeyboardButton("ROGERIO", callback_data="bulk_prod_rogerio")],
                [InlineKeyboardButton("HAWK", callback_data="bulk_prod_hwak"), InlineKeyboardButton("RAPID CORE", callback_data="bulk_prod_rapid")],
                [InlineKeyboardButton("DAEMON PHONK", callback_data="bulk_prod_daemon"), InlineKeyboardButton("HXN STREAMER", callback_data="bulk_prod_streamerxsh")],
                [InlineKeyboardButton("BS SECURE LOADER", callback_data="bulk_prod_bssecure"), InlineKeyboardButton("HYDRA ENGINE 8BP", callback_data="bulk_prod_hydra")],
                [InlineKeyboardButton("XTFFH4X STREAMER", callback_data="bulk_prod_xtffh4x_streamer")],
                [InlineKeyboardButton("STREAMER X", callback_data="bulk_prod_streamerx"), InlineKeyboardButton("BOOYAH PANEL", callback_data="bulk_prod_boyyah")],
                [InlineKeyboardButton("ELITE TEAM", callback_data="bulk_prod_eliteteam"), InlineKeyboardButton("NGO TRAN", callback_data="bulk_prod_ngo")],
                [InlineKeyboardButton("GREED PANEL", callback_data="bulk_prod_greed"), InlineKeyboardButton("LK TEAM PRO", callback_data="bulk_prod_lkpro")],
                [InlineKeyboardButton("KIWMODZ EXE", callback_data="bulk_prod_kiwmodz"), InlineKeyboardButton("XYZ SUPREME", callback_data="bulk_prod_xyz")],
                [InlineKeyboardButton("« Back to Admin Panel", callback_data="admin_panel_cb")]
            ]
            context.user_data["state"] = "awaiting_bulk_product"
            await query.edit_message_text("🛒 <b>Select Product to Add Keys:</b>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
            return

        all_buttons = []
        for wp in web_products:
            name = wp.get("display_name") or wp.get("name", "").upper().replace("_", " ")
            callback = f"bulk_prod_{wp.get('name', '').lower()}"
            all_buttons.append(InlineKeyboardButton(name, callback_data=callback))
            
        keyboard = []
        for i in range(0, len(all_buttons), 2):
            keyboard.append(all_buttons[i:i+2])
        keyboard.append([InlineKeyboardButton("« Back to Admin Panel", callback_data="admin_panel_cb")])
        context.user_data["state"] = "awaiting_bulk_product"
        await query.edit_message_text("🛒 <b>Select Product to Add Keys:</b>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
        return

    if data.startswith("bulk_prod_"):
        if update.effective_user.id not in settings["admin_ids"]: return
        product = "_".join(data.split("_")[2:])
        context.user_data["bulk_product"] = product
        keys = load_keys()
        # Count stock per duration
        stock_1d = len(keys.get(f"{product}_1d", []))
        stock_7d = len(keys.get(f"{product}_7d", []))
        stock_15d = len(keys.get(f"{product}_15d", []))
        stock_30d = len(keys.get(f"{product}_30d", []))
        stock_trial = len(keys.get(f"{product}_trial", []))
        total = stock_1d + stock_7d + stock_15d + stock_30d + stock_trial
        keyboard = [
            [InlineKeyboardButton(f"➕ 1 Day", callback_data="bulk_dur_1d"), InlineKeyboardButton(f"➕ 7 Days", callback_data="bulk_dur_7d")],
            [InlineKeyboardButton(f"➕ 15 Days", callback_data="bulk_dur_15d"), InlineKeyboardButton(f"➕ 30 Days", callback_data="bulk_dur_30d")],
            [InlineKeyboardButton(f"➕ Trial Keys", callback_data="bulk_dur_trial")],
            [InlineKeyboardButton(f"🗑 1D ({stock_1d})", callback_data=f"clrstk_{product}_1d"), InlineKeyboardButton(f"🗑 7D ({stock_7d})", callback_data=f"clrstk_{product}_7d")],
            [InlineKeyboardButton(f"🗑 15D ({stock_15d})", callback_data=f"clrstk_{product}_15d"), InlineKeyboardButton(f"🗑 30D ({stock_30d})", callback_data=f"clrstk_{product}_30d")],
            [InlineKeyboardButton(f"🗑 Trial ({stock_trial})", callback_data=f"clrstk_{product}_trial"), InlineKeyboardButton(f"🗑 ALL ({total})", callback_data=f"clrstk_{product}_all")],
            [InlineKeyboardButton("⬅️ Back", callback_data="admin_add_keys")]
        ]
        await query.edit_message_text(
            f"⏳ <b>{product.upper()}</b>\n━━━━━━━━━━━━━━━━━━\n"
            f"📦 <b>Current Stock:</b>\n"
            f"• 1 Day: {stock_1d} keys\n"
            f"• 7 Days: {stock_7d} keys\n"
            f"• 15 Days: {stock_15d} keys\n"
            f"• 30 Days: {stock_30d} keys\n"
            f"• Trial: {stock_trial} keys\n"
            f"• <b>Total: {total} keys</b>\n\n"
            f"Select ➕ to add keys or 🗑 to clear stock:",
            reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML"
        )
        return

    if data.startswith("clrstk_"):
        if update.effective_user.id not in settings["admin_ids"]: return
        parts = data.split("_")
        # clrstk_{product}_{duration} - product can have underscores
        duration = parts[-1]
        product = "_".join(parts[1:-1])
        keys = load_keys()
        cleared_count = 0
        if duration == "all":
            for dur in ["1d", "3d", "7d", "15d", "30d", "trial"]:
                dict_key = f"{product}_{dur}"
                if dict_key in keys:
                    cleared_count += len(keys[dict_key])
                    del keys[dict_key]
        else:
            dict_key = f"{product}_{duration}"
            if dict_key in keys:
                cleared_count = len(keys[dict_key])
                del keys[dict_key]
        save_keys(keys)
        dur_label = "ALL durations" if duration == "all" else duration.upper()
        keyboard = [[InlineKeyboardButton("« Back", callback_data=f"bulk_prod_{product}")]]
        await query.edit_message_text(
            f"✅ <b>STOCK CLEARED</b>\n━━━━━━━━━━━━━━\n"
            f"🏺 Product: <b>{product.upper()}</b>\n"
            f"⏱ Duration: <b>{dur_label}</b>\n"
            f"🗑 Deleted: <b>{cleared_count} keys</b>",
            reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML"
        )
        return

    if data.startswith("clear_stock_"):
        if update.effective_user.id not in settings["admin_ids"]: return
        product = "_".join(data.split("_")[2:])
        keys = load_keys()
        cleared_count = 0
        for dur in ["1d", "3d", "7d", "15d", "30d", "trial"]:
            dict_key = f"{product}_{dur}"
            if dict_key in keys:
                cleared_count += len(keys[dict_key])
                del keys[dict_key]
        save_keys(keys)
        keyboard = [[InlineKeyboardButton("« Back", callback_data=f"bulk_prod_{product}")]]
        await query.edit_message_text(f"✅ <b>STOCK CLEARED</b>\n━━━━━━━━━━━━━━\nSuccessfully deleted {cleared_count} keys for {product.upper()}.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
        return
        
    if data.startswith("bulk_dur_"):
        if update.effective_user.id not in settings["admin_ids"]: return
        duration = data.split("_")[2]
        context.user_data["bulk_duration"] = duration
        context.user_data["state"] = "awaiting_bulk_keys"
        product = context.user_data.get("bulk_product", "Unknown")
        keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data="admin_add_keys")]]
        await query.edit_message_text(f"📝 <b>SEND KEYS NOW</b>\n━━━━━━━━━━━━━━━━━━\nProduct: {product.upper()}\nDuration: {duration.upper()}\n\nSend me the keys as a normal message. You can send 1 key, or a list of multiple keys (separated by spaces or new lines).", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
        return

    if data == "shop":
        text = "🛒 <b>SELECT A PRODUCT</b>\n━━━━━━━━━━━━━━\nChoose the mod you want to purchase below:"
        keyboard = get_shop_keyboard(update.effective_user.id)
        if query.message.photo or query.message.document:
            await query.message.delete()
            await context.bot.send_message(chat_id=query.message.chat_id, text=text, reply_markup=keyboard, parse_mode="HTML")
        else:
            await query.edit_message_text(text=text, reply_markup=keyboard, parse_mode="HTML")
    elif data == "main_menu":
        await query.edit_message_text(
            settings["welcome_text"].format(name=update.effective_user.first_name),
            reply_markup=get_main_menu_keyboard(),
            parse_mode="HTML"
        )
    elif data == "profile":
        balances = load_balances()
        user_bal = balances.get(str(update.effective_user.id), 0.0)
        
        await query.edit_message_text(
            f"👤 <b>YOUR PROFILE</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"👤 <b>Name:</b> {update.effective_user.first_name}\n"
            f"🆔 <b>User ID:</b> <code>{update.effective_user.id}</code>\n"
            f"💰 <b>Balance:</b> ₹{user_bal:.2f}\n"
            f"📦 <b>Total Orders:</b> 0\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "<i>Your profile is fully verified.</i>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Back to Menu", callback_data="main_menu")]]),
            parse_mode="HTML"
        )
    elif data == "add_balance":
        context.user_data["state"] = "awaiting_balance_amount"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("« Back", callback_data="main_menu")]])
        if query.message.photo:
            await query.message.delete()
            await context.bot.send_message(chat_id=query.message.chat_id, text="💰 <b>ADD BALANCE</b>\n━━━━━━━━━━━━━━━━━━\nPlease type the amount you want to add to your wallet in INR (₹).", reply_markup=keyboard, parse_mode="HTML")
        else:
            await query.edit_message_text(
                "💰 <b>ADD BALANCE</b>\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "Please type the amount you want to add to your wallet in INR (₹).",
                reply_markup=keyboard,
                parse_mode="HTML"
            )
            
    elif data.startswith("balconfirm_"):
        parts = data.split("_")
        order_id = parts[1]
        amount = float(parts[2])
        username = f"@{query.from_user.username}" if query.from_user.username else query.from_user.first_name
        user_id = query.from_user.id
        
        settings = load_settings()
        admin_messages = {}
        msg = (
            "💰 <b>NEW BALANCE REQUEST</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"👤 <b>User:</b> {username} (<code>{user_id}</code>)\n"
            f"💵 <b>Amount:</b> ₹{amount:.2f}\n"
            f"🆔 <b>Order ID:</b> <code>{order_id}</code>\n\n"
            "<i>Please verify the payment and add balance.</i>"
        )
        for admin_id in settings.get("admin_ids", []):
            try:
                kb = [[InlineKeyboardButton("✅ Approve", callback_data=f"balapp_{user_id}_{amount}_{order_id}"), InlineKeyboardButton("❌ Reject", callback_data=f"balrej_{user_id}_{order_id}")]]
                sent_msg = await context.bot.send_message(chat_id=admin_id, text=msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
                admin_messages[str(admin_id)] = sent_msg.message_id
            except:
                pass
                
        save_order_messages(order_id, {"status": "pending", "messages": admin_messages, "text": msg, "is_photo": False})
        
        await query.edit_message_caption(caption="✅ <b>Request Sent!</b>\n━━━━━━━━━━━━━━━━━━\nThe admin has been notified. Your balance will be added once the payment is verified.", parse_mode="HTML") if query.message.photo else await query.edit_message_text(text="✅ <b>Request Sent!</b>\n━━━━━━━━━━━━━━━━━━\nThe admin has been notified. Your balance will be added once the payment is verified.", parse_mode="HTML")

    elif data.startswith("balapp_"):
        if update.effective_user.id not in settings.get("admin_ids", []): return
        parts = data.split("_")
        user_id = parts[1]
        amount = float(parts[2])
        order_id = parts[3] if len(parts) > 3 else "Unknown"
        
        order_data = load_order_messages(order_id)
        if order_data.get("status", "pending") != "pending":
            await query.answer(f"⚠️ Already {order_data['status'].upper()} by another admin!", show_alert=True)
            status_text = f"\n\n⚠️ <b>ALREADY {order_data['status'].upper()}</b>"
            try:
                await query.edit_message_text(text=query.message.text + status_text, reply_markup=None, parse_mode="HTML")
            except:
                pass
            return
            
        order_data["status"] = "approved"
        save_order_messages(order_id, order_data)
        
        balances = load_balances()
        balances[user_id] = balances.get(user_id, 0.0) + amount
        save_balances(balances)
        
        try:
            await context.bot.send_message(chat_id=user_id, text=f"✅ <b>BALANCE ADDED!</b>\n━━━━━━━━━━━━━━━━━━\n₹{amount:.2f} has been added to your wallet.\n💰 <b>New Balance:</b> ₹{balances[user_id]:.2f}", parse_mode="HTML")
        except:
            pass
            
        for admin_id, msg_id in order_data.get("messages", {}).items():
            try:
                if int(admin_id) == query.from_user.id:
                    orig_text = order_data.get("text", "")
                    update_text = (
                        f"\n\n✅ <b>APPROVED</b>\n"
                        f"👤 <b>Approved by:</b> {query.from_user.first_name}\n"
                        f"💰 Added ₹{amount:.2f} to {user_id}"
                    )
                    await context.bot.edit_message_text(
                        chat_id=int(admin_id),
                        message_id=msg_id,
                        text=orig_text + update_text,
                        reply_markup=None,
                        parse_mode="HTML"
                    )
                else:
                    await context.bot.delete_message(chat_id=int(admin_id), message_id=msg_id)
            except Exception as e:
                logger.error(f"Error updating/deleting admin message {admin_id}: {e}")
        
    elif data.startswith("balrej_"):
        if update.effective_user.id not in settings.get("admin_ids", []): return
        parts = data.split("_")
        user_id = parts[1]
        order_id = parts[2] if len(parts) > 2 else "Unknown"
        
        order_data = load_order_messages(order_id)
        if order_data.get("status", "pending") != "pending":
            await query.answer(f"⚠️ Already {order_data['status'].upper()} by another admin!", show_alert=True)
            status_text = f"\n\n⚠️ <b>ALREADY {order_data['status'].upper()}</b>"
            try:
                await query.edit_message_text(text=query.message.text + status_text, reply_markup=None, parse_mode="HTML")
            except:
                pass
            return
            
        order_data["status"] = "rejected"
        save_order_messages(order_id, order_data)
        
        try:
            await context.bot.send_message(chat_id=user_id, text="❌ <b>BALANCE REQUEST REJECTED</b>\n━━━━━━━━━━━━━━━━━━\nYour payment could not be verified. Please contact support.", parse_mode="HTML")
        except:
            pass
            
        for admin_id, msg_id in order_data.get("messages", {}).items():
            try:
                if int(admin_id) == query.from_user.id:
                    orig_text = order_data.get("text", "")
                    update_text = (
                        f"\n\n❌ <b>REJECTED</b>\n"
                        f"👤 <b>Rejected by:</b> {query.from_user.first_name}"
                    )
                    await context.bot.edit_message_text(
                        chat_id=int(admin_id),
                        message_id=msg_id,
                        text=orig_text + update_text,
                        reply_markup=None,
                        parse_mode="HTML"
                    )
                else:
                    await context.bot.delete_message(chat_id=int(admin_id), message_id=msg_id)
            except Exception as e:
                logger.error(f"Error updating/deleting admin message {admin_id}: {e}")
    elif data == "history":
        logs = load_user_history(query.from_user.id)
        if logs:
            history_text = "\n".join(logs[-10:])
            text = f"📋 <b>YOUR ORDER HISTORY</b>\n━━━━━━━━━━━━━━━━━━\n{history_text}\n<i>Showing your last 10 purchases.</i>"
        else:
            text = (
                "📋 <b>ORDER HISTORY</b>\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "❌ <b>No orders found!</b>\n\n"
                "Your previous purchases will appear here once they are verified."
            )
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Back", callback_data="main_menu")]]), parse_mode="HTML")
    elif data == "referral":
        settings = load_settings()
        if settings.get("refer_locked", False):
            await query.answer("❌ The Referral System is currently paused by the Admin.", show_alert=True)
            return
            
        bot_username = (await context.bot.get_me()).username
        referral_link = f"https://t.me/{bot_username}?start={update.effective_user.id}"
        refs = load_referrals()
        user_refs = refs.get("users", {}).get(str(update.effective_user.id), {"count": 0, "earnings": 0.0})
        count = user_refs["count"]
        earnings = user_refs["earnings"]
        await query.edit_message_text(
            "🎁 <b>REFERRAL SYSTEM</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Invite your friends and earn ₹10 to your wallet per invite!\n\n"
            f"🔗 <b>Your Link:</b>\n<code>{referral_link}</code>\n\n"
            f"👥 <b>Total Referrals:</b> {count}\n"
            f"💰 <b>Earnings:</b> ₹{earnings:.2f}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Back", callback_data="main_menu")]]),
            parse_mode="HTML"
        )
    elif data == "how_to_use":
        await query.edit_message_text(
            "🎬 <b>HOW TO USE THE BOT</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "1️⃣ <b>Verify:</b> Share your contact for security.\n"
            "2️⃣ <b>Shop:</b> Select your favorite mod/cheat.\n"
            "3️⃣ <b>Pay:</b> Scan the QR code and pay.\n"
            "4️⃣ <b>Confirm:</b> Send the UTR/Screenshot.\n"
            "5️⃣ <b>Receive:</b> Get your key instantly!\n\n"
            "📞 <b>Need help?</b> Contact @JFHAXX01",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Back", callback_data="main_menu")]]),
            parse_mode="HTML"
        )
    elif data == "helpline":
        await query.edit_message_text(
            "📞 <b>CONNECT HELPLINE</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "If you have any issues with payments or keys, contact our official support:\n\n"
            "👤 <b>Support:</b> @JFHAXX01\n"
            "⏰ <b>Active:</b> 10 AM - 10 PM",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Back", callback_data="main_menu")]]),
            parse_mode="HTML"
        )
    elif data == "lucky_game":
        await query.edit_message_text(
            "🎰 <b>LUCKY SPIN GAME</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Try your luck and win free keys or balance!\n\n"
            "⚠️ <i>Coming soon in the next update...</i>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Back", callback_data="main_menu")]]),
            parse_mode="HTML"
        )
    elif data.startswith("product_"):
        product_key = data.replace("product_", "").lower()
        product_name = data.replace("product_", "").upper().replace("_", " ")
        
        # Load prices from database
        prices = {"1d": 50, "7d": 200, "15d": 400, "30d": 600}
        web_products = load_web_products()
        for wp in web_products:
            wp_name = wp.get("name", "").lower()
            if wp_name == product_key or wp_name.startswith(product_key):
                prices = wp.get("prices", prices)
                break
                
        # Load stock (from keys)
        keys_data = load_keys()
        
        # Get stock length
        def get_stock(d_label):
            dict_key = f"{product_key}_{d_label}"
            return len(keys_data.get(dict_key, []))
            
        stock_1d = get_stock("1d")
        stock_7d = get_stock("7d")
        stock_15d = get_stock("15d")
        stock_30d = get_stock("30d")
        
        # Format the text dynamically
        price_text = (
            f"🛒 <b>{product_name}</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📦 <b>Package Info:</b>\n"
            f"┠ <b>1 DAY : ₹{prices.get('1d', 50)}</b> - {stock_1d} stock\n"
            f"{'✅ <b>Stock Available</b>' if stock_1d > 0 else '❌ <b>Out of Stock</b>'}\n\n"
            f"┠ <b>7 DAY : ₹{prices.get('7d', 200)}</b> - {stock_7d} stock\n"
            f"{'✅ <b>Stock Available</b>' if stock_7d > 0 else '❌ <b>Out of Stock</b>'}\n\n"
            f"┠ <b>15 DAY : ₹{prices.get('15d', 400)}</b> - {stock_15d} stock\n"
            f"{'✅ <b>Stock Available</b>' if stock_15d > 0 else '❌ <b>Out of Stock</b>'}\n\n"
            f"┠ <b>30 DAY : ₹{prices.get('30d', 600)}</b> - {stock_30d} stock\n"
            f"{'✅ <b>Stock Available</b>' if stock_30d > 0 else '❌ <b>Out of Stock</b>'}\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "<i>Prices are auto-calculated based on your tier.</i>"
        )
        
        keyboard = [
            [InlineKeyboardButton(f"🛒 1 Day - ₹{prices.get('1d', 50)}", callback_data=f"buy_{data}_1d")],
            [InlineKeyboardButton(f"🛒 7 Day - ₹{prices.get('7d', 200)}", callback_data=f"buy_{data}_7d")],
            [InlineKeyboardButton(f"🛒 15 Day - ₹{prices.get('15d', 400)}", callback_data=f"buy_{data}_15d")],
            [InlineKeyboardButton(f"🛒 30 Day - ₹{prices.get('30d', 600)}", callback_data=f"buy_{data}_30d")],
            [InlineKeyboardButton("« Back To Store", callback_data="shop")]
        ]
        
        await query.edit_message_text(
            price_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
    elif data.startswith("buy_"):
        parts = data.split("_")
        product_key = parts[2]
        duration = parts[3]
        
        duration_map = {"1d": "1 Days", "7d": "7 Days", "15d": "15 Days", "30d": "30 Days"}
        price_map = {"1d": "50.00", "7d": "200.00", "15d": "400.00", "30d": "600.00"}
        
        web_products = load_web_products()
        for wp in web_products:
            wp_name = wp.get("name", "").lower()
            if wp_name == product_key.lower() or wp_name.startswith(product_key.lower()):
                p_prices = wp.get("prices", {})
                if p_prices:
                    price_map = {
                        "1d": str(p_prices.get("1d", 50)),
                        "7d": str(p_prices.get("7d", 200)),
                        "15d": str(p_prices.get("15d", 400)),
                        "30d": str(p_prices.get("30d", 600)),
                    }
                break
        
        product_name = product_key.upper()
        days = duration_map.get(duration, duration)
        amount = price_map.get(duration, "0.00")
        order_id = "OID" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        # Store transaction details
        context.user_data["product"] = product_key
        context.user_data["amount"] = amount
        context.user_data["duration"] = duration
        context.user_data["order_id"] = order_id
        
        user_id_str = str(query.from_user.id)
        balances = load_balances()
        resellers = load_resellers()
        
        user_bal = balances.get(user_id_str, 0.0)
        float_amount = float(amount)
        is_reseller = user_id_str in resellers and time.time() < resellers[user_id_str]
        
        if is_reseller:
            float_amount = float_amount * 0.7  # 30% Discount
            amount = f"{float_amount:.2f}"
            context.user_data["amount"] = amount
            
        await query.message.delete()
        
        is_admin = query.from_user.id in settings.get("admin_ids", [])
        if is_admin or user_bal >= float_amount:
            wallet_locked = settings.get("wallet_buy_locked", False)
            locked_prods = settings.get("wallet_locked_products", [])
            locked_prods_lower = [p.lower() for p in locked_prods]
            product_locked = (
                product_key.lower() in locked_prods_lower or
                duration.lower() in locked_prods_lower or
                f"{product_key.lower()}_{duration.lower()}" in locked_prods_lower
            )
            
            from datetime import datetime
            today_str = datetime.now().strftime("%Y-%m-%d")
            wp = load_wallet_purchases()
            already_bought_today = (wp.get(user_id_str, "") == today_str)
            
            if not is_admin and (wallet_locked or product_locked or already_bought_today) and not is_reseller:
                title = "❌ <b>WALLET PURCHASE DISABLED</b>"
                reason_msg = "⚠️ <i>You have already purchased 1 key today using Wallet balance. Please pay using the QR code below for additional purchases.</i>" if already_bought_today else "⚠️ <i>Wallet payments are temporarily disabled for this product/action for normal users by Admin. Please pay using the QR code below.</i>"
                full_payment_text = (
                    "<b>Status:</b> <code>Wallet Disabled</code>\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    f"{reason_msg}\n\n"
                    f"{title}\n\n"
                    f"🏺 <b>Product:</b> {product_name}\n"
                    f"⏳ <b>Duration:</b> {days}\n"
                    f"💵 <b>Pay Amount:</b> ₹{amount}\n"
                    f"💰 <b>Your Balance:</b> ₹{user_bal:.2f}\n"
                    f"🆔 <b>Order ID:</b>\n<code>{order_id}</code>\n\n"
                    "<i>Scan the QR code to pay, then click 'Paid Confirmation'.</i>"
                )
                full_keyboard = [
                    [InlineKeyboardButton("✅ Paid Confirmation", callback_data=f"confirm_{order_id}")],
                    [InlineKeyboardButton("« Back to Store", callback_data="shop")]
                ]
                if os.path.exists("qr.png"):
                    await context.bot.send_photo(
                        chat_id=query.message.chat_id,
                        photo=open("qr.png", "rb"),
                        caption=full_payment_text,
                        reply_markup=InlineKeyboardMarkup(full_keyboard),
                        parse_mode="HTML"
                    )
                else:
                    await context.bot.send_message(
                        chat_id=query.message.chat_id,
                        text=full_payment_text + "\n\n⚠️ <i>(QR Code image missing on server)</i>",
                        reply_markup=InlineKeyboardMarkup(full_keyboard),
                        parse_mode="HTML"
                    )
            else:
                if is_admin:
                    title = "👑 <b>ADMIN CHECKOUT</b>"
                elif is_reseller:
                    title = "👑 <b>VIP RESELLER CHECKOUT (30% OFF)</b>"
                else:
                    title = "✅ <b>SUFFICIENT BALANCE</b>"
                full_payment_text = (
                    "<b>Status:</b> <code>Ready to Checkout</code>\n"
                    "<i>Pay using your Wallet Balance.</i>\n\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    f"{title}\n\n"
                    f"🏺 <b>Product:</b> {product_name}\n"
                    f"⏳ <b>Duration:</b> {days}\n"
                    f"💵 <b>Pay Amount:</b> ₹{amount}\n"
                    f"💰 <b>Your Balance:</b> ₹{user_bal:.2f}\n\n"
                    "<i>Click '💰 Pay with Wallet' to buy instantly.</i>"
                )
                full_keyboard = [
                    [InlineKeyboardButton("💰 Pay with Wallet", callback_data=f"walletpay_{order_id}")],
                    [InlineKeyboardButton("« Back to Store", callback_data="shop")]
                ]
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text=full_payment_text,
                    reply_markup=InlineKeyboardMarkup(full_keyboard),
                    parse_mode="HTML"
                )
        else:
            title = "👑 <b>VIP RESELLER CHECKOUT (30% OFF)</b>" if is_reseller else "⚠️ <b>INSUFFICIENT BALANCE</b>"
            full_payment_text = (
                "<b>Status:</b> <code>Waiting for Payment...</code>\n"
                "<i>Pay using the QR code below.</i>\n\n"
                "━━━━━━━━━━━━━━━━━━\n"
                f"{title}\n\n"
                f"🏺 <b>Product:</b> {product_name}\n"
                f"⏳ <b>Duration:</b> {days}\n"
                f"💵 <b>Pay Amount:</b> ₹{amount}\n"
                f"💰 <b>Your Balance:</b> ₹{user_bal:.2f}\n"
                f"🆔 <b>Order ID:</b>\n<code>{order_id}</code>\n\n"
                "<i>Scan the QR code to pay, then click 'Paid Confirmation'.</i>"
            )
            
            full_keyboard = [
                [InlineKeyboardButton("✅ Paid Confirmation", callback_data=f"confirm_{order_id}")],
                [InlineKeyboardButton("« Back to Store", callback_data="shop")]
            ]
            
            if os.path.exists("qr.png"):
                await context.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=open("qr.png", "rb"),
                    caption=full_payment_text,
                    reply_markup=InlineKeyboardMarkup(full_keyboard),
                    parse_mode="HTML"
                )
            else:
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text=full_payment_text + "\n\n⚠️ <i>(QR Code image missing on server)</i>",
                    reply_markup=InlineKeyboardMarkup(full_keyboard),
                    parse_mode="HTML"
                )

    elif data.startswith("walletpay_"):
        try:
            debug_log(f"Clicked walletpay: {data}")
            user_id_str = str(query.from_user.id)
            resellers = load_resellers()
            is_reseller = user_id_str in resellers and time.time() < resellers[user_id_str]
            settings = load_settings()
            product = context.user_data.get("product", "hxn").lower()
            duration = context.user_data.get("duration", "1d").lower()
            wallet_locked = settings.get("wallet_buy_locked", False)
            locked_prods = settings.get("wallet_locked_products", [])
            locked_prods_lower = [p.lower() for p in locked_prods]
            product_locked = (
                product in locked_prods_lower or
                duration in locked_prods_lower or
                f"{product}_{duration}" in locked_prods_lower
            )
            from datetime import datetime
            today_str = datetime.now().strftime("%Y-%m-%d")
            wp = load_wallet_purchases()
            already_bought_today = (wp.get(user_id_str, "") == today_str)
            is_admin = query.from_user.id in settings.get("admin_ids", [])
            if not is_admin and (wallet_locked or product_locked or already_bought_today) and not is_reseller:
                await query.answer("🚫 You have already purchased 1 key today using Wallet balance.", show_alert=True)
                return
            order_id = data.split("_")[1]
            if context.user_data.get(f"processed_{order_id}"):
                await query.answer("Processing...", show_alert=False)
                return
            context.user_data[f"processed_{order_id}"] = True
            try:
                await query.edit_message_reply_markup(reply_markup=None)
            except:
                pass
            amount = float(context.user_data.get("amount", "0"))
            product = context.user_data.get("product", "hxn")
            duration_label = context.user_data.get("duration", "1d")
        
            user_id_str = str(query.from_user.id)
            balances = load_balances()
            user_bal = balances.get(user_id_str, 0.0)
        
            debug_log(f"user_bal: {user_bal}, amount: {amount}")
            if is_admin or user_bal >= amount:
                debug_log("Sufficient balance")
                if not is_admin:
                    balances[user_id_str] -= amount
                    save_balances(balances)
            
                delivered_key = None
            
                if check_use_api(product):
                    delivered_key = await generate_key_from_api(product, duration_label)
                else:
                    dict_key = f"{product}_{duration_label}"
                    keys = load_keys()
                    if dict_key in keys and len(keys[dict_key]) > 0:
                        delivered_key = keys[dict_key].pop(0)
                        save_keys(keys)
            
                debug_log(f"Delivered key: {delivered_key}")
                if delivered_key:
                    # Save wallet purchase today
                    today_str = datetime.now().strftime("%Y-%m-%d")
                    wp = load_wallet_purchases()
                    wp[user_id_str] = today_str
                    save_wallet_purchases(wp)

                    resellers_check = load_resellers()
                    username_str = f"@{query.from_user.username}" if query.from_user.username else str(query.from_user.first_name)
                
                    if user_id_str in resellers_check:
                        debug_log("Calling log_reseller_action")
                        log_reseller_action(username_str, user_id_str, product, delivered_key)
                        debug_log("log_reseller_action finished")
                    log_user_action(user_id_str, product.upper(), delivered_key)
                    log_activity(user_id_str, f'generated {product} key')
                
                    settings = load_settings()
                    admin_ids = settings.get("admin_ids", [])
                    for admin_id in admin_ids:
                        try:
                            admin_msg = (
                                f"🔔 <b>NEW WALLET PURCHASE</b>\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"👤 <b>User:</b> {username_str} (<code>{user_id_str}</code>)\n"
                                f"🏺 <b>Product:</b> {product.upper()}\n"
                                f"⏳ <b>Duration:</b> {duration_label.upper()}\n"
                                f"💵 <b>Amount Paid:</b> ₹{amount}\n"
                                f"🔑 <b>Key Generated:</b> <code>{delivered_key}</code>\n"
                            )
                            await context.bot.send_message(chat_id=admin_id, text=admin_msg, parse_mode="HTML")
                        except:
                            pass
                
                    remaining_bal = user_bal if is_admin else balances[user_id_str]
                    success_msg = (
                        "✅ <b>PURCHASE SUCCESSFUL!</b>\n"
                        "━━━━━━━━━━━━━━━━━━\n"
                        f"🏺 <b>Product:</b> {product.upper()}\n"
                        f"⏳ <b>Duration:</b> {duration_label.upper()}\n"
                        f"💰 <b>Remaining Balance:</b> ₹{remaining_bal:.2f}\n"
                        "━━━━━━━━━━━━━━━━━━\n"
                        f"🔑 <b>YOUR KEY:</b>\n<code>{delivered_key}</code>\n\n"
                        "<i>Thank you for shopping with us!</i>\n\n"
                        "📱 <b>Get the APK here:</b> https://t.me/JFFREEAPK"
                    )
                    debug_log("Editing success msg")
                    await query.edit_message_text(text=success_msg, parse_mode="HTML")
                    debug_log("Edited success msg")
                else:
                    if not is_admin:
                        balances[user_id_str] += amount
                        save_balances(balances)
                    
                    wl = load_waitlists()
                    if product not in wl: wl[product] = []
                    if user_id_str not in wl[product]:
                        wl[product].append(user_id_str)
                        save_waitlists(wl)
                        
                    await query.answer(f"❌ ERROR! Out of stock for {product.upper()}. Balance refunded.", show_alert=True)
                    await query.edit_message_text(f"❌ Payment refunded due to out-of-stock.\n\n🔔 <b>You are on the Waitlist!</b>\nI will automatically DM you the moment new keys for {product.upper()} are uploaded.", parse_mode="HTML")
            else:
                await query.answer("❌ Insufficient balance!", show_alert=True)



        except Exception as e:
            import traceback
            err = traceback.format_exc()
            await query.edit_message_text(f"⚠️ INTERNAL ERROR:\n<pre>{err[-500:]}</pre>", parse_mode="HTML")
    elif data.startswith("confirm_"):
        order_id = data.split("_")[1]
        confirm_text = (
            f"<b>ORDER ID:</b> <code>{order_id}</code>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📝 <b>STEP 2: CONFIRMATION</b>\n\n"
            "Please send the <b>Transaction ID (UTR)</b> or a <b>Screenshot</b> of your successful payment.\n\n"
            "Our team will verify it and send your key shortly!"
        )
        confirm_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("« Back", callback_data="shop")]])
        
        try:
            if query.message.photo:
                await query.edit_message_caption(caption=confirm_text, reply_markup=confirm_keyboard, parse_mode="HTML")
            else:
                await query.edit_message_text(text=confirm_text, reply_markup=confirm_keyboard, parse_mode="HTML")
        except Exception as e:
            logger.error(f"Error in confirm: {e}")
            
        # Store that this user is now in 'payment_verification' state
        context.user_data["state"] = "awaiting_receipt"
        context.user_data["order_id"] = order_id

    elif data.startswith("approve_"):
        # approve_userid_product_orderid_duration
        parts = data.split("_")
        target_user_id = int(parts[1])
        product = parts[2].lower()
        order_id = parts[3]
        
        # Extract duration from callback data if present, otherwise default to 1d
        if len(parts) > 4:
            duration_label = parts[4]
        else:
            duration_label = context.user_data.get("duration", "1d")
        
        order_data = load_order_messages(order_id)
        if order_data.get("status", "pending") != "pending":
            await query.answer(f"⚠️ Already {order_data['status'].upper()} by another admin!", show_alert=True)
            status_text = f"\n\n⚠️ <b>ALREADY {order_data['status'].upper()}</b>"
            try:
                if query.message.photo:
                    await query.edit_message_caption(caption=query.message.caption + status_text, reply_markup=None, parse_mode="HTML")
                else:
                    await query.edit_message_text(text=query.message.text + status_text, reply_markup=None, parse_mode="HTML")
            except:
                pass
            return

        # 1. GENERATE OR FETCH KEY
        if check_use_api(product):
            delivered_key = await generate_key_from_api(product, duration_label)
        else:
            dict_key = f"{product}_{duration_label}"
            keys = load_keys()
            if dict_key in keys and len(keys[dict_key]) > 0:
                delivered_key = keys[dict_key].pop(0)
                save_keys(keys)
            else:
                delivered_key = None
        
        if delivered_key:
            order_data["status"] = "approved"
            save_order_messages(order_id, order_data)
            
            resellers_check = load_resellers()
            target_str = str(target_user_id)
            if target_str in resellers_check:
                # We don't have their username easily here, so we just use "Reseller"
                log_reseller_action("Reseller", target_str, product, delivered_key)
            log_user_action(target_user_id, product, delivered_key)
                
            # Send Key to User
            success_msg = (
                "✅ <b>PAYMENT VERIFIED!</b>\n"
                "━━━━━━━━━━━━━━━━━━\n"
                f"🏺 <b>Product:</b> {product.upper()}\n"
                f"⏳ <b>Duration:</b> {duration_label.upper()}\n"
                f"🆔 <b>Order ID:</b> <code>{order_id}</code>\n"
                "━━━━━━━━━━━━━━━━━━\n"
                f"🔑 <b>YOUR KEY:</b>\n<code>{delivered_key}</code>\n\n"
                "<i>Thank you for shopping with us!</i>\n\n"
                "📱 <b>Get the APK here:</b> https://t.me/JFFREEAPK"
            )
            try:
                await context.bot.send_message(chat_id=target_user_id, text=success_msg, parse_mode="HTML")
            except Exception as e:
                logger.error(f"Error sending key to user: {e}")
                
            for admin_id, msg_id in order_data.get("messages", {}).items():
                try:
                    if int(admin_id) == query.from_user.id:
                        orig_text = order_data.get("text", "")
                        update_text = (
                            f"\n\n✅ <b>APPROVED & KEY SENT</b>\n"
                            f"👤 <b>Approved by:</b> {query.from_user.first_name}\n"
                            f"🔑 <b>Generated:</b> <code>{delivered_key}</code>"
                        )
                        if order_data.get("is_photo", False):
                            await context.bot.edit_message_caption(
                                chat_id=int(admin_id),
                                message_id=msg_id,
                                caption=orig_text + update_text,
                                reply_markup=None,
                                parse_mode="HTML"
                            )
                        else:
                            await context.bot.edit_message_text(
                                chat_id=int(admin_id),
                                message_id=msg_id,
                                text=orig_text + update_text,
                                reply_markup=None,
                                parse_mode="HTML"
                            )
                    else:
                        await context.bot.delete_message(chat_id=int(admin_id), message_id=msg_id)
                except Exception as e:
                    logger.error(f"Error updating/deleting admin message {admin_id}: {e}")
        else:
            await query.answer(f"❌ ERROR! Could not generate or find a key for {product.upper()}. Out of stock?", show_alert=True)

    elif data.startswith("reject_"):
        parts = data.split("_")
        target_user_id = int(parts[1])
        order_id = parts[2] if len(parts) > 2 else "Unknown"
        
        order_data = load_order_messages(order_id)
        if order_data.get("status", "pending") != "pending":
            await query.answer(f"⚠️ Already {order_data['status'].upper()} by another admin!", show_alert=True)
            status_text = f"\n\n⚠️ <b>ALREADY {order_data['status'].upper()}</b>"
            try:
                if query.message.photo:
                    await query.edit_message_caption(caption=query.message.caption + status_text, reply_markup=None, parse_mode="HTML")
                else:
                    await query.edit_message_text(text=query.message.text + status_text, reply_markup=None, parse_mode="HTML")
            except:
                pass
            return
            
        order_data["status"] = "rejected"
        save_order_messages(order_id, order_data)
        
        try:
            await context.bot.send_message(chat_id=target_user_id, text="❌ <b>Payment Rejected!</b>\nYour payment could not be verified. Please contact support if you think this is a mistake.", parse_mode="HTML")
        except Exception as e:
            logger.error(f"Error notifying user: {e}")
            
        for admin_id, msg_id in order_data.get("messages", {}).items():
            try:
                if int(admin_id) == query.from_user.id:
                    orig_text = order_data.get("text", "")
                    update_text = (
                        f"\n\n❌ <b>REJECTED</b>\n"
                        f"👤 <b>Rejected by:</b> {query.from_user.first_name}"
                    )
                    if order_data.get("is_photo", False):
                        await context.bot.edit_message_caption(
                            chat_id=int(admin_id),
                            message_id=msg_id,
                            caption=orig_text + update_text,
                            reply_markup=None,
                            parse_mode="HTML"
                        )
                    else:
                        await context.bot.edit_message_text(
                            chat_id=int(admin_id),
                            message_id=msg_id,
                            text=orig_text + update_text,
                            reply_markup=None,
                            parse_mode="HTML"
                        )
                else:
                    await context.bot.delete_message(chat_id=int(admin_id), message_id=msg_id)
            except Exception as e:
                logger.error(f"Error updating/deleting admin message {admin_id}: {e}")
    elif data.startswith("refresh_"):
        order_id = data.split("_")[1]
        amount = context.user_data.get("amount", "0")
        product = context.user_data.get("product", "hxn")
        duration_label = context.user_data.get("duration", "1d")

        status_msg = await query.answer("🔄 Checking payment status...", show_alert=False)
        api_status = await verify_utr_api(order_id, amount)
        
        if api_status == "success":
            # 1. GENERATE REAL KEY FROM WEBSITE
            delivered_key = await generate_key_from_api(product, duration_label)
            
            if delivered_key:
                success_msg = (
                    "✅ <b>PAYMENT VERIFIED!</b>\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    f"🏺 <b>Product:</b> {product.upper()}\n"
                    f"⏳ <b>Duration:</b> {duration_label.upper()}\n"
                    f"🆔 <b>Order ID:</b> <code>{order_id}</code>\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    f"🔑 <b>YOUR KEY:</b>\n<code>{delivered_key}</code>\n\n"
                    "<i>Thank you for shopping with us!</i>"
                )
                await context.bot.send_message(chat_id=query.message.chat_id, text=success_msg, parse_mode="HTML")
                await query.edit_message_text("✅ <b>ORDER COMPLETED!</b>\nYour key has been delivered above.")
            else:
                await query.edit_message_text("✅ <b>Payment Verified!</b>\nBut there was an error generating your key. Admin will send it manually.")
        else:
            await query.answer("❌ Payment not found yet. Please pay and wait 30 seconds before clicking again.", show_alert=True)

    elif data == "refresh_pay":
        await query.answer("Payment status: PENDING ⌛\nPlease wait 1-2 minutes after paying.", show_alert=True)
    elif data == "admin_panel_cb":
        if update.effective_user.id not in settings["admin_ids"]: return
        keyboard = [
            [InlineKeyboardButton("➕ Add Reseller", callback_data="admin_guide_add"), InlineKeyboardButton("➖ Remove Reseller", callback_data="admin_guide_remove")],
            [InlineKeyboardButton("📋 Active Resellers", callback_data="admin_listresellers"), InlineKeyboardButton("🔍 View Reseller Logs", callback_data="admin_logsmode")],
            [InlineKeyboardButton("💰 Add Balance", callback_data="admin_guide_bal"), InlineKeyboardButton("📦 Check Stock", callback_data="admin_stock")],
            [InlineKeyboardButton("🔑 Add Keys (Bulk)", callback_data="admin_add_keys"), InlineKeyboardButton("📜 Trial Logs", callback_data="admin_trial_logs")],
            [InlineKeyboardButton("📦 Product Management", callback_data="admin_prod_mgmt")],
            [InlineKeyboardButton("🔄 Reset Trial Cooldown", callback_data="admin_reset_trial")],
            [InlineKeyboardButton("❓ Help Commands", callback_data="admin_help_commands")]
        ]
        await query.edit_message_text("👑 <b>Admin Dashboard</b>\nSelect an option below:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    elif data == "admin_prod_mgmt":
        if update.effective_user.id not in settings["admin_ids"]: return
        keyboard = [
            [InlineKeyboardButton("➕ Add Product", callback_data="admin_add_product_start")],
            [InlineKeyboardButton("⚙️ Manage Products", callback_data="admin_manage_list")],
            [InlineKeyboardButton("📋 View Short Names", callback_data="admin_view_short_names")],
            [InlineKeyboardButton("« Back to Admin Panel", callback_data="admin_panel_cb")]
        ]
        await query.edit_message_text("📦 <b>Product Management Dashboard</b>\nSelect an option below:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    elif data == "admin_view_short_names":
        if update.effective_user.id not in settings["admin_ids"]: return
        web_products = load_web_products()
        if not web_products:
            kb = [[InlineKeyboardButton("« Back", callback_data="admin_prod_mgmt")]]
            await query.edit_message_text("❌ No products found.", reply_markup=InlineKeyboardMarkup(kb))
            return
        
        text = "📋 <b>PRODUCT SHORT NAMES</b>\n━━━━━━━━━━━━━━━━━━\n"
        for wp in web_products:
            name = wp.get("display_name") or wp.get("name", "").upper()
            short_name = wp.get("name", "").lower()
            section = wp.get("section", "Both")
            text += f"• <b>{name}</b>\n  └ Short Name: <code>{short_name}</code> ({section})\n"
        
        text += (
            "\n💡 <i>Give this short name to resellers. Resellers can generate keys using:</i>\n"
            "<code>/gen [short_name] [duration]</code>"
        )
        kb = [[InlineKeyboardButton("« Back", callback_data="admin_prod_mgmt")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
    elif data == "admin_manage_list":
        if update.effective_user.id not in settings["admin_ids"]: return
        web_products = load_web_products()
        if not web_products:
            keyboard = [[InlineKeyboardButton("« Back", callback_data="admin_prod_mgmt")]]
            await query.edit_message_text("❌ No active products found to manage.", reply_markup=InlineKeyboardMarkup(keyboard))
            return
        buttons = []
        for wp in web_products:
            name = wp.get("display_name") or wp.get("name", "").upper()
            cb = f"admin_prod_opt_{wp.get('name', '').lower()}"
            buttons.append(InlineKeyboardButton(name, callback_data=cb))
        keyboard = []
        for i in range(0, len(buttons), 2):
            keyboard.append(buttons[i:i+2])
        keyboard.append([InlineKeyboardButton("« Back", callback_data="admin_prod_mgmt")])
        await query.edit_message_text("⚙️ <b>Select a product to manage:</b>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    elif data.startswith("admin_prod_opt_"):
        if update.effective_user.id not in settings["admin_ids"]: return
        prod_name = "_".join(data.split("_")[3:])
        web_products = load_web_products()
        wp = next((p for p in web_products if p.get("name", "").lower() == prod_name.lower()), None)
        if not wp:
            await query.answer("❌ Product not found.", show_alert=True)
            return
        display_name = wp.get("display_name") or wp.get("name", "").upper().replace("_", " ")
        use_api = wp.get("use_api", False)
        section = wp.get("section", "Both")
        
        status_text = "CONNECTED ✅ (Generates key from Alwaysdata API)" if use_api else "DISABLED ❌ (Uses local stock keys)"
        
        keyboard = [
            [InlineKeyboardButton("🔌 Toggle API Connection", callback_data=f"admin_prod_tglapi_{prod_name}")],
            [InlineKeyboardButton("🗑️ Remove / Delete Product", callback_data=f"admin_rmsel_{prod_name}")],
            [InlineKeyboardButton("« Back to List", callback_data="admin_manage_list")]
        ]
        await query.edit_message_text(
            f"⚙️ <b>PRODUCT SETTINGS: {display_name}</b>\n━━━━━━━━━━━━━━━━━━\n"
            f"📦 <b>Name:</b> {wp.get('name', '')}\n"
            f"📁 <b>Section:</b> {section}\n"
            f"🔌 <b>Alwaysdata API:</b> {status_text}\n"
            f"💡 <i>(Note: Alwaysdata API uses product_id = 1 for all queries)</i>\n"
            "━━━━━━━━━━━━━━━━━━",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
    elif data.startswith("admin_prod_tglapi_"):
        if update.effective_user.id not in settings["admin_ids"]: return
        prod_name = "_".join(data.split("_")[3:])
        web_products = load_web_products()
        changed = False
        for wp in web_products:
            if wp.get("name", "").lower() == prod_name.lower():
                current_val = wp.get("use_api", False)
                wp["use_api"] = not current_val
                wp["product_id"] = 1
                changed = True
                break
        if changed:
            save_web_products(web_products)
            await query.answer("✅ API Connection Toggled!")
            wp = next((p for p in web_products if p.get("name", "").lower() == prod_name.lower()), None)
            display_name = wp.get("display_name") or wp.get("name", "").upper().replace("_", " ")
            use_api = wp.get("use_api", False)
            section = wp.get("section", "Both")
            status_text = "CONNECTED ✅ (Generates key from Alwaysdata API)" if use_api else "DISABLED ❌ (Uses local stock keys)"
            keyboard = [
                [InlineKeyboardButton("🔌 Toggle API Connection", callback_data=f"admin_prod_tglapi_{prod_name}")],
                [InlineKeyboardButton("🗑️ Remove / Delete Product", callback_data=f"admin_rmsel_{prod_name}")],
                [InlineKeyboardButton("« Back to List", callback_data="admin_manage_list")]
            ]
            await query.edit_message_text(
                f"⚙️ <b>PRODUCT SETTINGS: {display_name}</b>\n━━━━━━━━━━━━━━━━━━\n"
                f"📦 <b>Name:</b> {wp.get('name', '')}\n"
                f"📁 <b>Section:</b> {section}\n"
                f"🔌 <b>Alwaysdata API:</b> {status_text}\n"
                f"💡 <i>(Note: Alwaysdata API uses product_id = 1 for all queries)</i>\n"
                "━━━━━━━━━━━━━━━━━━",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="HTML"
            )
        else:
            await query.answer("❌ Product not found.", show_alert=True)
    elif data == "admin_add_product_start":
        if update.effective_user.id not in settings["admin_ids"]: return
        context.user_data["state"] = "awaiting_new_product_name"
        keyboard = [[InlineKeyboardButton("« Back", callback_data="admin_prod_mgmt")]]
        await query.edit_message_text("✏️ <b>Enter the name of the new product:</b>\n(e.g., kiwmodz exe)", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    elif data.startswith("admin_add_product_sec_"):
        if update.effective_user.id not in settings["admin_ids"]: return
        section_type = data.split("_")[4]
        prod_name = context.user_data.get("new_product_name")
        if not prod_name:
            await query.answer("❌ Session expired. Please try again.", show_alert=True)
            return
        sec_map = {
            "trial": "Trial Only",
            "selling": "Selling Only",
            "both": "Both"
        }
        section_val = sec_map.get(section_type, "Both")
        web_products = load_web_products()
        new_prod = {
            "name": prod_name,
            "display_name": prod_name.upper(),
            "prices": {"1d": 50, "7d": 200, "15d": 400, "30d": 600},
            "status": "Active",
            "section": section_val
        }
        web_products.append(new_prod)
        save_web_products(web_products)
        
        keys = load_keys()
        for dur in ["1d", "7d", "15d", "30d", "trial"]:
            dict_key = f"{prod_name}_{dur}"
            if dict_key not in keys:
                keys[dict_key] = []
        save_keys(keys)
        
        keyboard = [[InlineKeyboardButton("« Back to Product Management", callback_data="admin_prod_mgmt")]]
        await query.edit_message_text(
            f"✅ <b>PRODUCT ADDED SUCCESSFULLY!</b>\n━━━━━━━━━━━━━━━━━━\n"
            f"📦 <b>Name:</b> {prod_name.upper()}\n"
            f"🔑 <b>Short Name (Key) for Resellers:</b> <code>{prod_name.lower()}</code>\n"
            f"📁 <b>Section:</b> {section_val}\n"
            f"💰 <b>Default Prices:</b> 1d: 50, 7d: 200, 15d: 400, 30d: 600\n"
            f"📈 <b>Stock Initialized:</b> empty keys added to database\n\n"
            f"💡 <i>Give this short name to resellers. They can generate keys using:</i>\n"
            f"<code>/gen {prod_name.lower()} [1d/7d/15d/30d]</code>\n"
            "━━━━━━━━━━━━━━━━━━",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
    elif data == "admin_remove_product_start":
        if update.effective_user.id not in settings["admin_ids"]: return
        web_products = load_web_products()
        if not web_products:
            keyboard = [[InlineKeyboardButton("« Back", callback_data="admin_prod_mgmt")]]
            await query.edit_message_text("❌ No active products found to remove.", reply_markup=InlineKeyboardMarkup(keyboard))
            return
        buttons = []
        for wp in web_products:
            name = wp.get("display_name") or wp.get("name", "").upper()
            cb = f"admin_rmsel_{wp.get('name', '').lower()}"
            buttons.append(InlineKeyboardButton(name, callback_data=cb))
        keyboard = []
        for i in range(0, len(buttons), 2):
            keyboard.append(buttons[i:i+2])
        keyboard.append([InlineKeyboardButton("« Back", callback_data="admin_prod_mgmt")])
        await query.edit_message_text("🗑️ <b>Select a product to remove:</b>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    elif data.startswith("admin_rmsel_"):
        if update.effective_user.id not in settings["admin_ids"]: return
        prod_name = "_".join(data.split("_")[2:])
        keyboard = [
            [InlineKeyboardButton("Remove from Trial Only", callback_data=f"admin_rmact_{prod_name}_trial")],
            [InlineKeyboardButton("Remove from Selling Only", callback_data=f"admin_rmact_{prod_name}_selling")],
            [InlineKeyboardButton("Remove Completely (With Stock)", callback_data=f"admin_rmact_{prod_name}_both")],
            [InlineKeyboardButton("« Back", callback_data="admin_remove_product_start")]
        ]
        await query.edit_message_text(
            f"❓ <b>How do you want to remove {prod_name.upper()}?</b>\n\n"
            "• <b>Trial Only:</b> Remove from Trial menu but keep in Selling menu.\n"
            "• <b>Selling Only:</b> Remove from Shop/Selling menu but keep in Trial menu.\n"
            "• <b>Remove Completely:</b> Fully delete the product and clear all stock keys from database.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
    elif data.startswith("admin_rmact_"):
        if update.effective_user.id not in settings["admin_ids"]: return
        parts = data.split("_")
        prod_name = "_".join(parts[2:-1])
        action = parts[-1]
        web_products = load_web_products()
        updated_products = []
        removed_completely = False
        section_changed_to = None
        for wp in web_products:
            if wp.get("name", "").lower() == prod_name.lower():
                current_sec = wp.get("section", "Both")
                if action == "trial":
                    if current_sec == "Both":
                        wp["section"] = "Selling Only"
                        section_changed_to = "Selling Only"
                        updated_products.append(wp)
                    elif current_sec == "Trial Only":
                        removed_completely = True
                    else:
                        updated_products.append(wp)
                elif action == "selling":
                    if current_sec == "Both":
                        wp["section"] = "Trial Only"
                        section_changed_to = "Trial Only"
                        updated_products.append(wp)
                    elif current_sec == "Selling Only":
                        removed_completely = True
                    else:
                        updated_products.append(wp)
                elif action == "both":
                    removed_completely = True
            else:
                updated_products.append(wp)
        save_web_products(updated_products)
        if removed_completely:
            keys = load_keys()
            to_delete = [k for k in keys if k.startswith(f"{prod_name}_") or k == prod_name]
            for k in to_delete:
                keys.pop(k, None)
            save_keys(keys)
            msg_text = f"✅ <b>{prod_name.upper()}</b> has been completely removed along with all its stock keys."
        else:
            if section_changed_to:
                msg_text = f"✅ <b>{prod_name.upper()}</b> section has been updated to <b>{section_changed_to}</b>."
            else:
                msg_text = f"✅ No changes were needed for <b>{prod_name.upper()}</b>."
        keyboard = [[InlineKeyboardButton("« Back to Product Management", callback_data="admin_prod_mgmt")]]
        await query.edit_message_text(msg_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    elif data == "admin_help_commands":
        if update.effective_user.id not in settings["admin_ids"]: return
        kb = [[InlineKeyboardButton("« Back", callback_data="admin_panel_cb")]]
        help_text = (
            "❓ <b>ADMIN SLASH COMMANDS</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "💬 <code>/set_welcome [text]</code> - Update welcome message\n"
            "👤 <code>/add_admin [telegram_id]</code> - Add new admin\n"
            "💰 <code>/add_balance [user_id] [amount]</code> - Add balance\n"
            "💸 <code>/remove_balance [user_id] [amount]</code> - Deduct balance\n"
            "💳 <code>/check_balance [user_id]</code> - Check user balance\n"
            "👤 <code>/check_user [user_id_or_username]</code> - View user info profile\n"
            "➕ <code>/add_reseller [user_id] [days]</code> - Add VIP reseller\n"
            "➖ <code>/remove_reseller [user_id]</code> - Remove reseller\n"
            "👑 <code>/resellers</code> - List active resellers\n"
            "📜 <code>/rlogs [user_id]</code> - Check reseller activity logs\n"
            "🔑 <code>/rperms [reseller_id] [products]</code> - Set reseller permissions\n"
            "📢 <code>/bc [message]</code> - Broadcast to all users\n"
            "📊 <code>/stats</code> - Show bot statistics\n"
            "🚫 <code>/ban [user_id]</code> - Ban user from bot\n"
            "✅ <code>/unban [user_id]</code> - Unban user from bot\n"
            "🔑 <code>/gen [product] [duration]</code> - Reseller key generator\n"
            "🔑 <code>/add_key [product] [duration] [key]</code> - Add single key\n"
            "📦 <code>/stock</code> - Check stock levels\n"
            "📜 <code>/check_history [user_id]</code> - Check key generation logs\n"
            "⏳ <code>/set_trial_days [days] [optional: product]</code> - Set trial key duration\n"
            "🔄 <code>/reset_trial [user_id]</code> - Reset trial cooldown for user\n"
            "🔒 <code>/lock_trial [optional: product] [optional: msg]</code> - Lock trials\n"
            "🔓 <code>/unlock_trial [optional: product]</code> - Unlock trials\n"
            "📢 <code>/add_channel [ch_id] [link]</code> - Add force join channel\n"
            "🔄 <code>/reset_channels</code> - Reset all force join channels\n"
            "🔒 <code>/lock_wallet [optional: product/duration]</code> - Lock wallet buy for normal users\n"
            "🔓 <code>/unlock_wallet [optional: product/duration]</code> - Unlock wallet buy for normal users"
        )
        await query.edit_message_text(help_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
    elif data == "admin_guide_add":
        kb = [[InlineKeyboardButton("« Back", callback_data="admin_panel_cb")]]; await query.edit_message_text("To add a VIP reseller, type:\n<code>/add_reseller [user_id] [days]</code>", reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
    elif data == "admin_guide_remove":
        kb = [[InlineKeyboardButton("« Back", callback_data="admin_panel_cb")]]; await query.edit_message_text("To remove a VIP reseller, type:\n<code>/remove_reseller [user_id]</code>", reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
    elif data == "admin_guide_bal":
        kb = [[InlineKeyboardButton("« Back", callback_data="admin_panel_cb")]]; await query.edit_message_text("To add wallet balance, type:\n<code>/add_balance [user_id] [amount]</code>", reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
    elif data == "admin_reset_trial":
        kb = [
            [InlineKeyboardButton("Reset ALL Users", callback_data="admin_reset_trial_all")],
            [InlineKeyboardButton("« Back", callback_data="admin_panel_cb")]
        ]
        await query.edit_message_text(
            "🔄 <b>Reset Trial Cooldowns</b>\n\n"
            "To reset the cooldown for a <b>SPECIFIC USER</b>, type this command:\n"
            "<code>/reset_trial [user_id]</code>\n\n"
            "To reset the cooldown for <b>ALL USERS</b> at once, click the button below.",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="HTML"
        )
    elif data == "admin_reset_trial_all":
        save_trials({}) # Empty the trial dictionary
        kb = [[InlineKeyboardButton("« Back", callback_data="admin_panel_cb")]]
        await query.edit_message_text("✅ All trial cooldowns have been reset! Every user can now claim another trial key.", reply_markup=InlineKeyboardMarkup(kb))
    elif data == "admin_trial_logs":
        hist = load_trial_history()
        if not hist:
            kb = [[InlineKeyboardButton("« Back", callback_data="admin_panel_cb")]]
            await query.edit_message_text("❌ No trial logs found.", reply_markup=InlineKeyboardMarkup(kb))
            return
            
        text = "📜 <b>RECENT TRIAL KEYS (Last 15)</b>\n━━━━━━━━━━━━━━━━━━\n"
        for log in hist[-15:]:
            import datetime
            date_str = datetime.datetime.fromtimestamp(log["time"]).strftime('%Y-%m-%d %H:%M')
            uname = log.get('username', 'None')
            display_name = f"@{uname}" if uname != "None" and update.effective_user.username else uname if uname != "None" else "User"
            if uname == "None": display_name = "User"
            elif " " in str(uname) or not str(uname).isascii(): display_name = uname # Likely a first name
            else: display_name = f"@{uname}"
            
            text += f"• <b>{display_name}</b> (<code>{log['user_id']}</code>)\n  └ {log['product'].upper()} - <code>{log['key']}</code>\n"
        
        kb = [[InlineKeyboardButton("« Back", callback_data="admin_panel_cb")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
    elif data == "admin_stock":
        keys = load_keys()
        web_products = load_web_products()
        active_names = {wp.get("name", "").lower() for wp in web_products}
        text = "📦 <b>CURRENT STOCK</b>\n━━━━━━━━━━━━━━━━━━\n"
        for k, v in keys.items():
            parts = k.split("_")
            prod_prefix = parts[0].lower()
            if prod_prefix in active_names and len(v) > 0:
                text += f"• {k.upper()}: {len(v)} keys\n"
        kb = [[InlineKeyboardButton("« Back", callback_data="admin_panel_cb")]]; await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
    elif data == "admin_listresellers":
        resellers = load_resellers()
        if not resellers:
            kb = [[InlineKeyboardButton("« Back", callback_data="admin_panel_cb")]]; await query.edit_message_text("No active resellers found.", reply_markup=InlineKeyboardMarkup(kb))
            return
        text = "👑 <b>ACTIVE RESELLERS</b>\n━━━━━━━━━━━━━━━━━━\n"
        for r_id, exp in resellers.items():
            if time.time() < exp:
                days_left = (exp - time.time()) / 86400
                text += f"👤 <code>{r_id}</code> - Expires in {days_left:.1f} days\n"
            else:
                text += f"👤 <code>{r_id}</code> - ❌ EXPIRED\n"
        kb = [[InlineKeyboardButton("« Back", callback_data="admin_panel_cb")]]; await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
    elif data == "admin_logsmode":
        resellers = load_resellers()
        if not resellers:
            kb = [[InlineKeyboardButton("« Back", callback_data="admin_panel_cb")]]; await query.edit_message_text("No active resellers found.", reply_markup=InlineKeyboardMarkup(kb))
            return
        keyboard = []
        for r_id in resellers:
            keyboard.append([InlineKeyboardButton(f"Logs for {r_id}", callback_data=f"admin_seelog_{r_id}")])
        keyboard.append([InlineKeyboardButton("« Back", callback_data="admin_panel_cb")]); await query.edit_message_text("Select a reseller to view their activity:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data.startswith("admin_seelog_"):
        target_id = data.split("_")[2]
        logs = load_reseller_logs()
        user_logs = [log for log in logs if f"({target_id})" in log][-20:]
        if not user_logs:
            kb = [[InlineKeyboardButton("« Back", callback_data="admin_logsmode")]]; await query.edit_message_text("❌ No activity found for this reseller.", reply_markup=InlineKeyboardMarkup(kb))
            return
        text = f"📋 <b>RESELLER LOGS: {target_id}</b>\n━━━━━━━━━━━━━━━━━━\n"
        for log in user_logs:
            text += f"• {log}\n"
        text += f"\n<i>Total keys generated: {len(user_logs)}</i>"
        kb = [[InlineKeyboardButton("« Back", callback_data="admin_panel_cb")]]; await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
    elif data == "check_joined":
        if not await check_force_sub(query.from_user.id, context):
            await query.answer("❌ You haven't joined the channel yet! Please join and click again.", show_alert=True)
            return
            
        await query.answer("✅ Verified! Welcome.", show_alert=False)
        settings = load_settings()
        reply_markup = None
        if query.from_user.id in settings["admin_ids"]:
            reply_markup = ReplyKeyboardMarkup([[KeyboardButton("👑 Admin Panel")]], resize_keyboard=True)
            
        await query.message.delete()
        
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=settings["welcome_text"].format(name=query.from_user.first_name),
            reply_markup=get_main_menu_keyboard(),
            parse_mode="HTML"
        )
        if reply_markup:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="Admin recognized.",
                reply_markup=reply_markup
            )
    else:
        await query.edit_message_text(f"Button: {data}")

async def add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]:
        return
        
    if len(context.args) < 2:
        await update.message.reply_text("<b>Usage:</b> <code>/add_channel @username https://link</code>\nOr with ID: <code>/add_channel -1001234567 https://link</code>", parse_mode="HTML")
        return
        
    ch_id = context.args[0]
    link = context.args[1]
    
    if "force_channels" not in settings:
        settings["force_channels"] = []
        
    settings["force_channels"].append({"id": ch_id, "link": link})
    save_settings(settings)
    await update.message.reply_text(f"✅ <b>Added Force Join Channel:</b>\nID: {ch_id}\nLink: {link}", parse_mode="HTML")

async def reset_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]:
        return
        
    settings["force_channels"] = []
    settings["force_channel"] = ""
    settings["invite_link"] = ""
    save_settings(settings)
    await update.message.reply_text("✅ <b>All Force Join channels have been removed!</b>", parse_mode="HTML")

async def reset_trial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]: return

    if not context.args:
        await update.message.reply_text("Usage: /reset_trial [user_id]")
        return
    
    target_id = str(context.args[0]).strip()
    trials = load_trials()
    if target_id in trials:
        trials[target_id]["last_trial"] = 0
        if "history" in trials[target_id]:
            trials[target_id]["history"] = {}
    else:
        trials[target_id] = {"last_trial": 0, "strikes": 0, "banned": False, "history": {}}
        
    save_trials(trials)
    
    try:
        await context.bot.send_message(chat_id=target_id, text="🎉 <b>GOOD NEWS!</b>\n━━━━━━━━━━━━━━\nYour Trial Key cooldown has been reset by the Admin!\n\nYou can now claim another Trial Key immediately.", parse_mode="HTML")
        await update.message.reply_text(f"✅ Trial cooldown reset for user {target_id}!\n📩 Notification successfully sent to the user.")
    except:
        await update.message.reply_text(f"✅ Trial cooldown reset for user {target_id}!\n⚠️ Could not send notification (user might have blocked the bot).")

async def lock_trial_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = load_settings()
    if update.effective_user.id not in settings["admin_ids"]: return
    
    known_products = ["hxn", "lk", "hex", "alpha", "boyyah", "ngo", "greed", "streamerx", "brmods"]
    
    if not context.args:
        settings["trial_locked"] = True
        settings["trial_locked_msg"] = (
            "🚫 <b>TRIAL SECTION LOCKED</b> 🚫\n\n"
            "<b>NO FEEDBACK AND SUPPORT KEY</b>\n"
            "<b>STOP ASK OWNER :-</b>@JFHAXX01\n"
            "<b>OR DEVLOPER :-</b>@rajput_harshil"
        )
        save_settings(settings)
        await update.message.reply_text("🔒 All Trial Keys Locked!\nUsage: /lock_trial [optional: product] [optional: custom message]\nValid products: " + ", ".join(known_products))
        return
        
    first_arg = context.args[0].lower()
    if first_arg in known_products:
        if "locked_products" not in settings or not isinstance(settings["locked_products"], dict):
            settings["locked_products"] = {}
            
        custom_msg = " ".join(context.args[1:]) if len(context.args) > 1 else None
        if not custom_msg:
            custom_msg = (
                f"🚫 <b>{first_arg.upper()} TRIAL LOCKED</b> 🚫\n\n"
                "<b>NO FEEDBACK AND SUPPORT KEY</b>\n"
                "<b>STOP ASK OWNER :-</b>@JFHAXX01\n"
                "<b>OR DEVLOPER :-</b>@rajput_harshil"
            )
            
        settings["locked_products"][first_arg] = custom_msg
        save_settings(settings)
        await update.message.reply_text(f"🔒 Trial Keys for '{first_arg.upper()}' Locked!")
    else:
        settings["trial_locked"] = True
        settings["trial_locked_msg"] = " ".join(context.args)
        save_settings(settings)
        await update.message.reply_text("🔒 All Trial Keys Locked with custom message!")

async def unlock_trial_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = load_settings()
    if update.effective_user.id not in settings["admin_ids"]: return
    
    if not context.args:
        settings["trial_locked"] = False
        settings["locked_products"] = {}
        save_settings(settings)
        await update.message.reply_text("🔓 All Trial Keys Unlocked!")
    else:
        first_arg = context.args[0].lower()
        if "locked_products" in settings and first_arg in settings["locked_products"]:
            del settings["locked_products"][first_arg]
            save_settings(settings)
            await update.message.reply_text(f"🔓 Trial Keys for '{first_arg.upper()}' Unlocked!")
        else:
            settings["trial_locked"] = False
            save_settings(settings)
            await update.message.reply_text(f"🔓 Global Trial lock removed! (If a specific mod was locked, use /unlock_trial [product])")

async def rperms_cmd(update, context):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]: return
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /rperms [reseller_id] [product1,product2 OR clear]\nExample: /rperms 123456789 hxn,hex,prime")
        return
    target_id = context.args[0]
    perms_str = context.args[1]
    perms = load_reseller_perms()
    if perms_str.lower() == "clear":
        perms[target_id] = []
    else:
        perms[target_id] = [p.strip() for p in perms_str.split(",")]
    save_reseller_perms(perms)
    await update.message.reply_text(f"✅ Permissions updated for reseller {target_id}.\nAllowed: {perms[target_id]}")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id in settings["admin_ids"]:
        help_text = (
            "❓ <b>ADMIN SLASH COMMANDS</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "💬 <code>/set_welcome [text]</code> - Update welcome message\n"
            "👤 <code>/add_admin [telegram_id]</code> - Add new admin\n"
            "💰 <code>/add_balance [user_id] [amount]</code> - Add balance\n"
            "💸 <code>/remove_balance [user_id] [amount]</code> - Deduct balance\n"
            "💳 <code>/check_balance [user_id]</code> - Check user balance\n"
            "👤 <code>/check_user [user_id_or_username]</code> - View user info profile\n"
            "➕ <code>/add_reseller [user_id] [days]</code> - Add VIP reseller\n"
            "➖ <code>/remove_reseller [user_id]</code> - Remove reseller\n"
            "👑 <code>/resellers</code> - List active resellers\n"
            "📜 <code>/rlogs [user_id]</code> - Check reseller activity logs\n"
            "🔑 <code>/rperms [reseller_id] [products]</code> - Set reseller permissions\n"
            "📢 <code>/bc [message]</code> - Broadcast to all users\n"
            "📊 <code>/stats</code> - Show bot statistics\n"
            "🚫 <code>/ban [user_id]</code> - Ban user from bot\n"
            "✅ <code>/unban [user_id]</code> - Unban user from bot\n"
            "🔑 <code>/gen [product] [duration]</code> - Reseller key generator\n"
            "🔑 <code>/add_key [product] [duration] [key]</code> - Add single key\n"
            "📦 <code>/stock</code> - Check stock levels\n"
            "📜 <code>/check_history [user_id]</code> - Check key generation logs\n"
            "⏳ <code>/set_trial_days [days] [optional: product]</code> - Set trial key duration\n"
            "🔄 <code>/reset_trial [user_id]</code> - Reset trial cooldown for user\n"
            "🔒 <code>/lock_trial [optional: product] [optional: msg]</code> - Lock trials\n"
            "🔓 <code>/unlock_trial [optional: product]</code> - Unlock trials\n"
            "📢 <code>/add_channel [ch_id] [link]</code> - Add force join channel\n"
            "🔄 <code>/reset_channels</code> - Reset all force join channels\n"
            "🔒 <code>/lock_wallet [optional: product/duration]</code> - Lock wallet buy for normal users\n"
            "🔓 <code>/unlock_wallet [optional: product/duration]</code> - Unlock wallet buy for normal users"
        )
        await update.message.reply_text(help_text, parse_mode="HTML")
    else:
        help_text = (
            "ℹ️ <b>STORE HELPLINE</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Use the menu buttons below to navigate the shop.\n\n"
            "👤 <b>Support:</b> @JFHAXX01\n"
            "📢 <b>Join Channel:</b> https://t.me/JFFREEAPK"
        )
        await update.message.reply_text(help_text, parse_mode="HTML")

def ensure_default_products():
    try:
        doc = jf_col.find_one({"_id": "web_products"})
        if doc is not None: # If document exists (even if empty list), do not overwrite/restore
            return
        products = []
        display_map = {
            "hxn": "HXN CHEAT",
            "lk": "LK TEAM",
            "hex": "HEX BLADE",
            "alpha": "ALPHA-X-STORE",
            "prime": "PRIME X CHEAT",
            "harshil": "HARSHIL MODS",
            "trinity": "TRINITY X ROOT",
            "fluorite": "FLUORITE ANDROID",
            "svj": "SVJ CHEATS",
            "brmods": "BR MODS",
            "beyond": "BEYOND CHEATS",
            "rogerio": "ROGERIO MODS",
            "hwak": "HAWK CHEATS",
            "rapid": "RAPID CORE",
            "daemon": "DAEMON PHONK",
            "hxnstreamer": "HXN STREAMER (.SH)",
            "bs": "BS SECURE LOADER",
            "hydra": "HYDRA ENGINE 8BP",
            "xtffh4x_streamer": "XTFFH4X STREAMER",
            "streamerx": "STREAMER X",
            "boyyah": "BOOYAH PANEL",
            "eliteteam": "ELITE TEAM",
            "ngo": "NGO TRAN",
            "greed": "GREED PANEL",
            "lkpro": "LK TEAM PRO",
            "kiwmodz": "KIWMODZ EXE",
            "xyz": "XYZ SUPREME"
        }
        changed = False
        for wp in products:
            pname = wp.get("name", "").lower()
            if pname in display_map and not wp.get("display_name"):
                wp["display_name"] = display_map[pname]
                changed = True
        existing_names = {wp.get("name", "").lower() for wp in products}
        for name_id, display_name in display_map.items():
            if name_id not in existing_names:
                products.append({
                    "name": name_id,
                    "display_name": display_name,
                    "prices": {"1d": 50, "7d": 200, "15d": 400, "30d": 600},
                    "status": "Active",
                    "section": "Both"
                })
                changed = True
        if changed:
            save_web_products(products)
            print("Successfully populated missing default products into database.")
    except Exception as e:
        print(f"Error populating default products: {e}")

async def run_bot():
    # Re-ban all users who have 3+ strikes but are not currently banned
    try:
        trials = load_trials()
        rebanned = 0
        for uid, data in trials.items():
            if data.get("strikes", 0) >= 3 and not data.get("banned", False):
                data["banned"] = True
                rebanned += 1
        if rebanned > 0:
            save_trials(trials)
            print(f"Startup reban: {rebanned} users re-banned (had 3+ strikes but were not banned)")
        banned_total = sum(1 for v in trials.values() if v.get("banned", False))
        print(f"Total banned users: {banned_total}")
    except Exception as e:
        print(f"Error during startup reban: {e}")
    ensure_default_products()
    try:
        keys_db = load_keys()
        purged = False
        if isinstance(keys_db, dict):
            for k in list(keys_db.keys()):
                if "hotstreamer" in k.lower() or "hot_streamer" in k.lower():
                    del keys_db[k]
                    purged = True
            if purged:
                save_keys(keys_db)
                print("Purged deleted product keys (hot streamer) from DB.")
    except Exception as e:
        print(f"Error purging keys: {e}")

    application = Application.builder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("id", get_my_id))
    application.add_handler(CommandHandler("help", help_cmd))
    application.add_handler(CommandHandler("admin", admin_panel))
    application.add_handler(CommandHandler("set_welcome", set_welcome))
    application.add_handler(CommandHandler("add_admin", add_admin))
    application.add_handler(CommandHandler("bc", broadcast))
    application.add_handler(CommandHandler("stats", stats_cmd))
    application.add_handler(CommandHandler("lock_refer", lock_refer_cmd))
    application.add_handler(CommandHandler("unlock_refer", unlock_refer_cmd))
    application.add_handler(CommandHandler("add_balance", add_balance_cmd))
    application.add_handler(CommandHandler("ban", ban_cmd))
    application.add_handler(CommandHandler("unban", unban_cmd))
    application.add_handler(CommandHandler("check_history", check_history_cmd))
    application.add_handler(CommandHandler("check_balance", check_balance_cmd))
    application.add_handler(CommandHandler("check_user", check_user_cmd))
    application.add_handler(CommandHandler("set_trial_days", set_trial_days_cmd))
    application.add_handler(CommandHandler("remove_balance", remove_balance_cmd))
    application.add_handler(CommandHandler("add_reseller", add_reseller_cmd))
    application.add_handler(CommandHandler("remove_reseller", remove_reseller_cmd))
    application.add_handler(CommandHandler("resellers", list_resellers_cmd))
    application.add_handler(CommandHandler("rlogs", rlogs_cmd))
    application.add_handler(CommandHandler("rperms", rperms_cmd))
    application.add_handler(CommandHandler("gen", gen_key_cmd))
    application.add_handler(CommandHandler("add_key", add_key))
    application.add_handler(CommandHandler("stock", check_stock))
    application.add_handler(CommandHandler("add_channel", add_channel))
    application.add_handler(CommandHandler("reset_channels", reset_channels))
    application.add_handler(CommandHandler("reset_trial", reset_trial))
    application.add_handler(CommandHandler("lock_trial", lock_trial_cmd))
    application.add_handler(CommandHandler("unlock_trial", unlock_trial_cmd))
    application.add_handler(CommandHandler("lock_wallet", lock_wallet_cmd))
    application.add_handler(CommandHandler("unlock_wallet", unlock_wallet_cmd))
    
    application.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    application.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.FORWARDED, message_handler))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(ChatMemberHandler(chat_member_update, ChatMemberHandler.CHAT_MEMBER))
    
    async def join_request_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            await update.chat_join_request.approve()
        except:
            pass
            
    application.add_handler(ChatJoinRequestHandler(join_request_handler))
    
    async with application:
        await application.initialize()
        await application.start()
        await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        print("Bot is running with Admin Controls...")
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("Stopped.")

import logging
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



def load_settings():
    doc = jf_col.find_one({"_id": "settings"})
    return doc["data"] if doc else {"admin_ids": [12345678]}

def save_settings(settings):
    jf_col.update_one({"_id": "settings"}, {"$set": {"data": settings}}, upsert=True)

def load_trials():
    doc = jf_col.find_one({"_id": "trials"})
    return doc["data"] if doc else {}

def save_trials(data):
    jf_col.update_one({"_id": "trials"}, {"$set": {"data": data}}, upsert=True)

def load_users():
    doc = jf_col.find_one({"_id": "users"})
    return doc["data"] if doc else []

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        jf_col.update_one({"_id": "users"}, {"$set": {"data": users}}, upsert=True)

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

def load_keys():
    doc = jf_col.find_one({"_id": "keys"})
    return doc["data"] if doc else {}

def save_keys(keys):
    jf_col.update_one({"_id": "keys"}, {"$set": {"data": keys}}, upsert=True)

def load_utr_log():
    doc = jf_col.find_one({"_id": "utr_log"})
    return doc["data"] if doc else []

def save_utr(utr):
    log = load_utr_log()
    if utr not in log:
        log.append(utr)
        jf_col.update_one({"_id": "utr_log"}, {"$set": {"data": log}}, upsert=True)

def load_balances():
    doc = jf_col.find_one({"_id": "balances"})
    return doc["data"] if doc else {}

def save_balances(balances):
    jf_col.update_one({"_id": "balances"}, {"$set": {"data": balances}}, upsert=True)

def load_resellers():
    doc = jf_col.find_one({"_id": "resellers"})
    return doc["data"] if doc else {}

def save_resellers(resellers):
    jf_col.update_one({"_id": "resellers"}, {"$set": {"data": resellers}}, upsert=True)

def load_reseller_logs():
    doc = jf_col.find_one({"_id": "reseller_logs"})
    return doc["data"] if doc else []

def save_reseller_logs(user_id, product, key):
    logs = load_reseller_logs()
    from datetime import datetime
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logs.append(f"{time_str} - User {user_id} generated {product} key: {key}")
    if len(logs) > 50: logs = logs[-50:]
    jf_col.update_one({"_id": "reseller_logs"}, {"$set": {"data": logs}}, upsert=True)

def log_reseller_action(user_id, product, duration_label):
    save_reseller_logs(user_id, product, "N/A")

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
        trials[user_id]["strikes"] += 1
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

async def generate_key_from_api(product, duration_label):
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
    
    # Map products to IDs (You can add more later)
    product_map = {
        "hxn": 1,
        "prime": 1,
        "harshil": 1,
        "streamerxsh": 1
    }
    product_id = product_map.get(product.lower(), 1)
    
    params = {
        "secret": api_secret,
        "product_id": product_id,
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
    save_user(user_id)
    
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
        order_id = context.user_data.get("order_id", "Unknown")
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
                InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
            ]
        ])
        
        for admin_id in settings["admin_ids"]:
            try:
                if update.message.photo:
                    await context.bot.send_photo(chat_id=admin_id, photo=update.message.photo[-1].file_id, caption=admin_msg, reply_markup=keyboard, parse_mode="HTML")
                else:
                    await context.bot.send_message(chat_id=admin_id, text=admin_msg, reply_markup=keyboard, parse_mode="HTML")
            except Exception as e:
                logger.error(f"Could not notify admin {admin_id}: {e}")
        
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
                    [InlineKeyboardButton("🔄 Reset Trial Cooldown", callback_data="admin_reset_trial")]
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

def get_shop_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("HXN CHEAT", callback_data="product_hxn"),
            InlineKeyboardButton("LK TEAM", callback_data="product_lk")
        ],
        [
            InlineKeyboardButton("HEX BLADE", callback_data="product_hex"),
            InlineKeyboardButton("ALPHA-X STORE", callback_data="product_alpha")
        ],
        [
            InlineKeyboardButton("PRIME X CHEAT", callback_data="product_prime"),
            InlineKeyboardButton("HARSHIL MODS", callback_data="product_harshil")
        ],
        [
            InlineKeyboardButton("BOOYAH MOD", callback_data="product_boyyah"),
            InlineKeyboardButton("STREAMER X", callback_data="product_streamerx")
        ],
        [
            InlineKeyboardButton("STREAMER-X PRO", callback_data="product_streamerpro"),
            InlineKeyboardButton("NGO TRAN", callback_data="product_ngo")
        ],
        [
            InlineKeyboardButton("GREED CHEAT", callback_data="product_greed"),
            InlineKeyboardButton("TRINITY X ROOT", callback_data="product_trinity")
        ],
        [
            InlineKeyboardButton("FLUORITE ANDROID", callback_data="product_fluorite"),
            InlineKeyboardButton("ELITE TEAM", callback_data="product_eliteteam")
        ],
        [
            InlineKeyboardButton("BR MODS", callback_data="product_brmods"),
            InlineKeyboardButton("SVJ CHEATS", callback_data="product_svj")
        ],
        [
            InlineKeyboardButton("VIPER TEAM", callback_data="product_viper"),
            InlineKeyboardButton("BEYOND CHEATS", callback_data="product_beyond")
        ],
        [
            InlineKeyboardButton("ROGERIO MODS", callback_data="product_rogerio"),
            InlineKeyboardButton("HAWK CHEATS", callback_data="product_hawk")
        ],
        [
            InlineKeyboardButton("KIWMODZ EXE", callback_data="product_kiwmodz"),
            InlineKeyboardButton("ANGRY MOD", callback_data="product_angry")
        ],
        [
            InlineKeyboardButton("RAPID CORE", callback_data="product_rapid"),
            InlineKeyboardButton("YOONSO BUTTERFLY", callback_data="product_yoonso")
        ],
        [InlineKeyboardButton("PRIME HOOK (.SH)", callback_data="product_primehook")],
        [InlineKeyboardButton("HXN STREAMER (.SH)", callback_data="product_streamerxsh")],
        [InlineKeyboardButton("BS SECURE LOADER", callback_data="product_bssecure")],
        [InlineKeyboardButton("HYDRA ENGINE 8BP", callback_data="product_hydra")],
        [InlineKeyboardButton("OS VICTORY 8BP", callback_data="product_osvictory")],
        [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="main_menu")]
    ]
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
    
    if target_id not in logs or len(logs[target_id]) == 0:
        await update.message.reply_text("❌ No activity found for this reseller.")
        return
        
    user_logs = logs[target_id][-20:] # Get last 20 actions
    
    text = f"📋 <b>RESELLER LOGS: {target_id}</b>\n━━━━━━━━━━━━━━━━━━\n"
    for log in user_logs:
        date_str = datetime.datetime.fromtimestamp(log["time"]).strftime('%Y-%m-%d %H:%M')
        text += f"• {date_str} - Generated {log['product'].upper()} ({log['duration']})\n"
        
    text += f"\n<i>Total keys generated: {len(logs[target_id])}</i>"
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
    
    auto_products = ["hxn", "prime", "harshil", "streamerxsh"]
    delivered_key = None
    
    status_msg = await update.message.reply_text("🔄 Generating key...")
    
    if product in auto_products:
        delivered_key = await generate_key_from_api(product, duration_label)
    else:
        dict_key = f"{product}_{duration_label}"
        keys = load_keys()
        if dict_key in keys and len(keys[dict_key]) > 0:
            delivered_key = keys[dict_key].pop(0)
            save_keys(keys)
            
    if delivered_key:
        log_reseller_action(user_id, product, duration_label)
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
    
    await update.message.reply_text(f"✅ <b>Key added for {product.upper()} ({duration.upper()})!</b>\nCurrent Stock: {len(keys[dict_key])}", parse_mode="HTML")

async def check_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]: return

    keys = load_keys()
    if not keys:
        await update.message.reply_text("📦 <b>Stock is empty!</b>", parse_mode="HTML")
        return

    stock_text = "📦 <b>CURRENT STOCK:</b>\n━━━━━━━━━━━━━━\n"
    for prod_dur, klist in keys.items():
        stock_text += f"┠ <b>{prod_dur.upper()}:</b> {len(klist)} keys\n"
    
    await update.message.reply_text(stock_text, parse_mode="HTML")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message to all users."""
    user_id = update.effective_user.id
    settings = load_settings()
    
    if user_id not in settings["admin_ids"]:
        await update.message.reply_text("❌ You are not authorized to broadcast.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /bc [Your Message]")
        return

    msg_to_send = " ".join(context.args)
    users = load_users()
    
    count = 0
    await update.message.reply_text(f"🚀 <b>Starting Broadcast to {len(users)} users...</b>", parse_mode="HTML")
    
    for uid in users:
        try:
            await context.bot.send_message(chat_id=uid, text=msg_to_send, parse_mode="HTML")
            count += 1
            await asyncio.sleep(0.05) # Small delay to avoid flooding
        except Exception as e:
            logger.error(f"Failed to send to {uid}: {e}")

    await update.message.reply_text(f"✅ <b>Broadcast Completed!</b>\nSuccessfully sent to {count} users.", parse_mode="HTML")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
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
            msg = ("🚫 <b>TRIAL SECTION LOCKED</b> 🚫\n\n"
                   "<b>NO FEEDBACK AND SUPPORT KEY</b>\n"
                   "<b>STOP ASK OWNER :-</b>@JFHAXX01\n"
                   "<b>OR DEVLOPER :-</b>@rajput_harshil")
            kb = [[InlineKeyboardButton("« Back", callback_data="main_menu")]]
            await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
            return
        keyboard = [
            [InlineKeyboardButton("HXN CHEAT", callback_data="claim_trial_hxn"), InlineKeyboardButton("LK TEAM", callback_data="claim_trial_lk")],
            [InlineKeyboardButton("HEX BLADE", callback_data="claim_trial_hex"), InlineKeyboardButton("ALPHA-X-STORE", callback_data="claim_trial_alpha")],
            [InlineKeyboardButton("BOOYAH MOD", callback_data="claim_trial_boyyah"), InlineKeyboardButton("NGO TRAN", callback_data="claim_trial_ngo")],
            [InlineKeyboardButton("GREED CHEAT", callback_data="claim_trial_greed"), InlineKeyboardButton("STREAMER X (.SH)", callback_data="claim_trial_streamerx")],
            [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="main_menu")]
        ]
        await query.edit_message_text("🎁 <b>TRIAL KEYS</b>\n\nSelect a product to get a 1-Day Trial Key.\n⚠️ <i>You can only claim ONE trial key every 24 hours. Leaving the channel to cheat will result in a PERMANENT BAN.</i>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
        return
        
    if data.startswith("claim_trial_"):
        settings = load_settings()
        if settings.get("trial_locked", False):
            msg = ("🚫 <b>TRIAL SECTION LOCKED</b> 🚫\n\n"
                   "<b>NO FEEDBACK AND SUPPORT KEY</b>\n"
                   "<b>STOP ASK OWNER :-</b>@JFHAXX01\n"
                   "<b>OR DEVLOPER :-</b>@rajput_harshil")
            kb = [[InlineKeyboardButton("« Back", callback_data="main_menu")]]
            await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
            return

        product = data.split("_")[2]
        user_id = str(update.effective_user.id)
        
        # Check channel
        if not await check_force_sub(update.effective_user.id, context):
            await query.answer("⚠️ You must join the channel first!", show_alert=True)
            return
            
        trials = load_trials()
        user_trial = trials.get(user_id, {"last_trial": 0, "strikes": 0, "banned": False})
        
        # 2 day check
        cooldown_time = 24 * 60 * 60
        time_since_last = time.time() - user_trial["last_trial"]
        if time_since_last < cooldown_time:
            remaining_seconds = int(cooldown_time - time_since_last)
            h, remainder = divmod(remaining_seconds, 3600)
            m, s = divmod(remainder, 60)
            keyboard = [[InlineKeyboardButton("« Back", callback_data="trial_key")]]
            last_key = user_trial.get("last_key", "None")
            last_prod = user_trial.get("last_product", "Unknown").upper()
            
            msg = f"⏳ <b>TRIAL COOLDOWN</b>\n━━━━━━━━━━━━━━\nPlease wait for {h}h {m}m {s}s.\nYou can claim your next trial key after this time."
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
        keyboard = [
            [InlineKeyboardButton("HXN", callback_data="bulk_prod_hxn"), InlineKeyboardButton("LK", callback_data="bulk_prod_lk")],
            [InlineKeyboardButton("HEX", callback_data="bulk_prod_hex"), InlineKeyboardButton("ALPHA", callback_data="bulk_prod_alpha")],
            [InlineKeyboardButton("PRIME", callback_data="bulk_prod_prime"), InlineKeyboardButton("HARSHIL", callback_data="bulk_prod_harshil")],
            [InlineKeyboardButton("BOOYAH", callback_data="bulk_prod_boyyah"), InlineKeyboardButton("STREAMER X", callback_data="bulk_prod_streamerx")],
            [InlineKeyboardButton("STREAMER-X PRO", callback_data="bulk_prod_streamerpro"), InlineKeyboardButton("NGO TRAN", callback_data="bulk_prod_ngo")],
            [InlineKeyboardButton("GREED", callback_data="bulk_prod_greed"), InlineKeyboardButton("PRIME HOOK (.SH )", callback_data="bulk_prod_primehook")],
            [InlineKeyboardButton("TRINITY X", callback_data="bulk_prod_trinity"), InlineKeyboardButton("FLUORITE", callback_data="bulk_prod_fluorite")],
            [InlineKeyboardButton("ELITE TEAM", callback_data="bulk_prod_eliteteam"), InlineKeyboardButton("BR MODS", callback_data="bulk_prod_brmods")],
            [InlineKeyboardButton("SVJ", callback_data="bulk_prod_svj"), InlineKeyboardButton("VIPER", callback_data="bulk_prod_viper")],
            [InlineKeyboardButton("BEYOND", callback_data="bulk_prod_beyond"), InlineKeyboardButton("ROGERIO", callback_data="bulk_prod_rogerio")],
            [InlineKeyboardButton("HAWK", callback_data="bulk_prod_hwak"), InlineKeyboardButton("HXN STREAMER", callback_data="bulk_prod_streamerxsh")],
            [InlineKeyboardButton("KIWMODZ EXE", callback_data="bulk_prod_kiwmodz"), InlineKeyboardButton("ANGRY MOD", callback_data="bulk_prod_angry")],
            [InlineKeyboardButton("RAPID CORE", callback_data="bulk_prod_rapid"), InlineKeyboardButton("YOONSO", callback_data="bulk_prod_yoonso")],
            [InlineKeyboardButton("BS SECURE LOADER", callback_data="bulk_prod_bssecure")],
            [InlineKeyboardButton("HYDRA ENGINE 8BP", callback_data="bulk_prod_hydra")],
            [InlineKeyboardButton("OS VICTORY 8BP", callback_data="bulk_prod_osvictory")],
            [InlineKeyboardButton("« Back to Admin Panel", callback_data="admin_panel_cb")]
        ]
        context.user_data["state"] = "awaiting_bulk_product"
        await query.edit_message_text("🛒 <b>Select Product to Add Keys:</b>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
        return
        
    if data.startswith("bulk_prod_"):
        if update.effective_user.id not in settings["admin_ids"]: return
        product = data.split("_")[2]
        context.user_data["bulk_product"] = product
        keyboard = [
            [InlineKeyboardButton("1 Day", callback_data="bulk_dur_1d"), InlineKeyboardButton("7 Days", callback_data="bulk_dur_7d")],
            [InlineKeyboardButton("15 Days", callback_data="bulk_dur_15d"), InlineKeyboardButton("30 Days", callback_data="bulk_dur_30d")],
            [InlineKeyboardButton("Trial Keys", callback_data="bulk_dur_trial")],
            [InlineKeyboardButton("🗑️ Clear All Stock", callback_data=f"clear_stock_{product}")],
            [InlineKeyboardButton("⬅️ Back", callback_data="admin_add_keys")]
        ]
        await query.edit_message_text(f"⏳ <b>Select Duration for {product.upper()}:</b>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
        return
        
    if data.startswith("clear_stock_"):
        if update.effective_user.id not in settings["admin_ids"]: return
        product = data.split("_")[2]
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
        keyboard = get_shop_keyboard()
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
        await query.edit_message_text(
            "💰 <b>ADD BALANCE</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "To add funds to your wallet, please select an amount or use the QR scanner in the payment section.\n\n"
            "1. Click 'Shop Store Now'\n"
            "2. Select any product\n"
            "3. Pay the exact amount\n\n"
            "<i>Balance will be added automatically after verification.</i>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🛍️ Go to Shop", callback_data="shop")], [InlineKeyboardButton("« Back", callback_data="main_menu")]]),
            parse_mode="HTML"
        )
    elif data == "history":
        await query.edit_message_text(
            "📋 <b>ORDER HISTORY</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "❌ <b>No orders found!</b>\n\n"
            "Your previous purchases will appear here once they are verified.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Back", callback_data="main_menu")]]),
            parse_mode="HTML"
        )
    elif data == "referral":
        bot_username = (await context.bot.get_me()).username
        referral_link = f"https://t.me/{bot_username}?start={update.effective_user.id}"
        await query.edit_message_text(
            "🎁 <b>REFERRAL SYSTEM</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Invite your friends and earn rewards!\n\n"
            f"🔗 <b>Your Link:</b>\n<code>{referral_link}</code>\n\n"
            "👥 <b>Total Referrals:</b> 0\n"
            "💰 <b>Earnings:</b> ₹0.00",
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
        product_name = data.replace("product_", "").upper().replace("_", " ")
        price_text = (
            f"🛒 <b>{product_name}</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📦 <b>Package Info:</b>\n"
            "┠ <b>1 DAY : ₹70</b> - 81 stock\n"
            "✅ <b>Stock Available</b>\n\n"
            "┠ <b>7 DAY : ₹200</b> - 4 stock\n"
            "✅ <b>Stock Available</b>\n\n"
            "┠ <b>15 DAY : ₹400</b> - 4 stock\n"
            "✅ <b>Stock Available</b>\n\n"
            "┠ <b>30 DAY : ₹600</b> - 4 stock\n"
            "✅ <b>Stock Available</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "<i>Prices are auto-calculated based on your tier.</i>"
        )
        
        keyboard = [
            [InlineKeyboardButton("🛒 1 Day - ₹70", callback_data=f"buy_{data}_1d")],
            [InlineKeyboardButton("🛒 7 Day - ₹200", callback_data=f"buy_{data}_7d")],
            [InlineKeyboardButton("🛒 15 Day - ₹400", callback_data=f"buy_{data}_15d")],
            [InlineKeyboardButton("🛒 30 Day - ₹600", callback_data=f"buy_{data}_30d")],
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
        price_map = {"1d": "70.00", "7d": "200.00", "15d": "400.00", "30d": "600.00"}
        
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
        
        if user_bal >= float_amount:
            title = "👑 <b>VIP RESELLER CHECKOUT (30% OFF)</b>" if is_reseller else "✅ <b>SUFFICIENT BALANCE</b>"
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
        order_id = data.split("_")[1]
        amount = float(context.user_data.get("amount", "0"))
        product = context.user_data.get("product", "hxn")
        duration_label = context.user_data.get("duration", "1d")
        
        user_id_str = str(query.from_user.id)
        balances = load_balances()
        user_bal = balances.get(user_id_str, 0.0)
        
        if user_bal >= amount:
            balances[user_id_str] -= amount
            save_balances(balances)
            
            auto_products = ["hxn", "prime", "harshil", "streamerxsh"]
            delivered_key = None
            
            if product in auto_products:
                delivered_key = await generate_key_from_api(product, duration_label)
            else:
                dict_key = f"{product}_{duration_label}"
                keys = load_keys()
                if dict_key in keys and len(keys[dict_key]) > 0:
                    delivered_key = keys[dict_key].pop(0)
                    save_keys(keys)
            
            if delivered_key:
                success_msg = (
                    "✅ <b>PURCHASE SUCCESSFUL!</b>\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    f"🏺 <b>Product:</b> {product.upper()}\n"
                    f"⏳ <b>Duration:</b> {duration_label.upper()}\n"
                    f"💰 <b>Remaining Balance:</b> ₹{balances[user_id_str]:.2f}\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    f"🔑 <b>YOUR KEY:</b>\n<code>{delivered_key}</code>\n\n"
                    "<i>Thank you for shopping with us!</i>"
                )
                await query.edit_message_text(text=success_msg, parse_mode="HTML")
            else:
                balances[user_id_str] += amount
                save_balances(balances)
                await query.answer(f"❌ ERROR! Out of stock for {product.upper()}. Balance refunded.", show_alert=True)
                await query.edit_message_text("❌ Payment refunded due to out-of-stock. Please contact Admin.")
        else:
            await query.answer("❌ Insufficient balance!", show_alert=True)



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
        
        # 1. GENERATE OR FETCH KEY
        auto_products = ["hxn", "prime", "harshil", "streamerxsh"]
        
        if product in auto_products:
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
            # Send Key to User
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
            try:
                await context.bot.send_message(chat_id=target_user_id, text=success_msg, parse_mode="HTML")
                
                # Update Admin Message
                update_text = (
                    f"✅ <b>APPROVED & KEY SENT</b>\n"
                    f"🔑 <b>Generated:</b> <code>{delivered_key}</code>"
                )
                if query.message.photo:
                    await query.edit_message_caption(caption=query.message.caption + f"\n\n{update_text}", parse_mode="HTML")
                else:
                    await query.edit_message_text(text=query.message.text + f"\n\n{update_text}", parse_mode="HTML")
            except Exception as e:
                await query.answer(f"Error sending key: {e}", show_alert=True)
        else:
            await query.answer(f"❌ ERROR! Could not generate or find a key for {product.upper()}. Out of stock?", show_alert=True)

    elif data.startswith("reject_"):
        target_user_id = int(data.split("_")[1])
        try:
            await context.bot.send_message(chat_id=target_user_id, text="❌ <b>Payment Rejected!</b>\nYour payment could not be verified. Please contact support if you think this is a mistake.", parse_mode="HTML")
            await query.edit_message_caption(caption=query.message.caption + "\n\n❌ <b>REJECTED</b>") if query.message.photo else await query.edit_message_text(text=query.message.text + "\n\n❌ <b>REJECTED</b>")
        except Exception as e:
            await query.answer(f"Error notifying user: {e}", show_alert=True)
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
            [InlineKeyboardButton("🔄 Reset Trial Cooldown", callback_data="admin_reset_trial")]
        ]
        await query.edit_message_text("👑 <b>Admin Dashboard</b>\nSelect an option below:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
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
        text = "📦 <b>CURRENT STOCK</b>\n━━━━━━━━━━━━━━━━━━\n"
        for k, v in keys.items():
            if len(v) > 0:
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
        if target_id not in logs or len(logs[target_id]) == 0:
            kb = [[InlineKeyboardButton("« Back", callback_data="admin_logsmode")]]; await query.edit_message_text("❌ No activity found for this reseller.", reply_markup=InlineKeyboardMarkup(kb))
            return
        user_logs = logs[target_id][-20:]
        text = f"📋 <b>RESELLER LOGS: {target_id}</b>\n━━━━━━━━━━━━━━━━━━\n"
        for log in user_logs:
            date_str = datetime.datetime.fromtimestamp(log["time"]).strftime('%Y-%m-%d %H:%M')
            text += f"• {date_str} - Gen {log['product'].upper()} ({log['duration']})\n"
        text += f"\n<i>Total keys generated: {len(logs[target_id])}</i>"
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
    else:
        trials[target_id] = {"last_trial": 0, "strikes": 0, "banned": False}
        
    save_trials(trials)
    
    try:
        await context.bot.send_message(chat_id=target_id, text="🎉 <b>GOOD NEWS!</b>\n━━━━━━━━━━━━━━\nYour Trial Key cooldown has been reset by the Admin!\n\nYou can now claim another Trial Key immediately.", parse_mode="HTML")
        await update.message.reply_text(f"✅ Trial cooldown reset for user {target_id}!\n📩 Notification successfully sent to the user.")
    except:
        await update.message.reply_text(f"✅ Trial cooldown reset for user {target_id}!\n⚠️ Could not send notification (user might have blocked the bot).")

async def lock_trial_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = load_settings()
    if update.effective_user.id not in settings["admin_ids"]: return
    settings["trial_locked"] = True
    save_settings(settings)
    await update.message.reply_text("🔒 Trial Key Section Locked!")

async def unlock_trial_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = load_settings()
    if update.effective_user.id not in settings["admin_ids"]: return
    settings["trial_locked"] = False
    save_settings(settings)
    await update.message.reply_text("🔓 Trial Key Section Unlocked!")

async def run_bot():
    application = Application.builder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("id", get_my_id))
    application.add_handler(CommandHandler("admin", admin_panel))
    application.add_handler(CommandHandler("set_welcome", set_welcome))
    application.add_handler(CommandHandler("add_admin", add_admin))
    application.add_handler(CommandHandler("bc", broadcast))
    application.add_handler(CommandHandler("add_balance", add_balance_cmd))
    application.add_handler(CommandHandler("add_reseller", add_reseller_cmd))
    application.add_handler(CommandHandler("remove_reseller", remove_reseller_cmd))
    application.add_handler(CommandHandler("resellers", list_resellers_cmd))
    application.add_handler(CommandHandler("rlogs", rlogs_cmd))
    application.add_handler(CommandHandler("gen", gen_key_cmd))
    application.add_handler(CommandHandler("add_key", add_key))
    application.add_handler(CommandHandler("stock", check_stock))
    application.add_handler(CommandHandler("add_channel", add_channel))
    application.add_handler(CommandHandler("reset_channels", reset_channels))
    application.add_handler(CommandHandler("reset_trial", reset_trial))
    application.add_handler(CommandHandler("lock_trial", lock_trial_cmd))
    application.add_handler(CommandHandler("unlock_trial", unlock_trial_cmd))
    
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

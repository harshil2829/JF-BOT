import os
import re

file_path = "/Users/cashify/Desktop/NewClientBot/bot.py"
with open(file_path, "r") as f:
    code = f.read()

# 1. Update Token
code = re.sub(r'BOT_TOKEN = ".*?"', 'BOT_TOKEN = "8821407634:AAENJNHB7JVdc4FamhOmFsgkhX-WS5K7j7k"', code)

# 2. Update Database
code = code.replace("db = client['TelegramBotDB']", "db = client['ClientBotDB']")
code = code.replace("jf_col = db['jf_data']", "jf_col = db['client2_data']")

# 3. Strip Web dependencies
code = re.sub(r'def load_web_products\(\):.*?return.*?\[\] if doc else \[\]', 'def load_web_products():\n    return []', code, flags=re.DOTALL)
code = re.sub(r'def load_web_settings\(\):.*?return.*?\{\} if doc else \{\}', 'def load_web_settings():\n    return {}', code, flags=re.DOTALL)
code = re.sub(r'def load_web_staff\(\):.*?return.*?\[\] if doc else \[\]', 'def load_web_staff():\n    return []', code, flags=re.DOTALL)

# 4. Currency change (₹ to $)
code = code.replace('₹', '$').replace('INR', 'USD')

# 5. Fix "add_balance" text prompt
code = code.replace("Please type the amount you want to add to your wallet in USD ($).", "Please type the amount you want to add to your wallet in USD ($).\n(For bKash, 1 USD = 120 BDT)")

# 6. Update `awaiting_balance_amount` handler inside `message_handler`
old_balance_logic = r'if state == "awaiting_balance_amount":.*?context\.user_data\["state"\] = None'
new_balance_logic = """if state == "awaiting_balance_amount":
        try:
            import string
            import random
            amount = float(update.message.text.strip())
            if amount <= 0:
                await update.message.reply_text("❌ Amount must be greater than 0. Try again:")
                return
            
            amount_usd = amount
            amount_bdt = amount * 120
            order_id = "ORD" + "".join(random.choices(string.digits, k=6))
            context.user_data["balance_amount"] = amount
            context.user_data["order_id"] = order_id
            
            msg = (
                f"💰 <b>ADD BALANCE</b>\\n"
                f"━━━━━━━━━━━━━━━━━━\\n"
                f"💵 <b>Amount:</b> ${amount_usd:.2f} (৳{amount_bdt:.2f})\\n"
                f"🆔 <b>Order ID:</b> <code>{order_id}</code>\\n\\n"
                f"<b>Please select your payment method below:</b>"
            )
            keyboard = [
                [InlineKeyboardButton("🌍 Global (Binance)", callback_data=f"pay_binance_{order_id}")],
                [InlineKeyboardButton("🇧🇩 Bangladesh (bKash)", callback_data=f"pay_bkash_{order_id}")],
                [InlineKeyboardButton("🇮🇳 India (UPI)", callback_data=f"pay_upi_{order_id}")],
                [InlineKeyboardButton("❌ Cancel", callback_data="main_menu")]
            ]
            context.user_data["state"] = None
            await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
            return
        except ValueError:
            await update.message.reply_text("❌ Invalid amount. Please enter a number (e.g. 5):")
            return"""
code = re.sub(old_balance_logic, new_balance_logic, code, count=1, flags=re.DOTALL)

# 7. Add `pay_` handler into `button_handler`
pay_handler = """    elif data.startswith("pay_"):
        parts = data.split("_")
        method = parts[1]
        order_id = parts[2]
        amount_usd = context.user_data.get("balance_amount", 0)
        amount_bdt = amount_usd * 120
        
        if method == "binance":
            pay_details = f"<b>Binance ID:</b> <code>781257349</code>\\n<b>Amount:</b> ${amount_usd:.2f}"
        elif method == "bkash":
            pay_details = f"<b>bKash Personal:</b> <code>01874640097</code>\\n<b>Amount:</b> ৳{amount_bdt:.2f}"
        elif method == "upi":
            pay_details = f"<b>UPI:</b> <i>Coming Soon</i>\\n<b>Amount:</b> ${amount_usd:.2f}"
            
        msg = (
            f"💳 <b>PAYMENT DETAILS ({method.upper()})</b>\\n"
            f"━━━━━━━━━━━━━━━━━━\\n"
            f"{pay_details}\\n\\n"
            f"<i>After paying exactly the amount shown above, please send your Transaction ID or Screenshot here to confirm.</i>"
        )
        context.user_data["state"] = "awaiting_receipt"
        await query.edit_message_text(msg, parse_mode="HTML")
"""
code = code.replace('elif data == "history":', pay_handler + '\n    elif data == "history":')

# 8. Update Products Menu
shop_kb_regex = r'def get_shop_keyboard\(.*?\):.*?return InlineKeyboardMarkup\(keyboard\)'
new_shop_kb = """def get_shop_keyboard(user_id=None):
    keyboard = [
        [InlineKeyboardButton("🛒 ALPHA-X STORE", callback_data="product_alphax")],
        [InlineKeyboardButton("🛒 LK TEAM", callback_data="product_lkteam")],
        [InlineKeyboardButton("🛒 BR MODS", callback_data="product_brmods")],
        [InlineKeyboardButton("🛒 HEX BLADE", callback_data="product_hexblade")],
        [InlineKeyboardButton("« Back", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)"""
code = re.sub(shop_kb_regex, new_shop_kb, code, flags=re.DOTALL)

# 9. Update Product Durations
prod_logic = r'elif data\.startswith\("product_"\):.*?parse_mode="HTML"'
new_prod_logic = """elif data.startswith("product_"):
        product_name = data.replace("product_", "").upper().replace("_", " ")
        price_text = (
            f"🛒 <b>{product_name}</b>\\n"
            "━━━━━━━━━━━━━━━━━━\\n"
            "📦 <b>Select Duration:</b>\\n\\n"
            "<i>Note: 1 USD = 120 BDT</i>"
        )
        keyboard = [
            [InlineKeyboardButton("1 Day", callback_data=f"buy_{data}_1d"), InlineKeyboardButton("3 Days", callback_data=f"buy_{data}_3d")],
            [InlineKeyboardButton("7 Days", callback_data=f"buy_{data}_7d"), InlineKeyboardButton("15 Days", callback_data=f"buy_{data}_15d")],
            [InlineKeyboardButton("30 Days", callback_data=f"buy_{data}_30d")],
            [InlineKeyboardButton("« Back To Store", callback_data="shop")]
        ]
        await query.edit_message_text(price_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")"""
code = re.sub(prod_logic, new_prod_logic, code, flags=re.DOTALL)

# 10. Update Price map
price_map_logic = r'duration_map = \{"1d": "1 Days", "7d": "7 Days", "15d": "15 Days", "30d": "30 Days"\}.*?price_map = \{"1d": "50.00", "7d": "200.00", "15d": "400.00", "30d": "600.00"\}'
new_price_map = """duration_map = {"1d": "1 Days", "3d": "3 Days", "7d": "7 Days", "15d": "15 Days", "30d": "30 Days"}
        price_map = {"1d": "2.00", "3d": "4.00", "7d": "6.00", "15d": "10.00", "30d": "18.00"}"""
code = re.sub(price_map_logic, new_price_map, code, flags=re.DOTALL)

with open(file_path, "w") as f:
    f.write(code)

print("Patched NewClientBot fully.")

import os

with open("JF BOT/bot.py", "r") as f:
    code = f.read()

# 1. Add APK Link to auto-verified
old_msg1 = """                        f"🔑 <b>YOUR KEY:</b>\\n<code>{delivered_key}</code>\\n\\n"
                        "<i>Thank you for shopping!</i>","""
new_msg1 = """                        f"🔑 <b>YOUR KEY:</b>\\n<code>{delivered_key}</code>\\n\\n"
                        "<i>Thank you for shopping!</i>\\n\\n"
                        "📱 <b>Get the APK here:</b> https://t.me/JFFREEAPK","""
code = code.replace(old_msg1, new_msg1)

# 2. Add APK Link to walletpay_
old_msg2 = """                        f"🔑 <b>YOUR KEY:</b>\\n<code>{delivered_key}</code>\\n\\n"
                        "<i>Thank you for shopping with us!</i>"
                    )"""
new_msg2 = """                        f"🔑 <b>YOUR KEY:</b>\\n<code>{delivered_key}</code>\\n\\n"
                        "<i>Thank you for shopping with us!</i>\\n\\n"
                        "📱 <b>Get the APK here:</b> https://t.me/JFFREEAPK"
                    )"""
code = code.replace(old_msg2, new_msg2)

# 3. Modify add_balance_cb to send qr.png
old_add_bal = """    elif data == "add_balance":
        await query.edit_message_text(
            "💰 <b>ADD BALANCE</b>\\n"
            "━━━━━━━━━━━━━━━━━━\\n"
            "To add funds to your wallet, please select an amount or use the QR scanner in the payment section.\\n\\n"
            "1. Click 'Shop Store Now'\\n"
            "2. Select any product\\n"
            "3. Pay the exact amount\\n\\n"
            "<i>Balance will be added automatically after verification.</i>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🛍️ Go to Shop", callback_data="shop")], [InlineKeyboardButton("« Back", callback_data="main_menu")]]),
            parse_mode="HTML"
        )"""

new_add_bal = """    elif data == "add_balance":
        text = (
            "💰 <b>ADD BALANCE</b>\\n"
            "━━━━━━━━━━━━━━━━━━\\n"
            "To add funds to your wallet, please select an amount or use the QR scanner in the payment section.\\n\\n"
            "1. Click 'Shop Store Now'\\n"
            "2. Select any product\\n"
            "3. Pay the exact amount\\n\\n"
            "<i>Balance will be added automatically after verification.</i>"
        )
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🛍️ Go to Shop", callback_data="shop")], [InlineKeyboardButton("« Back", callback_data="main_menu")]])
        import os
        if os.path.exists("qr.png"):
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=open("qr.png", "rb"), caption=text, reply_markup=keyboard, parse_mode="HTML")
            await query.message.delete()
        else:
            await query.edit_message_text(text, reply_markup=keyboard, parse_mode="HTML")"""
code = code.replace(old_add_bal, new_add_bal)

# 4. Remove KIWMODZ, YOONSO, ANGRY, VIPER from get_shop_keyboard
code = code.replace('        InlineKeyboardButton("KIWMODZ EXE", callback_data="product_kiwmodz"),\\n', '')
code = code.replace('        InlineKeyboardButton("YOONSO BUTTERFLY", callback_data="product_yoonso"),\\n', '')
code = code.replace('        InlineKeyboardButton("ANGRY MOD", callback_data="product_angry"),\\n', '')
code = code.replace('        InlineKeyboardButton("VIPER TEAM", callback_data="product_viper"),\\n', '')

# 5. Remove from admin bulk
code = code.replace('            [InlineKeyboardButton("KIWMODZ EXE", callback_data="bulk_prod_kiwmodz"), InlineKeyboardButton("ANGRY MOD", callback_data="bulk_prod_angry")],\\n', '')
code = code.replace('            [InlineKeyboardButton("RAPID CORE", callback_data="bulk_prod_rapid"), InlineKeyboardButton("YOONSO", callback_data="bulk_prod_yoonso")],\\n', '            [InlineKeyboardButton("RAPID CORE", callback_data="bulk_prod_rapid")],\\n')
code = code.replace('            [InlineKeyboardButton("SVJ", callback_data="bulk_prod_svj"), InlineKeyboardButton("VIPER", callback_data="bulk_prod_viper")],\\n', '            [InlineKeyboardButton("SVJ", callback_data="bulk_prod_svj")],\\n')

# 6. Add BR MODS to get_shop_keyboard
old_beyond = '        InlineKeyboardButton("BEYOND CHEATS", callback_data="product_beyond"),'
new_beyond = '        InlineKeyboardButton("BR MODS", callback_data="product_brmods"),\\n        InlineKeyboardButton("BEYOND CHEATS", callback_data="product_beyond"),'
code = code.replace(old_beyond, new_beyond)

with open("JF BOT/bot.py", "w") as f:
    f.write(code)

print("Patch 7 applied")

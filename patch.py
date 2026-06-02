import json
import os
import re

with open("JF BOT/bot.py", "r") as f:
    code = f.read()

# 1. Update load_reseller_logs to ensure we know it returns a list of strings
# 2. Update rlogs_cmd to filter lists
code = code.replace("""    if target_id not in logs or len(logs[target_id]) == 0:
        await update.message.reply_text("❌ No activity found for this reseller.")
        return
        
    user_logs = logs[target_id][-20:] # Get last 20 actions""",
"""    user_logs = [log for log in logs if f"User {target_id}" in log][-20:]
    if not user_logs:
        await update.message.reply_text("❌ No activity found for this reseller.")
        return""")

# 3. Update admin_seelog_
code = code.replace("""        if target_id not in logs or len(logs[target_id]) == 0:
            kb = [[InlineKeyboardButton("« Back", callback_data="admin_logsmode")]]; await query.edit_message_text("❌ No activity found for this reseller.", reply_markup=InlineKeyboardMarkup(kb))
            return
        user_logs = logs[target_id][-20:]""",
"""        user_logs = [log for log in logs if f"User {target_id}" in log][-20:]
        if not user_logs:
            kb = [[InlineKeyboardButton("« Back", callback_data="admin_logsmode")]]; await query.edit_message_text("❌ No activity found for this reseller.", reply_markup=InlineKeyboardMarkup(kb))
            return""")

# 4. Update get_shop_keyboard
old_shop = """def get_shop_keyboard():
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
        [InlineKeyboardButton("BS SECURE LOADER", callback_data="product_bssecure")],
        [InlineKeyboardButton("HYDRA ENGINE 8BP", callback_data="product_hydra")],
        [InlineKeyboardButton("OS VICTORY 8BP", callback_data="product_osvictory")],
        [InlineKeyboardButton("« Main Menu", callback_data="main_menu")]
    ]
    return keyboard"""

new_shop = """def get_shop_keyboard(user_id=None):
    all_buttons = [
        InlineKeyboardButton("HXN CHEAT", callback_data="product_hxn"),
        InlineKeyboardButton("LK TEAM", callback_data="product_lk"),
        InlineKeyboardButton("HEX BLADE", callback_data="product_hex"),
        InlineKeyboardButton("ALPHA-X STORE", callback_data="product_alpha"),
        InlineKeyboardButton("PRIME X CHEAT", callback_data="product_prime"),
        InlineKeyboardButton("HARSHIL MODS", callback_data="product_harshil"),
        InlineKeyboardButton("BOOYAH MOD", callback_data="product_boyyah"),
        InlineKeyboardButton("STREAMER X", callback_data="product_streamerx"),
        InlineKeyboardButton("STREAMER-X PRO", callback_data="product_streamerpro"),
        InlineKeyboardButton("NGO TRAN", callback_data="product_ngo"),
        InlineKeyboardButton("GREED CHEAT", callback_data="product_greed"),
        InlineKeyboardButton("TRINITY X ROOT", callback_data="product_trinity"),
        InlineKeyboardButton("FLUORITE ANDROID", callback_data="product_fluorite"),
        InlineKeyboardButton("ELITE TEAM", callback_data="product_eliteteam"),
        InlineKeyboardButton("SVJ CHEATS", callback_data="product_svj"),
        InlineKeyboardButton("VIPER TEAM", callback_data="product_viper"),
        InlineKeyboardButton("BEYOND CHEATS", callback_data="product_beyond"),
        InlineKeyboardButton("ROGERIO MODS", callback_data="product_rogerio"),
        InlineKeyboardButton("HAWK CHEATS", callback_data="product_hawk"),
        InlineKeyboardButton("KIWMODZ EXE", callback_data="product_kiwmodz"),
        InlineKeyboardButton("ANGRY MOD", callback_data="product_angry"),
        InlineKeyboardButton("RAPID CORE", callback_data="product_rapid"),
        InlineKeyboardButton("YOONSO BUTTERFLY", callback_data="product_yoonso"),
        InlineKeyboardButton("PRIME HOOK (.SH)", callback_data="product_primehook"),
        InlineKeyboardButton("BS SECURE LOADER", callback_data="product_bssecure"),
        InlineKeyboardButton("HYDRA ENGINE 8BP", callback_data="product_hydra"),
        InlineKeyboardButton("OS VICTORY 8BP", callback_data="product_osvictory"),
    ]
    
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
    return keyboard"""

code = code.replace(old_shop, new_shop)

# Update get_shop_keyboard() call in button_handler
code = code.replace("keyboard = get_shop_keyboard()", "keyboard = get_shop_keyboard(update.effective_user.id)")

# 5. Add trial BR MODS
old_trial_keys = """            [InlineKeyboardButton("GREED CHEAT", callback_data="claim_trial_greed"), InlineKeyboardButton("STREAMER X (.SH)", callback_data="claim_trial_streamerx")],
            [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="main_menu")]"""
new_trial_keys = """            [InlineKeyboardButton("GREED CHEAT", callback_data="claim_trial_greed"), InlineKeyboardButton("STREAMER X (.SH)", callback_data="claim_trial_streamerx")],
            [InlineKeyboardButton("BR MODS", callback_data="claim_trial_brmods"), InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="main_menu")]"""
code = code.replace(old_trial_keys, new_trial_keys)


# 6. Referral Implementation
old_start = """    if is_banned(user_id):
        await update.message.reply_text("🚫 You are banned from this bot for abusing the trial system.")
        return
    save_user(user_id)"""

new_start = """    if is_banned(user_id):
        await update.message.reply_text("🚫 You are banned from this bot for abusing the trial system.")
        return
    save_user(user_id)
    
    # Referral System
    if context.args and len(context.args) > 0:
        referrer_id = context.args[0]
        if str(referrer_id).isdigit() and str(referrer_id) != str(user_id):
            refs = load_referrals()
            if "referred" not in refs: refs["referred"] = []
            if "users" not in refs: refs["users"] = {}
            if user_id not in refs["referred"]:
                refs["referred"].append(user_id)
                if referrer_id not in refs["users"]: refs["users"][referrer_id] = {"count": 0, "earnings": 0.0}
                refs["users"][referrer_id]["count"] += 1
                refs["users"][referrer_id]["earnings"] += 10.0
                save_referrals(refs)
                
                bals = load_balances()
                bals[int(referrer_id)] = bals.get(int(referrer_id), 0) + 10
                save_balances(bals)
                
                try:
                    await context.bot.send_message(chat_id=int(referrer_id), text=f"🎉 <b>New Referral!</b>\\nSomeone joined using your link. You earned ₹10.00!", parse_mode="HTML")
                except:
                    pass"""

code = code.replace(old_start, new_start)

# Update referral button UI
old_ref_ui = """    elif data == "referral":
        bot_username = (await context.bot.get_me()).username
        referral_link = f"https://t.me/{bot_username}?start={update.effective_user.id}"
        await query.edit_message_text(
            "🎁 <b>REFERRAL SYSTEM</b>\\n"
            "━━━━━━━━━━━━━━━━━━\\n"
            "Invite your friends and earn rewards!\\n\\n"
            f"🔗 <b>Your Link:</b>\\n<code>{referral_link}</code>\\n\\n"
            "👥 <b>Total Referrals:</b> 0\\n"
            "💰 <b>Earnings:</b> ₹0.00","""

new_ref_ui = """    elif data == "referral":
        bot_username = (await context.bot.get_me()).username
        referral_link = f"https://t.me/{bot_username}?start={update.effective_user.id}"
        refs = load_referrals()
        user_refs = refs.get("users", {}).get(str(update.effective_user.id), {"count": 0, "earnings": 0.0})
        count = user_refs["count"]
        earnings = user_refs["earnings"]
        await query.edit_message_text(
            "🎁 <b>REFERRAL SYSTEM</b>\\n"
            "━━━━━━━━━━━━━━━━━━\\n"
            "Invite your friends and earn ₹10 to your wallet per invite!\\n\\n"
            f"🔗 <b>Your Link:</b>\\n<code>{referral_link}</code>\\n\\n"
            f"👥 <b>Total Referrals:</b> {count}\\n"
            f"💰 <b>Earnings:</b> ₹{earnings:.2f}","""

code = code.replace(old_ref_ui, new_ref_ui)


# Add /rperms command
old_commands = """    application.add_handler(CommandHandler("start", start))"""
new_commands = """async def rperms_cmd(update, context):
    user_id = update.effective_user.id
    settings = load_settings()
    if user_id not in settings["admin_ids"]: return
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /rperms [reseller_id] [product1,product2 OR clear]\\nExample: /rperms 123456789 hxn,hex,prime")
        return
    target_id = context.args[0]
    perms_str = context.args[1]
    perms = load_reseller_perms()
    if perms_str.lower() == "clear":
        perms[target_id] = []
    else:
        perms[target_id] = perms_str.split(",")
    save_reseller_perms(perms)
    await update.message.reply_text(f"✅ Permissions updated for reseller {target_id}.\\nAllowed: {perms[target_id]}")

    application.add_handler(CommandHandler("start", start))"""
code = code.replace(old_commands, new_commands)
code = code.replace("""    application.add_handler(CommandHandler("rlogs", rlogs_cmd))""", """    application.add_handler(CommandHandler("rlogs", rlogs_cmd))
    application.add_handler(CommandHandler("rperms", rperms_cmd))""")


with open("JF BOT/bot.py", "w") as f:
    f.write(code)

print("Patch applied successfully.")

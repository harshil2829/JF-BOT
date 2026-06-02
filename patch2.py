import os
import re

with open("JF BOT/bot.py", "r") as f:
    code = f.read()

# 1. Update save_reseller_logs and log_reseller_action
old_log = """def save_reseller_logs(user_id, product, key):
    logs = load_reseller_logs()
    from datetime import datetime
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logs.append(f"{time_str} - User {user_id} generated {product} key: {key}")
    if len(logs) > 50: logs = logs[-50:]
    jf_col.update_one({"_id": "reseller_logs"}, {"$set": {"data": logs}}, upsert=True)

def log_reseller_action(user_id, product, duration_label):
    save_reseller_logs(user_id, product, "N/A")"""

new_log = """def save_reseller_logs(username, user_id, product, key):
    logs = load_reseller_logs()
    from datetime import datetime
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logs.append(f"{time_str} - {username} ({user_id}) gen {product}: {key}")
    if len(logs) > 50: logs = logs[-50:]
    jf_col.update_one({"_id": "reseller_logs"}, {"$set": {"data": logs}}, upsert=True)

def log_reseller_action(username, user_id, product, key):
    save_reseller_logs(username, user_id, product, key)"""

code = code.replace(old_log, new_log)

# 2. Update log_reseller_action call in gen_key_cmd
old_gen = """    if delivered_key:
        log_reseller_action(user_id, product, duration_label)"""
new_gen = """    if delivered_key:
        username = f"@{update.effective_user.username}" if update.effective_user.username else str(update.effective_user.first_name)
        log_reseller_action(username, user_id, product, delivered_key)"""
code = code.replace(old_gen, new_gen)

# 3. Update get_shop_keyboard correctly!
shop_pattern = re.compile(r"def get_shop_keyboard\(\):.*?return InlineKeyboardMarkup\(keyboard\)", re.DOTALL)

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
        InlineKeyboardButton("HXN STREAMER (.SH)", callback_data="product_streamerxsh"),
        InlineKeyboardButton("BS SECURE LOADER", callback_data="product_bssecure"),
        InlineKeyboardButton("HYDRA ENGINE 8BP", callback_data="product_hydra"),
        InlineKeyboardButton("OS VICTORY 8BP", callback_data="product_osvictory")
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
    return InlineKeyboardMarkup(keyboard)"""

code = shop_pattern.sub(new_shop, code)

# 4. We also need to fix `admin_seelog_` and `rlogs_cmd` to search for `({target_id})` instead of `User {target_id}` 
# because we changed the string format!
code = code.replace('f"User {target_id}"', 'f"({target_id})"')

with open("JF BOT/bot.py", "w") as f:
    f.write(code)

print("Patch 2 applied")

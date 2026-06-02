import os

with open("JF BOT/bot.py", "r") as f:
    code = f.read()

old_code = """                if user_id_str in resellers_check:
                    debug_log("Calling log_reseller_action")
                    log_reseller_action(username_str, user_id_str, product, delivered_key)
                    debug_log("log_reseller_action finished")
                
                success_msg = ("""

new_code = """                username_str = f"@{query.from_user.username}" if query.from_user.username else str(query.from_user.first_name)
                if user_id_str in resellers_check:
                    debug_log("Calling log_reseller_action")
                    log_reseller_action(username_str, user_id_str, product, delivered_key)
                    debug_log("log_reseller_action finished")
                
                settings = load_settings()
                admin_ids = settings.get("admin_ids", [])
                for admin_id in admin_ids:
                    try:
                        admin_msg = (
                            f"🔔 <b>NEW WALLET PURCHASE</b>\\n"
                            f"━━━━━━━━━━━━━━━━━━\\n"
                            f"👤 <b>User:</b> {username_str} (<code>{user_id_str}</code>)\\n"
                            f"🏺 <b>Product:</b> {product.upper()}\\n"
                            f"⏳ <b>Duration:</b> {duration_label.upper()}\\n"
                            f"💵 <b>Amount Paid:</b> ₹{amount}\\n"
                            f"🔑 <b>Key Generated:</b> <code>{delivered_key}</code>\\n"
                        )
                        await context.bot.send_message(chat_id=admin_id, text=admin_msg, parse_mode="HTML")
                    except:
                        pass

                success_msg = ("""

code = code.replace(old_code, new_code)

with open("JF BOT/bot.py", "w") as f:
    f.write(code)

print("Patch 4 applied")

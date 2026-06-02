import os

with open("JF BOT/bot.py", "r") as f:
    code = f.read()

# Fix walletpay_
old_wallet = """            if delivered_key:
                success_msg = (
                    "✅ <b>PURCHASE SUCCESSFUL!</b>\\n\""""

new_wallet = """            if delivered_key:
                resellers_check = load_resellers()
                if user_id_str in resellers_check:
                    username_str = f"@{query.from_user.username}" if query.from_user.username else str(query.from_user.first_name)
                    log_reseller_action(username_str, user_id_str, product, delivered_key)
                
                success_msg = (
                    "✅ <b>PURCHASE SUCCESSFUL!</b>\\n\""""

code = code.replace(old_wallet, new_wallet)

# Fix approve_
old_approve = """        if delivered_key:
            # Send Key to User
            success_msg = (
                "✅ <b>PAYMENT VERIFIED!</b>\\n\""""

new_approve = """        if delivered_key:
            resellers_check = load_resellers()
            target_str = str(target_user_id)
            if target_str in resellers_check:
                # We don't have their username easily here, so we just use "Reseller"
                log_reseller_action("Reseller", target_str, product, delivered_key)
                
            # Send Key to User
            success_msg = (
                "✅ <b>PAYMENT VERIFIED!</b>\\n\""""

code = code.replace(old_approve, new_approve)

with open("JF BOT/bot.py", "w") as f:
    f.write(code)

print("Patch applied for wallet and approve logging")

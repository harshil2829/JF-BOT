import os

with open("JF BOT/bot.py", "r") as f:
    lines = f.readlines()

new_lines = []
in_walletpay = False
walletpay_indent = 0

for i, line in enumerate(lines):
    if line.startswith('    elif data.startswith("walletpay_"):'):
        new_lines.append(line)
        new_lines.append('        try:\n')
        in_walletpay = True
        walletpay_indent = len(line) - len(line.lstrip())
        continue
        
    if in_walletpay:
        current_indent = len(line) - len(line.lstrip())
        if line.strip() == "":
            new_lines.append(line)
        elif current_indent <= walletpay_indent:
            # We exited walletpay_
            new_lines.append('        except Exception as e:\n')
            new_lines.append('            import traceback\n')
            new_lines.append('            err = traceback.format_exc()\n')
            new_lines.append('            await query.edit_message_text(f"⚠️ INTERNAL ERROR:\\n<pre>{err[-500:]}</pre>", parse_mode="HTML")\n')
            in_walletpay = False
            new_lines.append(line)
        else:
            # Inside walletpay_, add 4 spaces
            new_lines.append("    " + line)
    else:
        new_lines.append(line)

with open("JF BOT/bot.py", "w") as f:
    f.writelines(new_lines)

print("Patch 5 applied")

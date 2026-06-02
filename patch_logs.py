import os

with open("JF BOT/bot.py", "r") as f:
    code = f.read()

# Fix rlogs_cmd loop
old_rlogs_loop = """    for log in user_logs:
        date_str = datetime.datetime.fromtimestamp(log["time"]).strftime('%Y-%m-%d %H:%M')
        text += f"• {date_str} - Generated {log['product'].upper()} ({log['duration']})\\n\""""
new_rlogs_loop = """    for log in user_logs:
        text += f"• {log}\\n\""""
code = code.replace(old_rlogs_loop, new_rlogs_loop)

# Fix admin_seelog_ loop
old_seelog_loop = """        for log in user_logs:
            date_str = datetime.datetime.fromtimestamp(log["time"]).strftime('%Y-%m-%d %H:%M')
            text += f"• {date_str} - Gen {log['product'].upper()} ({log['duration']})\\n\""""
new_seelog_loop = """        for log in user_logs:
            text += f"• {log}\\n\""""
code = code.replace(old_seelog_loop, new_seelog_loop)

with open("JF BOT/bot.py", "w") as f:
    f.write(code)

print("Logs formatting patched.")

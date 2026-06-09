import json
import re

# 1. Update Token
with open("bot.py", "r") as f:
    content = f.read()
content = re.sub(r'TOKEN\s*=\s*".*?"', 'TOKEN = "7994962595:AAGOZdezJAetEVJPCpbOVqAds7AYaypWlRY"', content)
with open("bot.py", "w") as f:
    f.write(content)

# 2. Reset JSON files
with open("keys.json", "w") as f: json.dump({}, f)
with open("balances.json", "w") as f: json.dump({}, f)
with open("resellers.json", "w") as f: json.dump({}, f)
with open("reseller_logs.json", "w") as f: json.dump({}, f)
with open("verified_users.json", "w") as f: json.dump([], f)
with open("utr_log.json", "w") as f: json.dump([], f)

# Make sure admin is the current user for testing
with open("settings.json", "r") as f:
    settings = json.load(f)
# Clear channels for the fresh bot
settings["force_channels"] = []
settings["force_channel"] = ""
settings["invite_link"] = ""
with open("settings.json", "w") as f:
    json.dump(settings, f, indent=4)
print("Done!")

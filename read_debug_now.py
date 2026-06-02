from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://admin:HARSHIL2829@cluster0.6kcmggh.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client["jf_bot"]
jf_col = db["bot_data"]

logs = jf_col.find_one({"_id": "debug_logs"})
if logs and "data" in logs and logs["data"]:
    print("--- DEBUG LOGS ---")
    for log in logs["data"]:
        print(log)
else:
    print("No debug logs found.")

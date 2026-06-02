from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://admin:HARSHIL2829@cluster0.6kcmggh.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client["jf_bot"]
jf_col = db["bot_data"]

doc = jf_col.find_one({"_id": "reseller_logs"})
if doc:
    print("Type of data:", type(doc["data"]))
    print("Value:", doc["data"])
else:
    print("No doc found")

from pymongo import MongoClient
import os
import json

client = MongoClient("mongodb+srv://harshil:harshil@cluster0.zoxmb8f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["jf_hacks"]
jf_col = db["jf_bot"]

trials = jf_col.find_one({"_id": "trials"})
print("Trials count:", len(trials["data"]) if trials else 0)

keys = jf_col.find_one({"_id": "keys"})
if keys:
    print("Keys:")
    for k, v in keys["data"].items():
        print(f"  {k}: {len(v)} keys")

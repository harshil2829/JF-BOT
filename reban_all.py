"""Re-ban all users who have any strikes (they left the channel at least once)."""
from pymongo import MongoClient
client = MongoClient('mongodb+srv://admin:28295609@cluster0.6kcmggh.mongodb.net/?appName=Cluster0')
db = client['TelegramBotDB']
jf_col = db['jf_data']
doc = jf_col.find_one({'_id': 'trials'})
if doc and 'data' in doc:
    trials = doc['data']
    count_before = sum(1 for v in trials.values() if v.get('banned', False))
    count_rebanned = 0
    for uid, data in trials.items():
        if data.get('strikes', 0) > 0 and not data.get('banned', False):
            data['banned'] = True
            count_rebanned += 1
    count_after = sum(1 for v in trials.values() if v.get('banned', False))
    jf_col.update_one({'_id': 'trials'}, {'$set': {'data': trials}}, upsert=True)
    print(f'Banned BEFORE: {count_before}')
    print(f'Newly re-banned: {count_rebanned}')
    print(f'Total banned NOW: {count_after}')
    print(f'Total trial entries: {len(trials)}')
else:
    print('No trials data found')

const { MongoClient } = require('mongodb');
const uri = 'mongodb+srv://admin:HARSHIL2829@cluster0.6kcmggh.mongodb.net/?appName=Cluster0';
const client = new MongoClient(uri);

async function main() {
    await client.connect();
    const db = client.db('TelegramBotDB');
    const col = db.collection('jf_data');
    const doc = await col.findOne({ _id: 'trials' });
    if (!doc || !doc.data) {
        console.log('No trials data found');
        await client.close();
        return;
    }
    const trials = doc.data;
    const entries = Object.entries(trials);
    const banned = entries.filter(([k, v]) => v.banned === true);
    const strikers = entries.filter(([k, v]) => (v.strikes || 0) > 0);
    const three_plus = entries.filter(([k, v]) => (v.strikes || 0) >= 3);
    console.log(`Total trial entries: ${entries.length}`);
    console.log(`Users with strikes > 0: ${strikers.length}`);
    console.log(`Users with strikes >= 3: ${three_plus.length}`);
    console.log(`Currently banned: ${banned.length}`);
    console.log('\n--- Banned users list ---');
    for (const [uid, data] of banned) {
        console.log(`  ${uid}: strikes=${data.strikes}, banned=${data.banned}, username=${data.username || 'N/A'}, name=${data.name || 'N/A'}`);
    }
    await client.close();
}
main().catch(console.error);

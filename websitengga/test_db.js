const { MongoClient } = require('mongodb');

async function test() {
  const uri = "mongodb+srv://admin:HARSHIL2829@cluster0.6kcmggh.mongodb.net/?appName=Cluster0";
  const client = new MongoClient(uri);
  await client.connect();
  const db = client.db('TelegramBotDB');
  const col = db.collection('jf_data');
  const usersDoc = await col.findOne({ _id: "users" });
  console.log("Users:", usersDoc.data ? (Array.isArray(usersDoc.data) ? 'Array of ' + usersDoc.data.length : 'Object with ' + Object.keys(usersDoc.data).length) : 'null');
  process.exit(0);
}
test();

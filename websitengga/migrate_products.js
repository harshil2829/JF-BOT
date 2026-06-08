const { MongoClient } = require('mongodb');

const MONGO_URI = "mongodb+srv://admin:HARSHIL2829@cluster0.6kcmggh.mongodb.net/?appName=Cluster0";
const client = new MongoClient(MONGO_URI);

async function run() {
  try {
    await client.connect();
    const db = client.db('TelegramBotDB');
    const col = db.collection('jf_data');
    
    const existingProducts = [
      { name: "hxn", price: 150, status: "Active", section: "Both" },
      { name: "lk", price: 150, status: "Active", section: "Both" },
      { name: "hex", price: 150, status: "Active", section: "Both" },
      { name: "alpha", price: 150, status: "Active", section: "Both" },
      { name: "boyyah", price: 150, status: "Active", section: "Both" },
      { name: "ngo", price: 150, status: "Active", section: "Both" },
      { name: "greed", price: 150, status: "Active", section: "Both" },
      { name: "streamerx", price: 150, status: "Active", section: "Both" },
      { name: "brmods", price: 150, status: "Active", section: "Both" },
      { name: "prime", price: 150, status: "Active", section: "Both" },
      { name: "harshil", price: 150, status: "Active", section: "Both" },
      { name: "streamerxsh", price: 150, status: "Active", section: "Both" }
    ];

    await col.updateOne(
      { _id: "web_products" },
      { $set: { data: existingProducts } },
      { upsert: true }
    );
    console.log("Successfully migrated all existing products to web DB!");
  } finally {
    await client.close();
  }
}
run();

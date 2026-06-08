"use server";

import clientPromise from '@/lib/mongodb';

const BOT_TOKEN = "7994962595:AAGOZdezJAetEVJPCpbOVqAds7AYaypWlRY";

export async function sendBroadcast(message, targetGroup) {
  if (!message.trim()) return { error: "Message cannot be empty." };

  const client = await clientPromise;
  const db = client.db('TelegramBotDB');
  const col = db.collection('jf_data');

  const usersDoc = await col.findOne({ _id: "users" });
  if (!usersDoc || !usersDoc.data || !Array.isArray(usersDoc.data)) {
    return { error: "No users found in database." };
  }

  let users = usersDoc.data;

  // Let's create a real broadcast history entry
  const broadcastLog = {
    message,
    target: targetGroup,
    date: new Date().toISOString(),
    totalTarget: users.length,
    success: 0,
    failed: 0,
    status: 'Running'
  };

  const logsDoc = await col.findOne({ _id: "broadcast_logs" });
  let logs = [];
  if (logsDoc && logsDoc.data) {
    logs = logsDoc.data;
  }
  logs.unshift(broadcastLog);
  await col.updateOne({ _id: "broadcast_logs" }, { $set: { data: logs } }, { upsert: true });

  // Run the broadcast in the background
  setTimeout(async () => {
    await processBroadcast(users, message, broadcastLog.date);
  }, 0);

  return { success: true };
}

async function processBroadcast(users, message, logDate) {
  let successCount = 0;
  let failedCount = 0;

  for (let i = 0; i < users.length; i++) {
    const uid = users[i];
    try {
      const res = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          chat_id: uid,
          text: message,
          parse_mode: "HTML"
        })
      });
      if (res.ok) {
        successCount++;
      } else {
        const err = await res.text();
        console.error("TG API Error:", err);
        failedCount++;
      }
    } catch (e) {
      console.error("Fetch Error:", e);
      failedCount++;
    }
    
    // Update DB every 20 messages so the UI can poll progress
    if (i % 20 === 0 || i === users.length - 1) {
      const client = await clientPromise;
      const db = client.db('TelegramBotDB');
      const col = db.collection('jf_data');
      const logsDoc = await col.findOne({ _id: "broadcast_logs" });
      if (logsDoc && logsDoc.data) {
        let logs = logsDoc.data;
        const logIdx = logs.findIndex(l => l.date === logDate);
        if (logIdx > -1) {
          logs[logIdx].success = successCount;
          logs[logIdx].failed = failedCount;
          if (i === users.length - 1) {
            logs[logIdx].status = 'Completed';
          }
          await col.updateOne({ _id: "broadcast_logs" }, { $set: { data: logs } });
        }
      }
    }

    // simple delay to prevent rate limits
    await new Promise(r => setTimeout(r, 10)); // 10ms to speed it up
  }

  console.log(`Broadcast done. Success: ${successCount}, Failed: ${failedCount}`);
}

export async function addKeys(product, duration, keysArray) {
  const client = await clientPromise;
  const db = client.db('TelegramBotDB');
  const col = db.collection('jf_data');

  const keysDoc = await col.findOne({ _id: "keys" });
  let data = keysDoc && keysDoc.data ? keysDoc.data : {};
  
  const dictKey = `${product.toLowerCase()}_${duration.toLowerCase()}`;
  if (!data[dictKey]) {
    data[dictKey] = [];
  }
  
  data[dictKey].push(...keysArray);
  
  await col.updateOne({ _id: "keys" }, { $set: { data } }, { upsert: true });
  return { success: true };
}

export async function saveSettings(settings) {
  const client = await clientPromise;
  const db = client.db('TelegramBotDB');
  const col = db.collection('jf_data');

  await col.updateOne({ _id: "web_settings" }, { $set: { data: settings } }, { upsert: true });
  
  // Optionally sync some settings directly to tele_data "settings" doc if needed
  const teleCol = db.collection('tele_data');
  const teleSettingsDoc = await teleCol.findOne({ _id: "settings" });
  let teleSettings = teleSettingsDoc && teleSettingsDoc.data ? teleSettingsDoc.data : { admin_ids: [] };
  
  // if you want to sync maintenance mode to bot
  // teleSettings.maintenance_mode = settings.maintenance_mode;
  // await teleCol.updateOne({ _id: "settings" }, { $set: { data: teleSettings } }, { upsert: true });

  return { success: true };
}

export async function getProducts() {
  const client = await clientPromise;
  const db = client.db('TelegramBotDB');
  const col = db.collection('jf_data');
  const doc = await col.findOne({ _id: "web_products" });
  
  if (!doc || !doc.data || doc.data.length <= 2) {
    const defaultProducts = [
      { name: "hxn", prices: { '1d': 50, '7d': 200, '15d': 400, '30d': 600 }, status: "Active", section: "Both" },
      { name: "lk", prices: { '1d': 50, '7d': 200, '15d': 400, '30d': 600 }, status: "Active", section: "Both" },
      { name: "hex", prices: { '1d': 50, '7d': 200, '15d': 400, '30d': 600 }, status: "Active", section: "Both" },
      { name: "alpha", prices: { '1d': 50, '7d': 200, '15d': 400, '30d': 600 }, status: "Active", section: "Both" },
      { name: "boyyah", prices: { '1d': 50, '7d': 200, '15d': 400, '30d': 600 }, status: "Active", section: "Both" },
      { name: "ngo", prices: { '1d': 50, '7d': 200, '15d': 400, '30d': 600 }, status: "Active", section: "Both" },
      { name: "greed", prices: { '1d': 50, '7d': 200, '15d': 400, '30d': 600 }, status: "Active", section: "Both" },
      { name: "streamerx", prices: { '1d': 50, '7d': 200, '15d': 400, '30d': 600 }, status: "Active", section: "Both" },
      { name: "brmods", prices: { '1d': 50, '7d': 200, '15d': 400, '30d': 600 }, status: "Active", section: "Both" },
      { name: "prime", prices: { '1d': 50, '7d': 200, '15d': 400, '30d': 600 }, status: "Active", section: "Both" },
      { name: "harshil", prices: { '1d': 50, '7d': 200, '15d': 400, '30d': 600 }, status: "Active", section: "Both" },
      { name: "streamerxsh", prices: { '1d': 50, '7d': 200, '15d': 400, '30d': 600 }, status: "Active", section: "Both" }
    ];
    await col.updateOne({ _id: "web_products" }, { $set: { data: defaultProducts } }, { upsert: true });
    return defaultProducts;
  }

  // Handle any existing scalar price products and convert them gracefully just in case
  const updatedData = doc.data.map(p => {
    if (!p.prices) {
      p.prices = { '1d': parseFloat(p.price) || 50, '7d': 200, '15d': 400, '30d': 600 };
      delete p.price;
    }
    return p;
  });

  return updatedData;
}

export async function addProduct(product) {
  const client = await clientPromise;
  const db = client.db('TelegramBotDB');
  const col = db.collection('jf_data');
  const products = await getProducts();
  products.push(product);
  await col.updateOne({ _id: "web_products" }, { $set: { data: products } }, { upsert: true });
  return { success: true };
}

export async function deleteProduct(productName) {
  const client = await clientPromise;
  const db = client.db('TelegramBotDB');
  const col = db.collection('jf_data');
  let products = await getProducts();
  products = products.filter(p => p.name !== productName);
  await col.updateOne({ _id: "web_products" }, { $set: { data: products } }, { upsert: true });
  return { success: true };
}

export async function editProduct(oldName, updatedProduct) {
  const client = await clientPromise;
  const db = client.db('TelegramBotDB');
  const col = db.collection('jf_data');
  let products = await getProducts();
  const index = products.findIndex(p => p.name === oldName);
  if (index > -1) {
    products[index] = updatedProduct;
    await col.updateOne({ _id: "web_products" }, { $set: { data: products } }, { upsert: true });
  }
  return { success: true };
}

export async function getStaff() {
  const client = await clientPromise;
  const db = client.db('TelegramBotDB');
  const col = db.collection('jf_data');
  const doc = await col.findOne({ _id: "web_staff" });
  return doc && doc.data ? doc.data : [];
}

export async function addStaff(staff) {
  const client = await clientPromise;
  const db = client.db('TelegramBotDB');
  const col = db.collection('jf_data');
  const staffList = await getStaff();
  staffList.push(staff);
  await col.updateOne({ _id: "web_staff" }, { $set: { data: staffList } }, { upsert: true });
  return { success: true };
}

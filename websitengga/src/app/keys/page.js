import clientPromise from '@/lib/mongodb';
import KeysClient from './KeysClient';

async function getKeysData() {
  const client = await clientPromise;
  const db = client.db('TelegramBotDB');
  const col = db.collection('jf_data');

  const keysDoc = await col.findOne({ _id: "keys" });
  let products = [];
  
  if (keysDoc && keysDoc.data) {
    for (const [productName, keys] of Object.entries(keysDoc.data)) {
      products.push({
        name: productName,
        count: Array.isArray(keys) ? keys.length : 0,
        keys: Array.isArray(keys) ? keys.slice(0, 10) : [] // show a preview of 10
      });
    }
  }

  return products;
}

export const revalidate = 0;

export default async function KeysPage() {
  const products = await getKeysData();
  return <KeysClient initialProducts={products} />;
}

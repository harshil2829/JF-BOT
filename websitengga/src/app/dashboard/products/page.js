import clientPromise from '@/lib/mongodb';
import ProductsClient from './ProductsClient';

export const revalidate = 0;

export default async function ProductsPage() {
  const client = await clientPromise;
  const db = client.db('TelegramBotDB');
  const col = db.collection('jf_data');
  const doc = await col.findOne({ _id: "web_products" });
  
  const initialProducts = doc && doc.data ? doc.data : [
    { name: "BR Mod", price: 150, status: "Active" },
    { name: "Streamer", price: 300, status: "Active" }
  ];

  return <ProductsClient initialProducts={initialProducts} />;
}

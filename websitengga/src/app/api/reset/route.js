import { NextResponse } from 'next/server';
import clientPromise from '@/lib/mongodb';

export async function GET() {
  try {
    const client = await clientPromise;
    const db = client.db('TelegramBotDB');
    const col = db.collection('jf_data');

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

    return NextResponse.json({ success: true, message: "Products instantly migrated! Go back to http://localhost:3000/products and refresh!" });
  } catch (error) {
    return NextResponse.json({ success: false, error: error.message });
  }
}

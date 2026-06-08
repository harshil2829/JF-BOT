import clientPromise from '@/lib/mongodb';
import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

export async function GET() {
  const client = await clientPromise;
  const db = client.db('TelegramBotDB');
  const col = db.collection('jf_data');

  const logsDoc = await col.findOne({ _id: "broadcast_logs" });
  const logs = logsDoc && logsDoc.data ? logsDoc.data : [];

  return NextResponse.json({ logs });
}

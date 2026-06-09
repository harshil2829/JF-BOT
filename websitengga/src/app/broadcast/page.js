import clientPromise from '@/lib/mongodb';
import BroadcastClient from './BroadcastClient';

export const revalidate = 0;

async function getBroadcastData() {
  const client = await clientPromise;
  const db = client.db('TelegramBotDB');
  const col = db.collection('jf_data');

  const usersDoc = await col.findOne({ _id: "users" });
  const totalUsers = usersDoc && usersDoc.data && Array.isArray(usersDoc.data) ? usersDoc.data.length : 0;

  const logsDoc = await col.findOne({ _id: "broadcast_logs" });
  const logs = logsDoc && logsDoc.data ? logsDoc.data : [];

  return { totalUsers, logs };
}

export default async function BroadcastPage() {
  const { totalUsers, logs } = await getBroadcastData();

  return <BroadcastClient totalUsers={totalUsers} logs={logs} />;
}

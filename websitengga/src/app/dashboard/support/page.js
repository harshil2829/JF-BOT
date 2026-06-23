import clientPromise from '@/lib/mongodb';
import SupportClient from './SupportClient';

export const revalidate = 0;

export default async function SupportPage() {
  const client = await clientPromise;
  const db = client.db('TelegramBotDB');
  const col = db.collection('jf_data');
  const doc = await col.findOne({ _id: "web_staff" });
  
  const initialStaff = doc && doc.data ? doc.data : [];

  return <SupportClient initialStaff={initialStaff} />;
}

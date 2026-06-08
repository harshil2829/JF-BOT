import clientPromise from '@/lib/mongodb';
import SettingsClient from './SettingsClient';

export const revalidate = 0;

async function getSettings() {
  const client = await clientPromise;
  const db = client.db('TelegramBotDB');
  // We'll save UI settings in jf_data collection
  const col = db.collection('jf_data');
  const doc = await col.findOne({ _id: "web_settings" });
  return doc && doc.data ? doc.data : null;
}

export default async function SettingsPage() {
  const initialSettings = await getSettings();
  return <SettingsClient initialSettings={initialSettings} />;
}

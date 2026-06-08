import { 
  Users, Key, ShieldCheck, Settings, HeadphonesIcon, XCircle, Crown, LayoutDashboard, Database
} from 'lucide-react';

import clientPromise from '@/lib/mongodb';
import AnalyticsChart from '@/components/Chart';

async function getStats() {
  const client = await clientPromise;
  const db = client.db('TelegramBotDB');
  const col = db.collection('jf_data');

  const usersDoc = await col.findOne({ _id: "users" });
  const trialsDoc = await col.findOne({ _id: "trials" });
  const resellersDoc = await col.findOne({ _id: "resellers" });
  const keysDoc = await col.findOne({ _id: "keys" });
  const globalStatsDoc = await col.findOne({ _id: "global_stats" });

  const totalUsers = usersDoc && usersDoc.data 
    ? (Array.isArray(usersDoc.data) ? usersDoc.data.length : Object.keys(usersDoc.data).length) 
    : 0;
  
  let totalBanned = 0;
  let activeUsers = 0;
  if (trialsDoc && trialsDoc.data) {
    const trials = Object.values(trialsDoc.data);
    totalBanned = trials.filter(t => t && t.banned).length;
    activeUsers = trials.filter(t => t && !t.banned && t.trial_used).length;
  }

  const totalResellers = resellersDoc && resellersDoc.data 
    ? (Array.isArray(resellersDoc.data) ? resellersDoc.data.length : Object.keys(resellersDoc.data).length) 
    : 0;
  
  let totalKeys = 0;
  if (keysDoc && keysDoc.data) {
    totalKeys = Object.values(keysDoc.data).reduce((acc, curr) => acc + (Array.isArray(curr) ? curr.length : 0), 0);
  }

  const claimedFromStats = globalStatsDoc && globalStatsDoc.data ? globalStatsDoc.data.total_keys_used || 0 : 0;
  
  // Also count from reseller logs for accuracy
  const resellerLogsDoc = await col.findOne({ _id: "reseller_logs" });
  const resellerKeyCount = resellerLogsDoc && Array.isArray(resellerLogsDoc.data) ? resellerLogsDoc.data.length : 0;
  
  // Count all user history_ entries
  const historyDocs = await col.find({ _id: { $regex: /^history_/ } }).toArray();
  let userKeyCount = 0;
  for (const doc of historyDocs) {
    if (Array.isArray(doc.data)) userKeyCount += doc.data.length;
  }
  
  const claimedKeys = Math.max(claimedFromStats, userKeyCount + resellerKeyCount);

  const activityDoc = await col.findOne({ _id: "bot_activity_logs" });
  const recentActivity = activityDoc && activityDoc.data && Array.isArray(activityDoc.data) 
    ? activityDoc.data.slice(-5).reverse() 
    : [];

  return {
    totalUsers: totalUsers || 0,
    activeUsers: activeUsers || 0,
    totalBanned: totalBanned || 0,
    totalResellers: totalResellers || 0,
    totalKeys: totalKeys || 0,
    claimedKeys: claimedKeys || 0,
    recentActivity: recentActivity
  };
}

export const revalidate = 0; // Disable cache so it updates live

export default async function Dashboard() {
  const stats = await getStats();

  return (
    <>
      {/* Main Content */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <div>
          <h1 style={{ fontSize: '24px', margin: '0 0 5px 0' }}>Dashboard</h1>
          <p style={{ color: 'var(--text-muted)', margin: 0, fontSize: '14px' }}>Welcome back! Here's your real-time bot overview.</p>
        </div>
        <button className="btn-primary">Refresh Data</button>
      </div>

        {/* Top Cards */}
        <div className="mobile-grid-5" style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '15px', marginBottom: '20px' }}>
          <div className="card stat-card" style={{ borderLeft: '4px solid var(--primary)' }}>
            <div className="stat-header">
              <Users size={20} color="var(--primary)" />
              <span className="badge positive">Live</span>
            </div>
            <p className="stat-title">Total Users</p>
            <h2 className="stat-value">{stats.totalUsers.toLocaleString()}</h2>
          </div>
          <div className="card stat-card" style={{ borderLeft: '4px solid var(--success)' }}>
            <div className="stat-header">
              <ShieldCheck size={20} color="var(--success)" />
              <span className="badge positive">Live</span>
            </div>
            <p className="stat-title">Trial Users</p>
            <h2 className="stat-value">{stats.activeUsers.toLocaleString()}</h2>
          </div>
          <div className="card stat-card" style={{ borderLeft: '4px solid #b388ff' }}>
            <div className="stat-header">
              <Crown size={20} color="#b388ff" />
              <span className="badge positive">Live</span>
            </div>
            <p className="stat-title">VIP Resellers</p>
            <h2 className="stat-value">{stats.totalResellers.toLocaleString()}</h2>
          </div>
          <div className="card stat-card" style={{ borderLeft: '4px solid var(--danger)' }}>
            <div className="stat-header">
              <XCircle size={20} color="var(--danger)" />
              <span className="badge negative">Banned</span>
            </div>
            <p className="stat-title">Banned Users</p>
            <h2 className="stat-value">{stats.totalBanned.toLocaleString()}</h2>
          </div>
          <div className="card stat-card" style={{ borderLeft: '4px solid var(--warning)' }}>
            <div className="stat-header">
              <Key size={20} color="var(--warning)" />
              <span className="badge positive">{stats.claimedKeys} Used</span>
            </div>
            <p className="stat-title">Keys in Stock</p>
            <h2 className="stat-value">{stats.totalKeys.toLocaleString()}</h2>
          </div>
        </div>

        {/* Analytics & Activity Section */}
        <div className="mobile-grid-2" style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }}>
          
          {/* Main Chart */}
          <div className="card">
            <h3 style={{ fontSize: '16px', marginBottom: '5px' }}>Traffic Analytics</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '13px' }}>User growth vs Key generation over last 7 days</p>
            <AnalyticsChart />
          </div>

          {/* Activity Feed */}
          <div className="card">
            <h3 style={{ fontSize: '16px', marginBottom: '20px' }}>Live Activity</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              {stats.recentActivity.map((log, idx) => (
                <div key={idx} style={{ display: 'flex', gap: '10px', alignItems: 'flex-start' }}>
                  <div style={{ background: 'rgba(0, 210, 255, 0.1)', padding: '8px', borderRadius: '50%' }}>
                    <Users size={16} color="var(--primary)" />
                  </div>
                  <div>
                    <p style={{ fontSize: '13px', margin: '0 0 3px 0' }}><b>User ID: {log.uid || 'Unknown'}</b> {log.action}</p>
                    <p style={{ fontSize: '11px', color: 'var(--text-muted)', margin: 0 }}>{log.time || 'Recent Activity'}</p>
                  </div>
                </div>
              ))}
              {stats.recentActivity.length === 0 && (
                <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>No recent activity yet. Logs will appear when users interact with the bot.</p>
              )}
            </div>
            <button className="btn-primary" style={{ width: '100%', marginTop: '20px', background: 'transparent', border: '1px solid var(--border)', color: 'white', boxShadow: 'none' }}>View Full Logs</button>
          </div>

        </div>

    </>
  );
}

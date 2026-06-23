import clientPromise from '@/lib/mongodb';
import { Search, Ban, CheckCircle } from 'lucide-react';

async function getUsersData() {
  const client = await clientPromise;
  const db = client.db('TelegramBotDB');
  const col = db.collection('jf_data');

  const usersDoc = await col.findOne({ _id: "users" });
  const balancesDoc = await col.findOne({ _id: "balances" });
  const trialsDoc = await col.findOne({ _id: "trials" });

  let usersList = [];
  if (usersDoc && usersDoc.data && Array.isArray(usersDoc.data)) {
    // Reverse so newest users are first
    const reversedIds = [...usersDoc.data].reverse();
    // For performance, let's just show top 100 on the dashboard
    usersList = reversedIds.slice(0, 100).map(uid => {
      const balance = balancesDoc && balancesDoc.data && balancesDoc.data[uid] ? balancesDoc.data[uid] : 0;
      const trialInfo = trialsDoc && trialsDoc.data && trialsDoc.data[uid] ? trialsDoc.data[uid] : {};
      return {
        id: uid,
        balance: balance,
        banned: trialInfo.banned || false
      };
    });
  }

  return usersList;
}

export const revalidate = 0; // live reload

export default async function UsersPage() {
  const users = await getUsersData();

  return (
    <>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <div>
          <h1 style={{ fontSize: '24px', margin: '0 0 5px 0' }}>User Management</h1>
          <p style={{ color: 'var(--text-muted)', margin: 0, fontSize: '14px' }}>View, ban, and modify all users interacting with your bot.</p>
        </div>
        <button className="btn-primary">Export User List</button>
      </div>
      
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h3 style={{ margin: 0 }}>Recent Users Database</h3>
          <div style={{ background: '#222', padding: '8px 15px', borderRadius: '8px', display: 'flex', gap: '10px', alignItems: 'center', width: '300px' }}>
            <Search size={16} color="var(--text-muted)" />
            <input 
              type="text" 
              placeholder="Search User ID..." 
              style={{ background: 'transparent', border: 'none', color: 'white', outline: 'none', width: '100%', fontSize: '14px' }}
            />
          </div>
        </div>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '14px' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border)', color: 'var(--text-muted)' }}>
                <th style={{ padding: '15px 10px', fontWeight: 500 }}>User ID</th>
                <th style={{ padding: '15px 10px', fontWeight: 500 }}>Wallet Balance</th>
                <th style={{ padding: '15px 10px', fontWeight: 500 }}>Status</th>
                <th style={{ padding: '15px 10px', fontWeight: 500, textAlign: 'right' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.length === 0 && (
                <tr><td colSpan="4" style={{ padding: '20px', textAlign: 'center', color: 'var(--text-muted)' }}>No users found.</td></tr>
              )}
              {users.map((user, idx) => (
                <tr key={idx} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                  <td style={{ padding: '15px 10px', fontWeight: 600 }}>{user.id}</td>
                  <td style={{ padding: '15px 10px', color: 'var(--success)' }}>₹{user.balance.toFixed(2)}</td>
                  <td style={{ padding: '15px 10px' }}>
                    {user.banned ? (
                      <span className="badge negative">Banned</span>
                    ) : (
                      <span className="badge positive">Active</span>
                    )}
                  </td>
                  <td style={{ padding: '15px 10px', textAlign: 'right' }}>
                    <button style={{ background: 'transparent', border: '1px solid #333', color: 'white', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer', marginRight: '10px' }}>Edit Balance</button>
                    {user.banned ? (
                      <button style={{ background: 'transparent', border: '1px solid var(--success)', color: 'var(--success)', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer' }}>Unban</button>
                    ) : (
                      <button style={{ background: 'transparent', border: '1px solid var(--danger)', color: 'var(--danger)', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer' }}>Ban</button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}

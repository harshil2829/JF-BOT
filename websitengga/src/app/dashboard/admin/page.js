import { ShieldCheck, UserCheck, Search } from 'lucide-react';

export default function AdminPage() {
  return (
    <>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <div>
          <h1 style={{ fontSize: '24px', margin: '0 0 5px 0' }}>Admin Management</h1>
          <p style={{ color: 'var(--text-muted)', margin: 0, fontSize: '14px' }}>Manage super-admin access and system logs.</p>
        </div>
        <button className="btn-primary" style={{ display: 'flex', gap: '8px', alignItems: 'center' }}><UserCheck size={16}/> Add Admin</button>
      </div>
      
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '10px' }}><ShieldCheck size={18} color="var(--success)"/> Super Admins</h3>
          <div style={{ background: '#222', padding: '8px 15px', borderRadius: '8px', display: 'flex', gap: '10px', alignItems: 'center', width: '200px' }}>
            <Search size={16} color="var(--text-muted)" />
            <input type="text" placeholder="Search..." style={{ background: 'transparent', border: 'none', color: 'white', outline: 'none', width: '100%', fontSize: '14px' }}/>
          </div>
        </div>

        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '14px' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--border)', color: 'var(--text-muted)' }}>
              <th style={{ padding: '15px 10px', fontWeight: 500 }}>Telegram ID</th>
              <th style={{ padding: '15px 10px', fontWeight: 500 }}>Role</th>
              <th style={{ padding: '15px 10px', fontWeight: 500, textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
              <td style={{ padding: '15px 10px', fontWeight: 600 }}>713606626 (Owner)</td>
              <td style={{ padding: '15px 10px' }}><span className="badge positive">Super Admin</span></td>
              <td style={{ padding: '15px 10px', textAlign: 'right' }}>
                <button style={{ background: 'transparent', border: '1px solid #333', color: 'white', padding: '6px 12px', borderRadius: '6px', cursor: 'not-allowed', opacity: 0.5 }}>Revoke</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </>
  );
}

"use client";

import { useState } from 'react';
import { Plus, Users, User, MessageCircle, Clock, Search, Download, X } from 'lucide-react';
import { addStaff } from '../actions';
import { useRouter } from 'next/navigation';

function StaffModal({ isOpen, onClose, onSave }) {
  const [name, setName] = useState('');
  const [telegramId, setTelegramId] = useState('');
  const [role, setRole] = useState('Support');

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({
      name,
      telegram_id: telegramId,
      role,
      chatsHandled: 0,
      status: 'Active'
    });
  };

  return (
    <div style={{
      position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
      background: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(6px)',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      zIndex: 9999, padding: '15px'
    }}>
      <div style={{
        background: '#1a1a2e', border: '1px solid #333',
        borderRadius: '16px', padding: '30px', width: '100%', maxWidth: '400px',
        boxShadow: '0 20px 60px rgba(0,0,0,0.5)'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '25px' }}>
          <h2 style={{ margin: 0, fontSize: '20px' }}>👤 Add Staff Member</h2>
          <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: '#aaa', cursor: 'pointer', padding: '5px' }}>
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', fontSize: '13px', color: '#aaa', marginBottom: '6px' }}>Staff Name</label>
            <input value={name} onChange={e => setName(e.target.value)} required
              placeholder="Enter name"
              style={{
                width: '100%', padding: '12px 14px', background: 'rgba(255,255,255,0.06)',
                border: '1px solid #333', borderRadius: '10px', color: 'white',
                fontSize: '14px', outline: 'none', boxSizing: 'border-box'
              }}
            />
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', fontSize: '13px', color: '#aaa', marginBottom: '6px' }}>Telegram ID</label>
            <input value={telegramId} onChange={e => setTelegramId(e.target.value)} required
              placeholder="e.g. 5626297359"
              style={{
                width: '100%', padding: '12px 14px', background: 'rgba(255,255,255,0.06)',
                border: '1px solid #333', borderRadius: '10px', color: 'white',
                fontSize: '14px', outline: 'none', boxSizing: 'border-box'
              }}
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', fontSize: '13px', color: '#aaa', marginBottom: '6px' }}>Role</label>
            <select value={role} onChange={e => setRole(e.target.value)}
              style={{
                width: '100%', padding: '12px 14px', background: 'rgba(255,255,255,0.06)',
                border: '1px solid #333', borderRadius: '10px', color: 'white',
                fontSize: '14px', outline: 'none', boxSizing: 'border-box'
              }}
            >
              <option value="Support" style={{ background: '#1a1a2e' }}>Support</option>
              <option value="Admin" style={{ background: '#1a1a2e' }}>Admin</option>
              <option value="Owner" style={{ background: '#1a1a2e' }}>Owner</option>
            </select>
          </div>

          <div style={{ display: 'flex', gap: '10px' }}>
            <button type="button" onClick={onClose} style={{
              flex: 1, padding: '12px', background: 'rgba(255,255,255,0.06)',
              border: '1px solid #333', borderRadius: '10px', color: '#aaa',
              fontSize: '14px', cursor: 'pointer'
            }}>Cancel</button>
            <button type="submit" className="btn-primary" style={{
              flex: 1, padding: '12px', borderRadius: '10px', fontSize: '14px',
              cursor: 'pointer', border: 'none', background: 'linear-gradient(135deg, #0072ff 0%, #00d2ff 100%)', color: 'white'
            }}>Add Staff</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function SupportClient({ initialStaff }) {
  const [staffList, setStaffList] = useState(initialStaff || []);
  const [modalOpen, setModalOpen] = useState(false);
  const router = useRouter();

  const handleSave = async (newStaff) => {
    await addStaff(newStaff);
    setStaffList([...staffList, newStaff]);
    setModalOpen(false);
    router.refresh();
  };

  return (
    <>
      <StaffModal 
        isOpen={modalOpen} 
        onClose={() => setModalOpen(false)} 
        onSave={handleSave} 
      />

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <div>
          <h1 style={{ fontSize: '24px', margin: '0 0 5px 0' }}>Staff & Support</h1>
          <p style={{ color: 'var(--text-muted)', margin: 0, fontSize: '14px' }}>Manage support staff and live chats</p>
        </div>
        <button onClick={() => setModalOpen(true)} className="btn-primary" style={{ display: 'flex', gap: '8px', alignItems: 'center', background: '#00d2ff', color: '#000', fontWeight: 'bold' }}>
          <Plus size={16}/> Add Staff
        </button>
      </div>
      
      {/* Top Stats */}
      <div className="mobile-grid-5" style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '15px', marginBottom: '20px' }}>
        <div className="card" style={{ position: 'relative', overflow: 'hidden' }}>
          <div style={{ position: 'absolute', right: '-20px', top: '-20px', width: '100px', height: '100px', background: 'rgba(0,210,255,0.05)', borderRadius: '50%' }}></div>
          <div style={{ background: 'rgba(0, 210, 255, 0.1)', width: '32px', height: '32px', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '15px' }}>
            <Users size={18} color="var(--primary)" />
          </div>
          <p style={{ margin: '0 0 5px 0', fontSize: '13px', color: 'var(--text-muted)' }}>Total Staff</p>
          <h2 style={{ margin: 0, fontSize: '24px' }}>{staffList.length}</h2>
        </div>
        
        <div className="card" style={{ position: 'relative', overflow: 'hidden' }}>
          <div style={{ position: 'absolute', right: '-20px', top: '-20px', width: '100px', height: '100px', background: 'rgba(0,230,118,0.05)', borderRadius: '50%' }}></div>
          <div style={{ background: 'rgba(0, 230, 118, 0.1)', width: '32px', height: '32px', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '15px' }}>
            <User size={18} color="var(--success)" />
          </div>
          <p style={{ margin: '0 0 5px 0', fontSize: '13px', color: 'var(--text-muted)' }}>Online Now</p>
          <h2 style={{ margin: 0, fontSize: '24px' }}>{Math.min(staffList.length, 1)}</h2>
        </div>

        <div className="card" style={{ position: 'relative', overflow: 'hidden' }}>
          <div style={{ position: 'absolute', right: '-20px', top: '-20px', width: '100px', height: '100px', background: 'rgba(41,121,255,0.05)', borderRadius: '50%' }}></div>
          <div style={{ background: 'rgba(41, 121, 255, 0.1)', width: '32px', height: '32px', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '15px' }}>
            <MessageCircle size={18} color="#2979ff" />
          </div>
          <p style={{ margin: '0 0 5px 0', fontSize: '13px', color: 'var(--text-muted)' }}>Active Chats</p>
          <h2 style={{ margin: 0, fontSize: '24px' }}>0</h2>
        </div>

        <div className="card" style={{ position: 'relative', overflow: 'hidden' }}>
          <div style={{ position: 'absolute', right: '-20px', top: '-20px', width: '100px', height: '100px', background: 'rgba(255,179,0,0.05)', borderRadius: '50%' }}></div>
          <div style={{ background: 'rgba(255, 179, 0, 0.1)', width: '32px', height: '32px', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '15px' }}>
            <Clock size={18} color="var(--warning)" />
          </div>
          <p style={{ margin: '0 0 5px 0', fontSize: '13px', color: 'var(--text-muted)' }}>Waiting</p>
          <h2 style={{ margin: 0, fontSize: '24px' }}>0</h2>
        </div>
      </div>

      <div className="mobile-grid-2" style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }}>
        {/* Staff Members List */}
        <div className="card">
          <h3 style={{ margin: '0 0 20px 0', fontSize: '16px' }}>Staff Members</h3>
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '20px' }}>
            <div style={{ flex: 1, background: '#111', border: '1px solid #333', borderRadius: '8px', display: 'flex', alignItems: 'center', padding: '10px 15px' }}>
              <Search size={16} color="var(--text-muted)" style={{ marginRight: '10px' }} />
              <input type="text" placeholder="Search staff..." style={{ background: 'transparent', border: 'none', color: 'white', outline: 'none', width: '100%', fontSize: '14px' }} />
            </div>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{staffList.length} results</span>
          </div>

          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '14px' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid #333', color: 'var(--text-muted)' }}>
                <th style={{ padding: '15px 10px', fontWeight: 500 }}>Staff Member</th>
                <th style={{ padding: '15px 10px', fontWeight: 500 }}>Role</th>
                <th style={{ padding: '15px 10px', fontWeight: 500 }}>Chats Handled</th>
                <th style={{ padding: '15px 10px', fontWeight: 500 }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {staffList.map((staff, i) => (
                <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                  <td style={{ padding: '15px 10px', fontWeight: 600 }}>{staff.name}</td>
                  <td style={{ padding: '15px 10px', color: 'var(--text-muted)' }}>{staff.role}</td>
                  <td style={{ padding: '15px 10px', color: 'var(--text-muted)' }}>{staff.chatsHandled}</td>
                  <td style={{ padding: '15px 10px' }}><span className="badge positive">{staff.status}</span></td>
                </tr>
              ))}
              {staffList.length === 0 && (
                <tr>
                  <td colSpan="4" style={{ padding: '40px 20px', textAlign: 'center', color: 'var(--text-muted)' }}>
                    No staff members
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Active Sessions Sidebar */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <h3 style={{ margin: 0, fontSize: '16px' }}>Active Sessions</h3>
            <button style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}><Download size={16}/></button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {[
              { id: '779928', status: 'pending' },
              { id: '132615', status: 'pending' },
              { id: '171690', status: 'pending' }
            ].map((session, idx) => (
              <div key={idx} style={{ background: '#111', borderRadius: '8px', padding: '15px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <p style={{ margin: '0 0 5px 0', fontSize: '14px', fontWeight: 600 }}>User #{session.id}</p>
                  <p style={{ margin: 0, fontSize: '12px', color: 'var(--text-muted)' }}>Invalid Date</p>
                </div>
                <span style={{ background: '#222', color: 'var(--text-muted)', padding: '4px 8px', borderRadius: '4px', fontSize: '11px' }}>{session.status}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}

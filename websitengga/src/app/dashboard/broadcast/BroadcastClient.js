"use client";

import { useState, useEffect } from 'react';
import { RefreshCw, Users, Send, Eye, User, Crown } from 'lucide-react';
import { sendBroadcast } from '../../actions';
import { useRouter } from 'next/navigation';

export default function BroadcastClient({ totalUsers, logs: initialLogs }) {
  const [message, setMessage] = useState('');
  const [target, setTarget] = useState('All Users');
  const [sending, setSending] = useState(false);
  const [logs, setLogs] = useState(initialLogs || []);
  const router = useRouter();

  // Poll for live updates every 1 second if any broadcast is running
  useEffect(() => {
    const hasRunning = logs.some(l => l.status === 'Running');
    if (!hasRunning) return;

    const interval = setInterval(async () => {
      try {
        const res = await fetch('/api/broadcast-logs');
        const data = await res.json();
        if (data.logs) {
          setLogs(data.logs);
        }
      } catch (e) { }
    }, 1000);

    return () => clearInterval(interval);
  }, [logs]);

  const handleSend = async () => {
    if (!message.trim()) return alert("Message is empty!");
    setSending(true);
    const res = await sendBroadcast(message, target);
    if (res.error) {
      alert(res.error);
    } else {
      setMessage('');
      // Optimistically add to UI to trigger polling
      setLogs(prev => [{
        message,
        target,
        date: new Date().toISOString(),
        totalTarget: totalUsers,
        success: 0,
        failed: 0,
        status: 'Running'
      }, ...prev]);
    }
    setSending(false);
  };

  const formatDate = (dateStr) => {
    const d = new Date(dateStr);
    return `${d.getDate()}/${d.getMonth() + 1}/${d.getFullYear()} ${d.getHours()}:${String(d.getMinutes()).padStart(2, '0')}`;
  };

  return (
    <>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <div>
          <h1 style={{ fontSize: '24px', margin: '0 0 5px 0' }}>Broadcast</h1>
          <p style={{ color: 'var(--text-muted)', margin: 0, fontSize: '14px' }}>Send messages to your users</p>
        </div>
        <button onClick={() => router.refresh()} style={{ background: 'transparent', border: '1px solid #333', color: 'white', padding: '8px 16px', borderRadius: '8px', display: 'flex', gap: '8px', alignItems: 'center', cursor: 'pointer' }}>
          <RefreshCw size={16} /> Refresh
        </button>
      </div>
      
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* Select Target */}
          <div className="card">
            <h3 style={{ margin: '0 0 20px 0', fontSize: '16px' }}>Select Target</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '15px' }}>
              <div onClick={() => setTarget('All Users')} style={{ background: target === 'All Users' ? 'rgba(0, 210, 255, 0.05)' : '#111', border: `1px solid ${target === 'All Users' ? 'var(--primary)' : '#333'}`, borderRadius: '12px', padding: '15px', cursor: 'pointer' }}>
                <Users size={20} color={target === 'All Users' ? 'var(--primary)' : 'var(--text-muted)'} style={{ marginBottom: '10px' }} />
                <p style={{ margin: '0 0 5px 0', fontSize: '14px', fontWeight: 600 }}>All Users</p>
                <p style={{ margin: 0, fontSize: '12px', color: target === 'All Users' ? 'var(--primary)' : 'var(--text-muted)' }}>{totalUsers.toLocaleString()} users</p>
              </div>
              <div style={{ background: '#111', border: '1px solid #333', borderRadius: '12px', padding: '15px', opacity: 0.5 }}>
                <User size={20} color="var(--text-muted)" style={{ marginBottom: '10px' }} />
                <p style={{ margin: '0 0 5px 0', fontSize: '14px', fontWeight: 600 }}>Active Users</p>
                <p style={{ margin: 0, fontSize: '12px', color: 'var(--text-muted)' }}>Coming soon</p>
              </div>
              <div style={{ background: '#111', border: '1px solid #333', borderRadius: '12px', padding: '15px', opacity: 0.5 }}>
                <Crown size={20} color="var(--text-muted)" style={{ marginBottom: '10px' }} />
                <p style={{ margin: '0 0 5px 0', fontSize: '14px', fontWeight: 600 }}>VIP Users</p>
                <p style={{ margin: 0, fontSize: '12px', color: 'var(--text-muted)' }}>Coming soon</p>
              </div>
            </div>
          </div>

          {/* Compose Message */}
          <div className="card">
            <h3 style={{ margin: '0 0 20px 0', fontSize: '16px' }}>Compose Message</h3>
            
            <div style={{ border: '1px solid #333', borderRadius: '8px', overflow: 'hidden' }}>
              <div style={{ background: '#111', padding: '10px 15px', borderBottom: '1px solid #333', display: 'flex', gap: '15px' }}>
                <span style={{ color: 'var(--text-muted)', cursor: 'pointer', fontWeight: 'bold' }}>B</span>
                <span style={{ color: 'var(--text-muted)', cursor: 'pointer', fontStyle: 'italic' }}>I</span>
                <span style={{ color: 'var(--text-muted)', cursor: 'pointer', textDecoration: 'line-through' }}>S</span>
              </div>
              <textarea 
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Write your message here... Use <b>bold</b>, <i>italic</i>, and <a href='url'>links</a> for HTML formatting." 
                style={{ width: '100%', minHeight: '200px', background: 'transparent', border: 'none', color: 'white', padding: '15px', outline: 'none', resize: 'vertical', fontSize: '14px' }}
              ></textarea>
            </div>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '20px' }}>
              <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{message.length} characters · Sending to {totalUsers.toLocaleString()} recipients</span>
              <div style={{ display: 'flex', gap: '10px' }}>
                <button onClick={handleSend} disabled={sending} className="btn-primary" style={{ display: 'flex', gap: '8px', alignItems: 'center', opacity: sending ? 0.7 : 1 }}>
                  <Send size={16} /> {sending ? 'Sending...' : 'Send Broadcast'}
                </button>
              </div>
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* Recent Broadcasts */}
          <div className="card">
            <h3 style={{ margin: '0 0 20px 0', fontSize: '16px' }}>Recent Broadcasts</h3>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              {logs.length === 0 && (
                <p style={{ color: 'var(--text-muted)', fontSize: '13px' }}>No broadcasts sent yet.</p>
              )}
              {logs.map((log, idx) => (
                <div key={idx} style={{ background: '#111', padding: '15px', borderRadius: '8px', border: '1px solid #222' }}>
                  <p style={{ margin: '0 0 5px 0', fontSize: '13px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{log.message}</p>
                  <p style={{ margin: '0 0 10px 0', fontSize: '11px', color: 'var(--text-muted)' }}>{log.target} · {formatDate(log.date)}</p>
                  <div style={{ display: 'flex', gap: '15px', fontSize: '12px' }}>
                    <span style={{ color: 'var(--success)' }}>✓ {log.success}</span>
                    <span style={{ color: 'var(--danger)' }}>✗ {log.failed}</span>
                    <span style={{ color: log.status === 'Completed' ? 'var(--success)' : 'var(--warning)' }}>● {log.status}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Tips */}
          <div className="card">
            <h3 style={{ margin: '0 0 15px 0', fontSize: '16px' }}>Tips</h3>
            <ul style={{ margin: 0, padding: '0 0 0 20px', color: 'var(--text-muted)', fontSize: '13px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <li>Use &lt;b&gt;bold text&lt;/b&gt;</li>
              <li>Use &lt;i&gt;italic text&lt;/i&gt;</li>
              <li>Use &lt;a href="url"&gt;link&lt;/a&gt;</li>
            </ul>
          </div>
        </div>
      </div>
    </>
  );
}

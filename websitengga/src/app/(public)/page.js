"use client";

import { useEffect, useRef, useState } from 'react';
import Link from 'next/link';
import './landing.css';
import { 
  Rocket, Book, Shield, Database, Lock, UserCheck, 
  Key, Zap, Users, CheckCircle2, Code, Globe, 
  Activity, Terminal, Cpu, HardDrive, RefreshCw, 
  ChevronDown, ChevronUp, DollarSign, Server, Bell, 
  ArrowRight, Check, Play, Settings
} from 'lucide-react';

// Scroll Reveal Wrapper (Compositor and IntersectionObserver performance optimized)
function Reveal({ children }) {
  const ref = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target); // Unobserve to avoid repeating calculations
          }
        });
      },
      { threshold: 0.05 }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => {
      if (ref.current) observer.unobserve(ref.current);
    };
  }, []);

  return (
    <div ref={ref} className="reveal">
      {children}
    </div>
  );
}

// Interactive FAQ Accordion Component
function FAQItem({ question, answer }) {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <div style={{
      background: 'rgba(255, 255, 255, 0.02)',
      border: '1px solid rgba(255, 255, 255, 0.05)',
      borderRadius: '12px',
      marginBottom: '15px',
      overflow: 'hidden',
      transition: 'all 0.3s cubic-bezier(0.16, 1, 0.3, 1)'
    }}>
      <button 
        onClick={() => setIsOpen(!isOpen)}
        style={{
          width: '100%',
          padding: '22px 30px',
          background: 'none',
          border: 'none',
          color: '#fff',
          textAlign: 'left',
          fontSize: '16px',
          fontWeight: 'bold',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          cursor: 'pointer',
        }}
      >
        <span style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ color: '#00e599', fontSize: '18px' }}>?</span>
          {question}
        </span>
        {isOpen ? <ChevronUp size={18} color="#00e599" /> : <ChevronDown size={18} color="#888" />}
      </button>
      <div style={{
        maxHeight: isOpen ? '250px' : '0px',
        opacity: isOpen ? 1 : 0,
        transition: 'all 0.35s cubic-bezier(0.16, 1, 0.3, 1)',
        padding: isOpen ? '0px 30px 22px 30px' : '0px 30px',
        color: '#a0a0b0',
        fontSize: '14px',
        lineHeight: '1.6'
      }}>
        {answer}
      </div>
    </div>
  );
}

// Isolated Dashboard Mockup Component (prevents main page re-renders)
function DashboardConsoleMockup() {
  const [activeTab, setActiveTab] = useState('overview');
  const [telemetry, setTelemetry] = useState({
    activeUsers: 8421,
    attacksBlocked: 1482903,
    avgLatency: 14.2,
    cpuUsage: 42
  });

  const [logs, setLogs] = useState([
    { id: 1, time: '19:19:01', type: 'SECURE', msg: 'JF Secure link node US-West initialized.' },
    { id: 2, time: '19:19:12', type: 'AUTH', msg: 'Verification success: User dev_admin_4.' },
    { id: 3, time: '19:19:18', type: 'HWID', msg: 'HWID Lock match verified. 0.04ms validation.' },
    { id: 4, time: '19:19:24', type: 'CRYPTO', msg: 'Session verified. Bot client session handshake OK.' },
  ]);

  const pathRef = useRef(null);
  const fillPathRef = useRef(null);

  // CPU and other numbers ticking interval
  useEffect(() => {
    const telemetryInterval = setInterval(() => {
      setTelemetry(prev => ({
        activeUsers: prev.activeUsers + Math.floor(Math.random() * 5) - 2,
        attacksBlocked: prev.attacksBlocked + Math.floor(Math.random() * 3),
        avgLatency: Number((13.5 + Math.random() * 1.5).toFixed(1)),
        cpuUsage: Math.floor(38 + Math.random() * 10)
      }));
    }, 2500);

    const logTemplates = [
      { type: 'SECURE', msg: 'Inbound bot verification token verified.' },
      { type: 'AUTH', msg: 'Role check complete: Reseller voucher authenticated.' },
      { type: 'HWID', msg: 'HWID configuration check: Client profiles match.' },
      { type: 'AUDIT', msg: 'Voucher key claims logged: JF-VIP-M6.' },
      { type: 'SECURE', msg: 'Spam throttling limits bypassed cleanly.' },
      { type: 'CRYPTO', msg: 'Session code decrypted securely.' }
    ];

    const logsInterval = setInterval(() => {
      const template = logTemplates[Math.floor(Math.random() * logTemplates.length)];
      const now = new Date();
      const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
      
      setLogs(prev => [
        ...prev.slice(1),
        { id: Date.now(), time: timeStr, type: template.type, msg: template.msg }
      ]);
    }, 3800);

    return () => {
      clearInterval(telemetryInterval);
      clearInterval(logsInterval);
    };
  }, []);

  // Butter-smooth, zero-lag dynamic SVG path wiggling via direct DOM mutations
  useEffect(() => {
    let animId;
    const animate = () => {
      const now = Date.now();
      const p1 = 20 + Math.sin(now / 1000) * 8;
      const p2 = 45 + Math.cos(now / 1500) * 12;
      const p3 = 30 + Math.sin(now / 850) * 8;
      const p4 = 25 + Math.sin(now / 550) * 7;
      
      const pathD = `M0 45 Q 40 ${p1} 80 ${p2} T 160 ${p3} T 240 45 T 300 ${p4}`;
      const fillD = `${pathD} L 300 80 L 0 80 Z`;
      
      if (pathRef.current) pathRef.current.setAttribute('d', pathD);
      if (fillPathRef.current) fillPathRef.current.setAttribute('d', fillD);
      
      animId = requestAnimationFrame(animate);
    };
    animId = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animId);
  }, []);

  return (
    <div className="console-wrapper" style={{
      width: '100%',
      maxWidth: '1000px',
      margin: '40px auto 0 auto',
      zIndex: 10,
      position: 'relative'
    }}>
      <div className="unfolding-console" style={{
        width: '100%',
        background: 'rgba(8, 8, 12, 0.75)',
        border: '1px solid rgba(255, 255, 255, 0.08)',
        borderRadius: '16px',
        overflow: 'hidden',
        backdropFilter: 'blur(24px)',
        WebkitBackdropFilter: 'blur(24px)',
        position: 'relative'
      }}>
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '15px 25px',
        background: 'rgba(255,255,255,0.03)',
        borderBottom: '1px solid rgba(255,255,255,0.08)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{ display: 'flex', gap: '6px' }}>
            <div style={{ width: '11px', height: '11px', borderRadius: '50%', background: '#ff5f56' }}></div>
            <div style={{ width: '11px', height: '11px', borderRadius: '50%', background: '#ffbd2e' }}></div>
            <div style={{ width: '11px', height: '11px', borderRadius: '50%', background: '#27c93f' }}></div>
          </div>
          <span style={{ fontSize: '11px', color: '#666', fontFamily: 'monospace', marginLeft: '10px', letterSpacing: '1px' }}>JF_CONSOLE_V2</span>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '11px', color: '#00e599', fontWeight: 'bold' }}>
            <span style={{ display: 'inline-block', width: '6px', height: '6px', borderRadius: '50%', background: '#00e599', animation: 'pulse-glow 2s infinite' }}></span>
            SECURE LINK: ACTIVE
          </div>
          <div style={{ fontSize: '11px', color: '#778' }}>
            PING: <strong style={{ color: '#fff' }}>{telemetry.avgLatency}ms</strong>
          </div>
        </div>
      </div>

      {/* Grid Content */}
      <div style={{ display: 'grid', gridTemplateColumns: '220px 1fr', minHeight: '440px', background: 'rgba(5, 5, 8, 0.4)' }}>
        {/* Sidebar */}
        <div style={{ borderRight: '1px solid rgba(255,255,255,0.06)', padding: '25px 15px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <div style={{ fontSize: '9px', color: '#556', fontWeight: 'bold', paddingLeft: '12px', letterSpacing: '1.5px', marginBottom: '10px' }}>BOT CONTROL</div>
          
          <button onClick={() => setActiveTab('overview')} style={sidebarBtnStyle(activeTab === 'overview')}>
            <Activity size={15} /> Bot Overview
          </button>
          <button onClick={() => setActiveTab('keys')} style={sidebarBtnStyle(activeTab === 'keys')}>
            <Key size={15} /> Key Management
          </button>
          <button onClick={() => setActiveTab('security')} style={sidebarBtnStyle(activeTab === 'security')}>
            <Shield size={15} /> Client Protection
          </button>
          <button onClick={() => setActiveTab('logs')} style={sidebarBtnStyle(activeTab === 'logs')}>
            <Terminal size={15} /> Activity Feed
          </button>

          <div style={{ fontSize: '9px', color: '#556', fontWeight: 'bold', paddingLeft: '12px', letterSpacing: '1.5px', marginTop: '25px', marginBottom: '10px' }}>INTEGRATION</div>
          <button onClick={() => setActiveTab('api')} style={sidebarBtnStyle(activeTab === 'api')}>
            <Code size={15} /> Bot API Keys
          </button>
          <button onClick={() => setActiveTab('settings')} style={sidebarBtnStyle(activeTab === 'settings')}>
            <Settings size={15} /> Config Panel
          </button>
        </div>

        {/* Content */}
        <div style={{ padding: '30px' }}>
          {activeTab === 'overview' && (
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '25px' }}>
                <div>
                  <h4 style={{ margin: 0, fontSize: '18px', fontWeight: 'bold' }}>Sovereign Bot Telemetry</h4>
                  <p style={{ margin: '3px 0 0 0', fontSize: '12px', color: '#667' }}>Real-time verification handshakes and loads</p>
                </div>
                <span style={{ fontSize: '10px', background: 'rgba(0, 229, 153, 0.1)', color: '#00e599', border: '1px solid rgba(0, 229, 153, 0.2)', padding: '4px 10px', borderRadius: '4px', fontWeight: 'bold' }}>
                  NODE: CENTRAL CLUSTER
                </span>
              </div>

              {/* Stats Cards */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '15px', marginBottom: '25px' }}>
                <div style={{ background: 'rgba(255,255,255,0.01)', border: '1px solid rgba(255,255,255,0.04)', padding: '15px 20px', borderRadius: '10px' }}>
                  <div style={{ fontSize: '11px', color: '#666', marginBottom: '5px' }}>BOT CLIENT SESSIONS</div>
                  <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#fff', fontFamily: 'monospace' }}>{telemetry.activeUsers.toLocaleString('en-US')}</div>
                </div>
                <div style={{ background: 'rgba(255,255,255,0.01)', border: '1px solid rgba(255,255,255,0.04)', padding: '15px 20px', borderRadius: '10px' }}>
                  <div style={{ fontSize: '11px', color: '#666', marginBottom: '5px' }}>CRACKS MITIGATED</div>
                  <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#ff5555', fontFamily: 'monospace' }}>{telemetry.attacksBlocked.toLocaleString('en-US')}</div>
                </div>
                <div style={{ background: 'rgba(255,255,255,0.01)', border: '1px solid rgba(255,255,255,0.04)', padding: '15px 20px', borderRadius: '10px' }}>
                  <div style={{ fontSize: '11px', color: '#666', marginBottom: '5px' }}>BOT ENGINE CPU</div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '6px' }}>
                    <div style={{ flex: 1, height: '6px', background: 'rgba(255,255,255,0.08)', borderRadius: '3px', overflow: 'hidden' }}>
                      <div style={{ width: `${telemetry.cpuUsage}%`, height: '100%', background: 'linear-gradient(90deg, #8b8bff, #00e599)', borderRadius: '3px' }}></div>
                    </div>
                    <span style={{ fontSize: '13px', fontFamily: 'monospace', fontWeight: 'bold' }}>{telemetry.cpuUsage}%</span>
                  </div>
                </div>
              </div>

              {/* Chart & Mini log */}
              <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '20px' }}>
                <div style={{ background: 'rgba(0,0,0,0.2)', border: '1px solid rgba(255,255,255,0.04)', padding: '15px', borderRadius: '10px', height: '150px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: '#556' }}>
                    <span>VERIFICATION FLOW PULSE</span>
                    <span style={{ color: '#00e599' }}>Live Telemetry</span>
                  </div>
                  <svg viewBox="0 0 300 80" style={{ width: '100%', height: '80px', overflow: 'visible' }}>
                    <defs>
                      <linearGradient id="chartGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#00e599" stopOpacity="0.2"/>
                        <stop offset="100%" stopColor="#00e599" stopOpacity="0"/>
                      </linearGradient>
                    </defs>
                    <path 
                      ref={pathRef}
                      d="M0 45 Q 40 25 80 40 T 160 35 T 240 45 T 300 30" 
                      fill="none" 
                      stroke="#00e599" 
                      strokeWidth="2"
                    />
                    <path 
                      ref={fillPathRef}
                      d="M0 45 Q 40 25 80 40 T 160 35 T 240 45 T 300 30 L 300 80 L 0 80 Z" 
                      fill="url(#chartGrad)"
                    />
                  </svg>
                </div>

                <div style={{ background: 'rgba(0,0,0,0.2)', border: '1px solid rgba(255,255,255,0.04)', padding: '15px', borderRadius: '10px', height: '150px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                  <div style={{ fontSize: '11px', color: '#556', marginBottom: '8px' }}>LATEST VERIFICATION EVENT</div>
                  <div style={{ fontFamily: 'monospace', fontSize: '11px', display: 'flex', flexDirection: 'column', gap: '6px', overflowY: 'hidden' }}>
                    {logs.slice(-3).map(log => (
                      <div key={log.id} style={{ display: 'flex', gap: '8px' }}>
                        <span style={{ color: '#445' }}>[{log.time}]</span>
                        <span style={{ color: log.type === 'SECURE' ? '#00e599' : log.type === 'AUTH' ? '#8b8bff' : '#ffb84d', fontWeight: 'bold' }}>{log.type}</span>
                        <span style={{ color: '#ccc', textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap' }}>{log.msg}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab !== 'overview' && (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '300px', textAlign: 'center', color: '#556' }}>
              <Cpu size={40} style={{ marginBottom: '15px', color: '#00e599' }} />
              <div style={{ fontSize: '14px', fontWeight: 'bold', color: '#ccc' }}>Active Module Interface: {activeTab.toUpperCase()}</div>
              <p style={{ fontSize: '12px', maxWidth: '300px', margin: '5px 0 0 0' }}>Linking direct bot configuration database parameters. Enter secure console routing headers to manage options.</p>
            </div>
          )}
        </div>
      </div>
    </div>
    </div>
  );
}

// Helper styling generators for layout cleaniness
function sidebarBtnStyle(isActive) {
  return {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    width: '100%',
    padding: '10px 14px',
    background: isActive ? 'rgba(0, 229, 153, 0.08)' : 'transparent',
    border: 'none',
    color: isActive ? '#00e599' : '#888',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '12px',
    fontWeight: 'bold',
    textAlign: 'left',
    transition: 'all 0.2s ease',
    textShadow: isActive ? '0 0 10px rgba(0, 229, 153, 0.2)' : 'none'
  };
}

// Isolated Telemetry Section Component (prevents parent page re-renders)
function TelemetryMetricsBlock() {
  const [telemetry, setTelemetry] = useState({
    avgLatency: 14.2,
    activeUsers: 8420
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setTelemetry({
        avgLatency: Number((13.5 + Math.random() * 1.5).toFixed(1)),
        activeUsers: 8410 + Math.floor(Math.random() * 20)
      });
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '50px', alignItems: 'center' }}>
        <div>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', border: '1px solid rgba(255, 184, 77, 0.3)', background: 'rgba(255, 184, 77, 0.05)', color: '#ffb84d', padding: '6px 16px', borderRadius: '20px', fontSize: '10px', fontWeight: 'bold', letterSpacing: '1px', marginBottom: '25px' }}>
            <Activity size={12} /> BOT TELEMETRY
          </div>
          <h2 style={{ fontSize: '50px', fontWeight: '900', margin: '0 0 20px 0', letterSpacing: '-1.5px', lineHeight: '1.1' }}>
            Sovereign bot gateway.
          </h2>
          <p style={{ fontSize: '17px', color: '#888', lineHeight: '1.7', marginBottom: '35px' }}>
            Verify execution requests immediately. Trace global bot loads, CPU cycles, and average handshake delays directly from the staff dashboard.
          </p>
          
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            <div style={{ borderLeft: '3px solid #00e599', paddingLeft: '15px' }}>
              <div style={{ fontSize: '11px', color: '#666', fontWeight: 'bold', letterSpacing: '1px' }}>BOT GATEWAY PING</div>
              <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#fff', margin: '5px 0' }}>{telemetry.avgLatency}ms</div>
              <p style={{ fontSize: '11px', color: '#444', margin: 0 }}>High-speed validation relays</p>
            </div>
            <div style={{ borderLeft: '3px solid #8b8bff', paddingLeft: '15px' }}>
              <div style={{ fontSize: '11px', color: '#666', fontWeight: 'bold', letterSpacing: '1px' }}>HANDSHAKE CAPACITY</div>
              <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#fff', margin: '5px 0' }}>99.998%</div>
              <p style={{ fontSize: '11px', color: '#444', margin: 0 }}>Active validation replicas</p>
            </div>
          </div>
        </div>

        {/* Graphical Live Stats */}
        <div style={{
          background: 'rgba(10, 10, 15, 0.65)',
          border: '1px solid rgba(255, 255, 255, 0.05)',
          borderRadius: '20px',
          padding: '40px',
          backdropFilter: 'blur(10px)',
          WebkitBackdropFilter: 'blur(10px)'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Server size={16} color="#00e599" />
              <span style={{ fontSize: '13px', fontWeight: 'bold', letterSpacing: '1px' }}>JF BOT CORE SERVER 7</span>
            </div>
            <span style={{ fontSize: '9px', background: 'rgba(0, 229, 153, 0.1)', color: '#00e599', padding: '3px 8px', borderRadius: '4px', fontWeight: 'bold' }}>ACTIVE</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '8px' }}>
                <span style={{ color: '#ccc' }}>Client Session Bandwidth</span>
                <span style={{ color: '#00e599', fontFamily: 'monospace' }}>{(telemetry.activeUsers * 1.2).toFixed(0)} kbps</span>
              </div>
              <div style={{ height: '6px', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '3px', overflow: 'hidden' }}>
                <div style={{ width: '75%', height: '100%', background: '#00e599' }}></div>
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '8px' }}>
                <span style={{ color: '#ccc' }}>Encryption Verification Speed</span>
                <span style={{ color: '#8b8bff', fontFamily: 'monospace' }}>82.1 GigaHash/s</span>
              </div>
              <div style={{ height: '6px', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '3px', overflow: 'hidden' }}>
                <div style={{ width: '85%', height: '100%', background: '#8b8bff' }}></div>
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '8px' }}>
                <span style={{ color: '#ccc' }}>Active Node Synchronization</span>
                <span style={{ color: '#ffb84d', fontFamily: 'monospace' }}>Sync Verified (0ms delay)</span>
              </div>
              <div style={{ height: '6px', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '3px', overflow: 'hidden' }}>
                <div style={{ width: '100%', height: '100%', background: '#ffb84d' }}></div>
              </div>
            </div>
          </div>

          <div style={{ borderTop: '1px solid rgba(255, 255, 255, 0.05)', marginTop: '30px', paddingTop: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '11px', color: '#666' }}>
              <Bell size={12} color="#00e599" /> System Status: Normal Operations
            </div>
            <Link href="/login" style={{ fontSize: '12px', color: '#00e599', textDecoration: 'none', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '4px' }}>
              Manage Bot Node <ArrowRight size={12} />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

// Isolated Audit Terminal Component
function AuditTerminalStream() {
  const [logs, setLogs] = useState([
    { id: 1, time: '19:19:01', type: 'SECURE', msg: 'JF Secure link node US-West initialized.' },
    { id: 2, time: '19:19:12', type: 'AUTH', msg: 'Verification success: User dev_admin_4.' },
    { id: 3, time: '19:19:18', type: 'HWID', msg: 'HWID Lock match verified. 0.04ms validation.' },
    { id: 4, time: '19:19:24', type: 'CRYPTO', msg: 'Session verified. Bot client session handshake OK.' },
  ]);

  useEffect(() => {
    const logTemplates = [
      { type: 'SECURE', msg: 'Inbound bot verification token verified.' },
      { type: 'AUTH', msg: 'Role check complete: Reseller voucher authenticated.' },
      { type: 'HWID', msg: 'HWID configuration check: Client profiles match.' },
      { type: 'AUDIT', msg: 'Voucher key claims logged: JF-VIP-M6.' },
      { type: 'SECURE', msg: 'Spam throttling limits bypassed cleanly.' },
      { type: 'CRYPTO', msg: 'Session code decrypted securely.' }
    ];

    const interval = setInterval(() => {
      const template = logTemplates[Math.floor(Math.random() * logTemplates.length)];
      const now = new Date();
      const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
      
      setLogs(prev => [
        ...prev.slice(1),
        { id: Date.now(), time: timeStr, type: template.type, msg: template.msg }
      ]);
    }, 4000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.2fr', gap: '50px', alignItems: 'center' }}>
      <div style={{
        background: 'rgba(4, 4, 6, 0.85)',
        border: '1px solid rgba(0, 229, 153, 0.25)',
        borderRadius: '16px',
        padding: '30px',
        boxShadow: '0 20px 40px rgba(0,0,0,0.7), inset 0 0 20px rgba(0, 229, 153, 0.03)',
        position: 'relative'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid rgba(255,255,255,0.06)', paddingBottom: '15px', marginBottom: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#00e599', animation: 'pulse-glow 1.5s infinite' }}></div>
            <span style={{ fontSize: '11px', fontFamily: 'monospace', letterSpacing: '1px', color: '#00e599', fontWeight: 'bold' }}>SECURE VERIFICATION FEED</span>
          </div>
          <span style={{ fontSize: '10px', color: '#445', fontFamily: 'monospace' }}>SECURE CHANNEL</span>
        </div>

        <div className="cyber-terminal" style={{
          padding: '20px',
          borderRadius: '8px',
          height: '240px',
          overflowY: 'hidden',
          display: 'flex',
          flexDirection: 'column',
          gap: '12px',
          fontSize: '12px',
          lineHeight: '1.5'
        }}>
          {logs.map((log) => (
            <div key={log.id} style={{ display: 'flex', gap: '12px', fontFamily: 'monospace' }}>
              <span style={{ color: '#444' }}>{log.time}</span>
              <span style={{
                color: log.type === 'SECURE' ? '#00e599' : log.type === 'AUTH' ? '#8b8bff' : log.type === 'HWID' ? '#ffb84d' : '#ff5f56',
                fontWeight: 'bold',
                minWidth: '55px'
              }}>[{log.type}]</span>
              <span style={{ color: '#ddd' }}>{log.msg}</span>
            </div>
          ))}
        </div>
      </div>

      <div>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', border: '1px solid rgba(0, 229, 153, 0.3)', background: 'rgba(0, 229, 153, 0.05)', color: '#00e599', padding: '6px 16px', borderRadius: '20px', fontSize: '10px', fontWeight: 'bold', letterSpacing: '1px', marginBottom: '25px' }}>
          <Terminal size={12} /> AUDIT SYSTEM
        </div>
        <h2 style={{ fontSize: '50px', fontWeight: '900', margin: '0 0 20px 0', letterSpacing: '-1.5px', lineHeight: '1.1' }}>
          Tamper-proof event logs.
        </h2>
        <p style={{ fontSize: '17px', color: '#888', lineHeight: '1.7', marginBottom: '20px' }}>
          The panel validates and archives client actions using encrypted verify signatures, generating immutable event histories.
        </p>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
            <CheckCircle2 size={18} color="#00e599" style={{ marginTop: '2px' }} />
            <div>
              <strong style={{ color: '#fff' }}>Secure Activity Recording</strong>
              <p style={{ margin: '2px 0 0 0', fontSize: '13px', color: '#888' }}>Every generated key, product creation, or ban trigger is stamped and logged.</p>
            </div>
          </div>
          <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
            <CheckCircle2 size={18} color="#00e599" style={{ marginTop: '2px' }} />
            <div>
              <strong style={{ color: '#fff' }}>Instant Session Revocations</strong>
              <p style={{ margin: '2px 0 0 0', fontSize: '13px', color: '#888' }}>Terminate sessions dynamically across all edge relays with immediate key cancellation.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// MAIN PAGE
export default function LandingPage() {
  return (
    <div style={{
      minHeight: '100vh',
      color: '#ffffff',
      fontFamily: 'var(--font-geist-sans), sans-serif',
      display: 'flex',
      flexDirection: 'column',
      position: 'relative',
      overflowX: 'hidden'
    }}>
      {/* Scroll Progress Bar */}
      <div className="scroll-progress" />
      {/* Universal Deep Space Mesh Background */}
      <div className="bg-mesh">
        <div className="bg-grid"></div>
        <div className="scanline"></div>
        
        {/* Falling Cyber Matrix Columns - DENSE LAYERING */}
        <div className="cyber-column" style={{ left: '3%', height: '320px', animationDelay: '0s', animationDuration: '14s' }}></div>
        <div className="cyber-column cyber-col-purple" style={{ left: '8%', height: '240px', animationDelay: '3s', animationDuration: '11s' }}></div>
        <div className="cyber-column" style={{ left: '14%', height: '400px', animationDelay: '1s', animationDuration: '18s' }}></div>
        <div className="cyber-column cyber-col-orange" style={{ left: '20%', height: '280px', animationDelay: '5s', animationDuration: '13s' }}></div>
        <div className="cyber-column" style={{ left: '26%', height: '360px', animationDelay: '2s', animationDuration: '15s' }}></div>
        <div className="cyber-column cyber-col-purple" style={{ left: '32%', height: '300px', animationDelay: '7s', animationDuration: '12s' }}></div>
        <div className="cyber-column" style={{ left: '38%', height: '420px', animationDelay: '4s', animationDuration: '19s' }}></div>
        <div className="cyber-column cyber-col-orange" style={{ left: '44%', height: '260px', animationDelay: '1s', animationDuration: '10s' }}></div>
        <div className="cyber-column" style={{ left: '50%', height: '350px', animationDelay: '6s', animationDuration: '16s' }}></div>
        <div className="cyber-column cyber-col-purple" style={{ left: '56%', height: '290px', animationDelay: '2s', animationDuration: '12s' }}></div>
        <div className="cyber-column" style={{ left: '62%', height: '380px', animationDelay: '8s', animationDuration: '17s' }}></div>
        <div className="cyber-column cyber-col-orange" style={{ left: '68%', height: '280px', animationDelay: '3s', animationDuration: '13s' }}></div>
        <div className="cyber-column" style={{ left: '74%', height: '410px', animationDelay: '5s', animationDuration: '18s' }}></div>
        <div className="cyber-column cyber-col-purple" style={{ left: '80%', height: '320px', animationDelay: '0s', animationDuration: '14s' }}></div>
        <div className="cyber-column" style={{ left: '86%', height: '370px', animationDelay: '4s', animationDuration: '15s' }}></div>
        <div className="cyber-column cyber-col-orange" style={{ left: '92%', height: '250px', animationDelay: '7s', animationDuration: '11s' }}></div>
        <div className="cyber-column" style={{ left: '97%', height: '390px', animationDelay: '2s', animationDuration: '17s' }}></div>

        {/* Floating Space Particles - GLOWING FIELDS */}
        <div style={{ position: 'absolute', top: '8%', left: '15%', width: '5px', height: '5px', backgroundColor: '#00e599', borderRadius: '50%', boxShadow: '0 0 15px #00e599', pointerEvents: 'none' }}></div>
        <div style={{ position: 'absolute', top: '22%', right: '25%', width: '4px', height: '4px', backgroundColor: '#8b8bff', borderRadius: '50%', boxShadow: '0 0 12px #8b8bff', pointerEvents: 'none' }}></div>
        <div style={{ position: 'absolute', top: '35%', left: '8%', width: '6px', height: '6px', backgroundColor: '#ffb84d', borderRadius: '50%', boxShadow: '0 0 15px #ffb84d', pointerEvents: 'none' }}></div>
        <div style={{ position: 'absolute', top: '48%', right: '12%', width: '4px', height: '4px', backgroundColor: '#00e599', borderRadius: '50%', boxShadow: '0 0 12px #00e599', pointerEvents: 'none' }}></div>
        <div style={{ position: 'absolute', top: '62%', left: '18%', width: '5px', height: '5px', backgroundColor: '#8b8bff', borderRadius: '50%', boxShadow: '0 0 12px #8b8bff', pointerEvents: 'none' }}></div>
        <div style={{ position: 'absolute', top: '75%', right: '35%', width: '6px', height: '6px', backgroundColor: '#ffb84d', borderRadius: '50%', boxShadow: '0 0 15px #ffb84d', pointerEvents: 'none' }}></div>
        <div style={{ position: 'absolute', bottom: '15%', left: '5%', width: '4px', height: '4px', backgroundColor: '#00e599', borderRadius: '50%', boxShadow: '0 0 12px #00e599', pointerEvents: 'none' }}></div>
        <div style={{ position: 'absolute', bottom: '25%', right: '8%', width: '5px', height: '5px', backgroundColor: '#8b8bff', borderRadius: '50%', boxShadow: '0 0 12px #8b8bff', pointerEvents: 'none' }}></div>
        <div style={{ position: 'absolute', bottom: '38%', left: '28%', width: '4px', height: '4px', backgroundColor: '#ffb84d', borderRadius: '50%', boxShadow: '0 0 12px #ffb84d', pointerEvents: 'none' }}></div>

        {/* Floating Aesthetic 3D & HUD Objects from Screenshot */}
        <div className="float-pill float-elem" style={{ top: '25%', left: '4%', zIndex: 1 }}></div>
        <div className="float-pill float-elem-delay-2" style={{ top: '55%', right: '5%', zIndex: 1, filter: 'hue-rotate(240deg)' }}></div>
        <div className="float-glass-rect float-elem-delay-1" style={{ top: '18%', right: '8%', zIndex: 1 }}></div>
        <div className="float-glass-square float-elem-delay-2" style={{ bottom: '22%', left: '10%', zIndex: 1 }}></div>
        <div className="float-glass-square float-elem" style={{ top: '65%', left: '42%', zIndex: 1, width: '45px', height: '45px', opacity: 0.7 }}></div>
        <div className="float-circle-hud" style={{ bottom: '15%', right: '12%', zIndex: 1 }}></div>
        <div className="float-circle-hud float-elem-delay-1" style={{ top: '40%', left: '2%', zIndex: 1, width: '60px', height: '60px', opacity: 0.6 }}></div>

        {/* Cyber Crosshairs - Grid Intersection Aesthetics */}
        <div className="float-crosshair float-elem" style={{ top: '10%', left: '18%' }}></div>
        <div className="float-crosshair float-crosshair-purple float-elem-delay-1" style={{ top: '45%', left: '6%' }}></div>
        <div className="float-crosshair float-crosshair-orange float-elem-delay-2" style={{ top: '25%', right: '20%' }}></div>
        <div className="float-crosshair float-elem" style={{ top: '70%', right: '8%' }}></div>
        <div className="float-crosshair float-crosshair-purple float-elem-delay-1" style={{ bottom: '30%', left: '35%' }}></div>
        <div className="float-crosshair float-crosshair-orange float-elem-delay-2" style={{ bottom: '12%', right: '40%' }}></div>
      </div>

      {/* Background glow orbs */}
      <div className="glow-orb-1" style={{ position: 'absolute', top: '8%', left: '5%', width: '35%', height: '35%', zIndex: 0, pointerEvents: 'none' }}></div>
      <div className="glow-orb-2" style={{ position: 'absolute', top: '35%', right: '2%', width: '40%', height: '40%', zIndex: 0, pointerEvents: 'none' }}></div>
      <div className="glow-orb-3" style={{ zIndex: 0 }}></div>

      {/* Navigation */}
      <nav className="main-nav" style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '20px 50px',
        borderBottom: '1px solid rgba(255,255,255,0.06)',
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        zIndex: 100,
        background: 'rgba(3, 2, 6, 0.75)',
        backdropFilter: 'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
          <div style={{
            background: 'linear-gradient(135deg, #fff 0%, #a5a5b5 100%)',
            color: '#000',
            width: '36px',
            height: '36px',
            borderRadius: '8px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: '900',
            fontSize: '18px',
            boxShadow: '0 0 15px rgba(255,255,255,0.2)'
          }}>JF</div>
          <div>
            <div style={{ fontSize: '15px', fontWeight: 'bold', letterSpacing: '1.5px', color: '#fff' }}>JF HACKS</div>
            <div style={{ fontSize: '8px', color: '#00e599', letterSpacing: '2px', fontWeight: 'bold' }}>BOT DISTRIBUTION SYSTEM</div>
          </div>
        </div>

        <div className="nav-center-links" style={{ display: 'flex', gap: '40px', fontSize: '12px', fontWeight: '600', letterSpacing: '1.5px' }}>
          <a href="#security" className="nav-link" style={{ textDecoration: 'none' }}>SECURITY</a>
          <a href="#features" className="nav-link" style={{ textDecoration: 'none' }}>MODULES</a>
          <a href="#telemetry" className="nav-link" style={{ textDecoration: 'none' }}>TELEMETRY</a>
          <a href="#api" className="nav-link" style={{ textDecoration: 'none' }}>API</a>
        </div>

        <div className="nav-right-actions" style={{ display: 'flex', alignItems: 'center', gap: '25px' }}>
          <Link href="/login" className="nav-link" style={{ textDecoration: 'none', fontSize: '13px', fontWeight: '600' }}>
            Sign In
          </Link>
          <Link href="/login" className="btn-console" style={{
            padding: '11px 24px',
            borderRadius: '8px',
            textDecoration: 'none',
            fontWeight: 'bold',
            fontSize: '13px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}>
            Console <ArrowRight size={14} />
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="hero-content" style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
        padding: '200px 20px 60px 20px',
        position: 'relative',
        zIndex: 10
      }}>
        <h1 className="hero-title" style={{
          fontSize: '96px',
          fontWeight: '900',
          lineHeight: '1.0',
          letterSpacing: '-3px',
          maxWidth: '1100px',
          margin: '0 0 30px 0'
        }}>
          Telegram bot licensing<br/>engineered to scale.
        </h1>

        <p style={{
          fontSize: '23px',
          color: '#a0a0b0',
          maxWidth: '850px',
          lineHeight: '1.6',
          margin: '0 0 50px 0',
          fontWeight: '400'
        }}>
          The definitive software distribution panel for bot developers. Encrypted key validation, strict HWID fingerprint lock rules, reseller scope routing, and instant client broadcast pipelines.
        </p>

        <div className="hero-action-buttons" style={{ display: 'flex', gap: '25px', marginBottom: '60px' }}>
          <Link href="/login" className="btn-primary-large" style={{
            padding: '20px 42px',
            borderRadius: '12px',
            textDecoration: 'none',
            fontWeight: '800',
            fontSize: '17px',
            display: 'flex',
            alignItems: 'center',
            gap: '12px'
          }}>
            Launch Console Panel <Rocket size={20} />
          </Link>
          <a href="#api" className="btn-secondary-large" style={{
            padding: '20px 42px',
            borderRadius: '12px',
            textDecoration: 'none',
            fontWeight: '800',
            fontSize: '17px',
            display: 'flex',
            alignItems: 'center',
            gap: '12px'
          }}>
            Verify Bot API <Book size={20} />
          </a>
        </div>

        {/* 3D Scroll-Unfolding Console Mockup */}
        <DashboardConsoleMockup />

        {/* Badges */}
        <div className="hero-bottom-badges" style={{
          display: 'flex',
          gap: '30px',
          marginTop: '65px',
          fontSize: '10px',
          fontWeight: 'bold',
          letterSpacing: '1.5px',
          color: '#556'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Shield size={14} color="#00e599" /> BOT HIERARCHY PROTECTION
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Lock size={14} color="#8b8bff" /> CLIENT HWID INTEGRITY
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Users size={14} color="#ffb84d" /> ZERO-BYPASS TELEGRAM CONTROLLER
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Database size={14} color="#00e599" /> AUTOMATED LICENSE LIFECYCLE
          </div>
        </div>
      </main>

      {/* Defensive Architecture Section */}
      <section id="security" style={{ padding: '120px 50px', position: 'relative', zIndex: 10 }}>
        <Reveal>
          <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
            <div style={{ textAlign: 'center', marginBottom: '80px' }}>
              <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', border: '1px solid rgba(139, 139, 255, 0.3)', background: 'rgba(139, 139, 255, 0.05)', color: '#8b8bff', padding: '6px 16px', borderRadius: '20px', fontSize: '10px', fontWeight: 'bold', letterSpacing: '1px', marginBottom: '20px' }}>
                <Shield size={12} /> CLIENT EXECUTABLE PROTECTION
              </div>
              <h2 style={{ fontSize: '50px', fontWeight: '900', margin: '0 0 20px 0', letterSpacing: '-1px' }}>Defensive Architecture.</h2>
              <p style={{ fontSize: '18px', color: '#888', maxWidth: '700px', margin: '0 auto', lineHeight: '1.6' }}>
                Every verification request validates <span style={{ background: 'rgba(255,255,255,0.05)', padding: '3px 9px', borderRadius: '4px', color: '#ccc', fontFamily: 'monospace' }}>Secure Client Fingerprints</span> prior to enabling bot commands. Complete executable security.
              </p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '35px' }}>
              {/* Threat Mitigation Matrix */}
              <div style={{ background: 'rgba(10,10,15,0.6)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: '20px', padding: '45px', backdropFilter: 'blur(10px)', WebkitBackdropFilter: 'blur(10px)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '40px' }}>
                  <div style={{ background: 'rgba(255, 95, 86, 0.1)', padding: '12px', borderRadius: '12px', color: '#ff5f56' }}>
                    <Shield size={24} />
                  </div>
                  <div>
                    <h3 style={{ fontSize: '22px', fontWeight: 'bold', margin: '0 0 5px 0' }}>Bot Threat Shield</h3>
                    <p style={{ color: '#666', fontSize: '13px', margin: 0 }}>Enforced at runtime validation endpoints</p>
                  </div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                  <div className="feature-badge" style={{ background: 'rgba(255,255,255,0.01)', border: '1px solid rgba(255,255,255,0.03)', padding: '20px', borderRadius: '12px', display: 'block' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                      <Database size={16} color="#00e599" />
                      <h4 style={{ margin: 0, fontSize: '15px', fontWeight: 'bold' }}>Dynamic Bypass Loader</h4>
                    </div>
                    <p style={{ color: '#888', fontSize: '13px', margin: 0, paddingLeft: '26px' }}>Delivers encrypted memory offsets, bypass payloads, and streamer protection libraries to bot clients at runtime.</p>
                  </div>
                  
                  <div className="feature-badge" style={{ background: 'rgba(255,255,255,0.01)', border: '1px solid rgba(255,255,255,0.03)', padding: '20px', borderRadius: '12px', display: 'block' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                      <Lock size={16} color="#8b8bff" />
                      <h4 style={{ margin: 0, fontSize: '15px', fontWeight: 'bold' }}>HWID Fingerprint Validation</h4>
                    </div>
                    <p style={{ color: '#888', fontSize: '13px', margin: 0, paddingLeft: '26px' }}>Locks cheat licenses to unique CPU, motherboard, and GPU hardware IDs, preventing key sharing or cracking.</p>
                  </div>

                  <div className="feature-badge" style={{ background: 'rgba(255,255,255,0.01)', border: '1px solid rgba(255,255,255,0.03)', padding: '20px', borderRadius: '12px', display: 'block' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                      <UserCheck size={16} color="#ffb84d" />
                      <h4 style={{ margin: 0, fontSize: '15px', fontWeight: 'bold' }}>Telegram Store Gateway</h4>
                    </div>
                    <p style={{ color: '#888', fontSize: '13px', margin: 0, paddingLeft: '26px' }}>Verifies reseller payments instantly via UPI Gateway, automatically delivering keys and managing trial vouchers.</p>
                  </div>
                </div>
              </div>

              {/* RBAC Hierarchy */}
              <div style={{ background: 'rgba(10,10,15,0.6)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: '20px', padding: '45px', backdropFilter: 'blur(10px)', WebkitBackdropFilter: 'blur(10px)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '40px' }}>
                  <div style={{ background: 'rgba(0, 229, 153, 0.1)', padding: '12px', borderRadius: '12px', color: '#00e599' }}>
                    <Users size={24} />
                  </div>
                  <div>
                    <h3 style={{ fontSize: '22px', fontWeight: 'bold', margin: '0 0 5px 0' }}>Reseller Allocation Matrix</h3>
                    <p style={{ color: '#666', fontSize: '13px', margin: 0 }}>Scoped hierarchies to generate and sell keys</p>
                  </div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '30px', position: 'relative' }}>
                  <div style={{ position: 'absolute', left: '7px', top: '20px', bottom: '20px', width: '2px', background: 'rgba(255,255,255,0.05)' }}></div>
                  
                  <div style={{ position: 'relative', paddingLeft: '30px' }}>
                    <div style={{ position: 'absolute', left: '4px', top: '5px', width: '8px', height: '8px', borderRadius: '50%', background: '#00e599', boxShadow: '0 0 10px #00e599' }}></div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
                      <h4 style={{ margin: 0, fontSize: '16px', fontWeight: 'bold' }}>ROOT DEVELOPER</h4>
                      <span style={{ fontSize: '9px', background: 'rgba(0, 229, 153, 0.15)', padding: '3px 8px', borderRadius: '4px', color: '#00e599', fontWeight: 'bold', border: '1px solid rgba(0, 229, 153, 0.2)' }}>ROOT ACCESS</span>
                    </div>
                    <p style={{ color: '#888', fontSize: '13px', margin: 0, lineHeight: '1.5' }}>Complete administrative ownership. Can build server modules, delete keys, edit pricing settings, and run global client broadcasts.</p>
                  </div>

                  <div style={{ position: 'relative', paddingLeft: '30px' }}>
                    <div style={{ position: 'absolute', left: '4px', top: '5px', width: '8px', height: '8px', borderRadius: '50%', background: '#8b8bff', boxShadow: '0 0 10px #8b8bff' }}></div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
                      <h4 style={{ margin: 0, fontSize: '16px', fontWeight: 'bold' }}>STAFF OPERATOR</h4>
                      <span style={{ fontSize: '9px', background: 'rgba(139, 139, 255, 0.15)', padding: '3px 8px', borderRadius: '4px', color: '#8b8bff', fontWeight: 'bold', border: '1px solid rgba(139, 139, 255, 0.2)' }}>STAFF ACCESS</span>
                    </div>
                    <p style={{ color: '#888', fontSize: '13px', margin: 0, lineHeight: '1.5' }}>Manage bot user databases, edit active keys, log client tickets, and check live system telemetry.</p>
                  </div>

                  <div style={{ position: 'relative', paddingLeft: '30px' }}>
                    <div style={{ position: 'absolute', left: '4px', top: '5px', width: '8px', height: '8px', borderRadius: '50%', background: '#ffb84d', boxShadow: '0 0 10px #ffb84d' }}></div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
                      <h4 style={{ margin: 0, fontSize: '16px', fontWeight: 'bold' }}>VIP RESELLER</h4>
                      <span style={{ fontSize: '9px', background: 'rgba(255, 184, 77, 0.15)', padding: '3px 8px', borderRadius: '4px', color: '#ffb84d', fontWeight: 'bold', border: '1px solid rgba(255, 184, 77, 0.2)' }}>RESELLER SCOPE</span>
                    </div>
                    <p style={{ color: '#888', fontSize: '13px', margin: 0, lineHeight: '1.5' }}>Scoped down to client generation. Buy balance pools and generate client keys for their own customer scopes safely.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Reveal>
      </section>

      {/* Unified Operations Section */}
      <section id="features" style={{ padding: '100px 50px', position: 'relative', zIndex: 10 }}>
        <Reveal>
          <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
            <div style={{ textAlign: 'center', marginBottom: '80px' }}>
              <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', border: '1px solid rgba(0, 229, 153, 0.3)', background: 'rgba(0, 229, 153, 0.05)', color: '#00e599', padding: '6px 16px', borderRadius: '20px', fontSize: '10px', fontWeight: 'bold', letterSpacing: '1px', marginBottom: '20px' }}>
                <Zap size={12} /> SYSTEM CHANNELS
              </div>
              <h2 style={{ fontSize: '50px', fontWeight: '900', margin: '0 0 20px 0', letterSpacing: '-1px' }}>Unified Bot Controls.</h2>
              <p style={{ fontSize: '17px', color: '#888', maxWidth: '650px', margin: '0 auto', lineHeight: '1.6' }}>
                Optimized endpoints to coordinate bot vouchers, client scopes, and server configuration.
              </p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '30px' }}>
              <div className="glass-card" style={{ padding: '40px' }}>
                <div style={{ background: 'rgba(255, 184, 77, 0.1)', width: '46px', height: '46px', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#ffb84d', marginBottom: '25px', boxShadow: '0 0 15px rgba(255, 184, 77, 0.15)' }}>
                  <Key size={22} />
                </div>
                <h3 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '15px' }}>Cheat Key Generation</h3>
                <p style={{ color: '#888', fontSize: '14px', lineHeight: '1.6', margin: 0 }}>
                  Instantly generate and manage premium keys for products like Greed, HXN, Prime, and BR Mods from the central console.
                </p>
              </div>

              <div className="glass-card" style={{ padding: '40px' }}>
                <div style={{ background: 'rgba(139, 139, 255, 0.1)', width: '46px', height: '46px', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#8b8bff', marginBottom: '25px', boxShadow: '0 0 15px rgba(139, 139, 255, 0.15)' }}>
                  <Zap size={22} />
                </div>
                <h3 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '15px' }}>Trial Key Cooldowns</h3>
                <p style={{ color: '#888', fontSize: '14px', lineHeight: '1.6', margin: 0 }}>
                  Enforce strict free trial rules. Automate claiming cooldown periods tracking Telegram User IDs to block multi-account claims.
                </p>
              </div>

              <div className="glass-card" style={{ padding: '40px' }}>
                <div style={{ background: 'rgba(0, 229, 153, 0.1)', width: '46px', height: '46px', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#00e599', marginBottom: '25px', boxShadow: '0 0 15px rgba(0, 229, 153, 0.15)' }}>
                  <Users size={22} />
                </div>
                <h3 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '15px' }}>Alert & Broadcaster</h3>
                <p style={{ color: '#888', fontSize: '14px', lineHeight: '1.6', margin: 0 }}>
                  Broadcast key cheat updates, server notices, or loader files directly to all running bot clients and user chats in real-time.
                </p>
              </div>
            </div>
          </div>
        </Reveal>
      </section>

      {/* Real-Time Telemetry Monitor Section (Isolated component) */}
      <section id="telemetry" style={{ padding: '100px 50px', position: 'relative', zIndex: 10 }}>
        <Reveal>
          <TelemetryMetricsBlock />
        </Reveal>
      </section>

      {/* Security Authorization Stream Section (Isolated component) */}
      <section id="terminal-stream" style={{ padding: '100px 50px', position: 'relative', zIndex: 10 }}>
        <Reveal>
          <AuditTerminalStream />
        </Reveal>
      </section>

      {/* Integration Section */}
      <section id="api" style={{ padding: '120px 50px', position: 'relative', zIndex: 10 }}>
        <Reveal>
          <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '60px', alignItems: 'center' }}>
            <div>
              <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', border: '1px solid rgba(255, 184, 77, 0.3)', background: 'rgba(255, 184, 77, 0.05)', color: '#ffb84d', padding: '6px 16px', borderRadius: '20px', fontSize: '10px', fontWeight: 'bold', letterSpacing: '1px', marginBottom: '25px' }}>
                <Code size={12} /> DEVELOPER INTEGRATION
              </div>
              <h2 style={{ fontSize: '55px', fontWeight: '900', margin: '0 0 10px 0', letterSpacing: '-2px', lineHeight: '1.1' }}>Link bot clients in seconds.</h2>
              <h2 className="gradient-text" style={{ fontSize: '55px', fontWeight: '900', margin: '0 0 30px 0', letterSpacing: '-2px', background: 'linear-gradient(90deg, #8b8bff 0%, #00e599 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>Scale infinitely.</h2>
              
              <p style={{ fontSize: '17px', color: '#888', lineHeight: '1.7', marginBottom: '40px' }}>
                Call our check servers directly from your bot script files. Secure validations return clear JSON data while mapping hardware signatures.
              </p>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', fontSize: '15px', fontWeight: '500' }}>
                  <CheckCircle2 size={18} color="#00e599" /> Simple JSON payload exchanges
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', fontSize: '15px', fontWeight: '500' }}>
                  <CheckCircle2 size={18} color="#00e599" /> Native HWID lock checks (Python, C#, C++)
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', fontSize: '15px', fontWeight: '500' }}>
                  <CheckCircle2 size={18} color="#00e599" /> Sub-millisecond verification nodes
                </div>
              </div>
            </div>

            <div style={{ background: '#040406', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '16px', overflow: 'hidden', boxShadow: '0 20px 45px rgba(0,0,0,0.6)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 20px', background: 'rgba(255,255,255,0.02)', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
                <div style={{ display: 'flex', gap: '6px' }}>
                  <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ff5f56' }}></div>
                  <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ffbd2e' }}></div>
                  <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#27c93f' }}></div>
                </div>
                <div style={{ fontSize: '11px', color: '#556', fontFamily: 'monospace' }}>bot_client.py</div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '10px', color: '#00e599', fontWeight: 'bold' }}>
                  <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#00e599' }}></div> ONLINE LINK
                </div>
              </div>
              <div style={{ padding: '25px', fontFamily: 'monospace', fontSize: '13px', lineHeight: '1.6', color: '#ccc', overflowX: 'auto' }}>
                <div style={{ display: 'flex' }}><span style={{ color: '#444', marginRight: '15px', userSelect: 'none' }}>1</span><span style={{ color: '#666' }}># Connect bot to validation servers</span></div>
                <div style={{ display: 'flex' }}><span style={{ color: '#444', marginRight: '15px', userSelect: 'none' }}>2</span><span>sdk = jfhacks.<span style={{ color: '#8b8bff' }}>InitClient</span>(<span style={{ color: '#00e599' }}>"JF-KEY-CHECK"</span>)</span></div>
                <div style={{ display: 'flex' }}><span style={{ color: '#444', marginRight: '15px', userSelect: 'none' }}>3</span><span></span></div>
                <div style={{ display: 'flex' }}><span style={{ color: '#444', marginRight: '15px', userSelect: 'none' }}>4</span><span style={{ color: '#666' }}># Validate hardware config matching</span></div>
                <div style={{ display: 'flex' }}><span style={{ color: '#444', marginRight: '15px', userSelect: 'none' }}>5</span><span>res, err = sdk.<span style={{ color: '#00e599' }}>VerifyLicense</span>({`{`}</span></div>
                <div style={{ display: 'flex' }}><span style={{ color: '#444', marginRight: '15px', userSelect: 'none' }}>6</span><span>  <span style={{ color: '#00e599' }}>"key"</span>: <span style={{ color: '#00e599' }}>"JF-VIP-KEY-8871"</span>,</span></div>
                <div style={{ display: 'flex' }}><span style={{ color: '#444', marginRight: '15px', userSelect: 'none' }}>7</span><span>  <span style={{ color: '#00e599' }}>"hwid"</span>: <span style={{ color: '#00e599' }}>"2faf50e937bdc80f99f..."</span></span></div>
                <div style={{ display: 'flex' }}><span style={{ color: '#444', marginRight: '15px', userSelect: 'none' }}>8</span><span>{`}`})</span></div>
                <div style={{ display: 'flex' }}><span style={{ color: '#444', marginRight: '15px', userSelect: 'none' }}>9</span><span></span></div>
                <div style={{ display: 'flex' }}><span style={{ color: '#444', marginRight: '15px', userSelect: 'none' }}>10</span><span><span style={{ color: '#ffb84d' }}>if</span> err == None and res[<span style={{ color: '#00e599' }}>"status"</span>] == True:</span></div>
                <div style={{ display: 'flex' }}><span style={{ color: '#444', marginRight: '15px', userSelect: 'none' }}>11</span><span>  <span style={{ color: '#00e599' }}>print</span>(f<span style={{ color: '#00e599' }}>"Session active. Expiry: {`{`}res['expires_at']{`}`}"</span>)</span></div>
              </div>
            </div>
          </div>
        </Reveal>
      </section>

      {/* FAQ Section */}
      <section id="faq" style={{ padding: '100px 50px', position: 'relative', zIndex: 10 }}>
        <Reveal>
          <div style={{ maxWidth: '800px', margin: '0 auto' }}>
            <div style={{ textAlign: 'center', marginBottom: '60px' }}>
              <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', border: '1px solid rgba(0, 229, 153, 0.3)', background: 'rgba(0, 229, 153, 0.05)', color: '#00e599', padding: '6px 16px', borderRadius: '20px', fontSize: '10px', fontWeight: 'bold', letterSpacing: '1px', marginBottom: '20px' }}>
                <Book size={12} /> FREQUENT QUESTIONS
              </div>
              <h2 style={{ fontSize: '46px', fontWeight: '900', margin: '0 0 20px 0', letterSpacing: '-1px' }}>System FAQ.</h2>
              <p style={{ fontSize: '16px', color: '#888', lineHeight: '1.6' }}>
                Everything you need to understand about the secure JF HACKS bot panel.
              </p>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column' }}>
              <FAQItem 
                question="How does the HWID lock protect my bot clients?" 
                answer="When a bot client executes, the library hashes the CPU and hardware configuration, checking it against stored records. If matching credentials are run on unauthorized hardware, the verification gateway immediately blocks validation, preventing cracks and license sharing."
              />
              <FAQItem 
                question="What is the difference between Staff Operators and Resellers?" 
                answer="Staff Operators are administrative accounts that can edit configuration variables, log global tickets, and manage all users. Reseller accounts are scoped to only view, buy, and allocate key licenses they purchase, isolating reseller customer details."
              />
              <FAQItem 
                question="How does the live Broadcast system work?" 
                answer="The administration panel connects directly with bot binaries via our real-time messaging pipeline. Root Developers can send push updates, announce code changes, or notify bot clients of downtime instantly."
              />
              <FAQItem 
                question="Is database verification latency optimized?" 
                answer="Yes. Telemetry verification requests are resolved utilizing memory caches and optimized databases. Handshake checks execute in under 15ms globally, keeping bot performance completely unaffected."
              />
            </div>
          </div>
        </Reveal>
      </section>

      {/* Global Scale Section */}
      <section id="scale" style={{ padding: '150px 50px', position: 'relative', overflow: 'hidden', zIndex: 10 }}>
        {/* Globe Effect Background */}
        <div className="dome-effect"></div>
        
        <Reveal>
          <div style={{ maxWidth: '800px', margin: '0 auto', textAlign: 'center', position: 'relative', zIndex: 20 }}>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', border: '1px solid rgba(0, 229, 153, 0.3)', background: 'rgba(0, 229, 153, 0.05)', color: '#00e599', padding: '6px 16px', borderRadius: '20px', fontSize: '10px', fontWeight: 'bold', letterSpacing: '1px', marginBottom: '30px' }}>
              <Globe size={12} /> SOVEREIGN DISTRIBUTION NETWORK
            </div>
            <h2 style={{ fontSize: '70px', fontWeight: '900', margin: '0 0 10px 0', letterSpacing: '-2.5px', lineHeight: '1' }}>JF HACKS Scale.</h2>
            <h2 style={{ fontSize: '70px', fontWeight: '900', margin: '0 0 30px 0', letterSpacing: '-2.5px', color: '#00e599', lineHeight: '1' }}>Zero Compromise.</h2>
            
            <p style={{ fontSize: '20px', color: '#a0a0b0', lineHeight: '1.6', marginBottom: '50px', maxWidth: '650px', margin: '0 auto 50px auto' }}>
              Built to manage thousands of active bot clients concurrently. Compile your binaries, and let JF HACKS coordinate verification.
            </p>

            <Link href="/login" className="btn-primary-large" style={{
              padding: '18px 45px',
              borderRadius: '12px',
              textDecoration: 'none',
              fontWeight: '800',
              fontSize: '16px',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '10px'
            }}>
              Deploy License Gateway <Rocket size={18} />
            </Link>
          </div>
        </Reveal>
      </section>

      {/* Footer */}
      <footer style={{
        padding: '50px 50px',
        backgroundColor: 'rgba(3, 2, 6, 0.9)',
        borderTop: '1px solid rgba(255,255,255,0.06)',
        position: 'relative',
        zIndex: 10,
        backdropFilter: 'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)'
      }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '25px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              background: '#fff',
              color: '#000',
              width: '24px',
              height: '24px',
              borderRadius: '5px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: '900',
              fontSize: '14px',
            }}>JF</div>
            <div style={{ fontSize: '14px', fontWeight: 'bold', letterSpacing: '2px', color: '#fff' }}>
              JF HACKS
            </div>
          </div>
          
          <div style={{ display: 'flex', gap: '35px', fontSize: '11px', fontWeight: 'bold', letterSpacing: '1.5px', color: '#556' }}>
            <a href="#security" className="nav-link" style={{ textDecoration: 'none' }}>SECURITY</a>
            <a href="#features" className="nav-link" style={{ textDecoration: 'none' }}>MODULES</a>
            <a href="#telemetry" className="nav-link" style={{ textDecoration: 'none' }}>TELEMETRY</a>
            <a href="#api" className="nav-link" style={{ textDecoration: 'none' }}>API</a>
          </div>
          
          <div style={{ fontSize: '11px', color: '#445', fontWeight: 'bold', letterSpacing: '1.5px' }}>
            © 2026 JF HACKS SYSTEMS. ALL RIGHTS RESERVED.
          </div>
        </div>
      </footer>

    </div>
  );
}

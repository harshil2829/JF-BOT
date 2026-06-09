'use client';

import { Users, Key, ShieldCheck, Settings, HeadphonesIcon, XCircle, Crown, LayoutDashboard, Database, Megaphone } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="sidebar">
      <div style={{ padding: '0 20px', display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '30px' }}>
        <div style={{ width: '32px', height: '32px', background: 'var(--primary)', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 10px var(--primary-glow)' }}>
          <span style={{ color: 'white', fontWeight: 'bold', fontSize: '18px' }}>⚡</span>
        </div>
        <h2 style={{ fontSize: '18px', margin: 0, fontWeight: 700 }}>Quantum Bot <span style={{display: 'block', fontSize: '12px', color: 'var(--text-muted)', fontWeight: 400}}>Admin Panel</span></h2>
      </div>

      <Link href="/" className={`menu-item ${pathname === '/' ? 'active' : ''}`}>
        <LayoutDashboard size={18} /> Dashboard
      </Link>
      <Link href="/keys" className={`menu-item ${pathname === '/keys' ? 'active' : ''}`}>
        <Key size={18} /> Key Management
      </Link>
      <Link href="/users" className={`menu-item ${pathname === '/users' ? 'active' : ''}`}>
        <Users size={18} /> User Management
      </Link>
      <Link href="/products" className={`menu-item ${pathname === '/products' ? 'active' : ''}`}>
        <Database size={18} /> Product Management
      </Link>
      <Link href="/broadcast" className={`menu-item ${pathname === '/broadcast' ? 'active' : ''}`}>
        <Megaphone size={18} /> Broadcast
      </Link>
      <Link href="/settings" className={`menu-item ${pathname === '/settings' ? 'active' : ''}`}>
        <Settings size={18} /> Settings
      </Link>
      <Link href="/support" className={`menu-item ${pathname === '/support' ? 'active' : ''}`}>
        <HeadphonesIcon size={18} /> Staff & Support
      </Link>
      <Link href="/admin" className={`menu-item ${pathname === '/admin' ? 'active' : ''}`}>
        <ShieldCheck size={18} /> Admin Management
      </Link>
    </div>
  );
}

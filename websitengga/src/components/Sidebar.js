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

      <Link href="/dashboard" className={`menu-item ${pathname === '/dashboard' ? 'active' : ''}`}>
        <LayoutDashboard size={18} /> Dashboard
      </Link>
      <Link href="/dashboard/keys" className={`menu-item ${pathname === '/dashboard/keys' ? 'active' : ''}`}>
        <Key size={18} /> Key Management
      </Link>
      <Link href="/dashboard/users" className={`menu-item ${pathname === '/dashboard/users' ? 'active' : ''}`}>
        <Users size={18} /> User Management
      </Link>
      <Link href="/dashboard/products" className={`menu-item ${pathname === '/dashboard/products' ? 'active' : ''}`}>
        <Database size={18} /> Product Management
      </Link>
      <Link href="/dashboard/broadcast" className={`menu-item ${pathname === '/dashboard/broadcast' ? 'active' : ''}`}>
        <Megaphone size={18} /> Broadcast
      </Link>
      <Link href="/dashboard/settings" className={`menu-item ${pathname === '/dashboard/settings' ? 'active' : ''}`}>
        <Settings size={18} /> Settings
      </Link>
      <Link href="/dashboard/support" className={`menu-item ${pathname === '/dashboard/support' ? 'active' : ''}`}>
        <HeadphonesIcon size={18} /> Staff & Support
      </Link>
      <Link href="/dashboard/admin" className={`menu-item ${pathname === '/dashboard/admin' ? 'active' : ''}`}>
        <ShieldCheck size={18} /> Admin Management
      </Link>
    </div>
  );
}

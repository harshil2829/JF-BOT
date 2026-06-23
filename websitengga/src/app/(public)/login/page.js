'use client';
import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();
    // Redirect to the dashboard after a simple delay (to mimic login)
    router.push('/');
  };

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#000000',
      color: '#ffffff',
      fontFamily: 'var(--font-geist-sans), sans-serif',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px'
    }}>
      
      {/* Logo */}
      <div style={{
        background: '#ffffff',
        color: '#000000',
        width: '40px',
        height: '40px',
        borderRadius: '6px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontWeight: 'bold',
        fontSize: '20px',
        marginBottom: '40px'
      }}>
        Q
      </div>

      {/* Login Card */}
      <div style={{
        backgroundColor: '#0a0a0a',
        border: '1px solid rgba(255,255,255,0.05)',
        borderRadius: '12px',
        padding: '30px',
        width: '100%',
        maxWidth: '380px',
        boxShadow: '0 10px 40px rgba(0,0,0,0.5)'
      }}>
        <h2 style={{ fontSize: '20px', fontWeight: 'bold', margin: '0 0 8px 0' }}>Welcome back</h2>
        <p style={{ color: '#888', fontSize: '13px', margin: '0 0 30px 0' }}>
          Enter your credentials to access your account
        </p>

        <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <label style={{ fontSize: '10px', fontWeight: 'bold', letterSpacing: '1px', color: '#ccc' }}>USERNAME</label>
            <input 
              type="text" 
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              style={{
                backgroundColor: '#111',
                border: '1px solid #222',
                borderRadius: '8px',
                padding: '12px 14px',
                color: '#fff',
                fontSize: '14px',
                outline: 'none',
                width: '100%',
                boxSizing: 'border-box'
              }}
            />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <label style={{ fontSize: '10px', fontWeight: 'bold', letterSpacing: '1px', color: '#ccc' }}>PASSWORD</label>
            <div style={{ position: 'relative' }}>
              <input 
                type="password" 
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{
                  backgroundColor: '#111',
                  border: '1px solid #222',
                  borderRadius: '8px',
                  padding: '12px 14px',
                  color: '#fff',
                  fontSize: '14px',
                  outline: 'none',
                  width: '100%',
                  boxSizing: 'border-box',
                  fontFamily: 'monospace'
                }}
              />
              {/* Fake Eye Icon */}
              <div style={{
                position: 'absolute',
                right: '12px',
                top: '50%',
                transform: 'translateY(-50%)',
                color: '#666',
                cursor: 'pointer'
              }}>
                👁️
              </div>
            </div>
          </div>

          <button type="submit" style={{
            backgroundColor: '#ffffff',
            color: '#000000',
            border: 'none',
            borderRadius: '8px',
            padding: '12px',
            fontSize: '14px',
            fontWeight: 'bold',
            cursor: 'pointer',
            marginTop: '10px',
            transition: 'background-color 0.2s'
          }}>
            Sign In
          </button>

        </form>
      </div>

      {/* Footer Link */}
      <div style={{ marginTop: '20px', fontSize: '12px', color: '#666' }}>
        Need help? <a href="#" style={{ color: '#888', textDecoration: 'none' }}>Contact support</a>
      </div>

    </div>
  );
}

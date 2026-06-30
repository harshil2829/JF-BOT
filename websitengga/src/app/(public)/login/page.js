'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Eye, EyeOff, Lock, User, AlertCircle } from 'lucide-react';
import { loginAction } from './actions';
import '../landing.css'; // Leverage our premium landing CSS

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      // Secure server action call
      const res = await loginAction(username, password);
      
      if (res.success) {
        // Successful login, redirect to protected dashboard
        router.push('/dashboard');
      } else {
        setError(res.error || 'Invalid credentials');
      }
    } catch (err) {
      setError('A secure socket communication error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      color: '#ffffff',
      fontFamily: 'var(--font-geist-sans), sans-serif',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px',
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Background Mesh Grid */}
      <div className="bg-mesh">
        <div className="bg-grid"></div>
        <div className="scanline"></div>

        {/* Falling Cyber Matrix Columns */}
        <div className="cyber-column" style={{ left: '10%', height: '280px', animationDelay: '0s', animationDuration: '14s' }}></div>
        <div className="cyber-column cyber-col-purple" style={{ left: '25%', height: '350px', animationDelay: '4s', animationDuration: '18s' }}></div>
        <div className="cyber-column cyber-col-orange" style={{ left: '42%', height: '220px', animationDelay: '1.5s', animationDuration: '12s' }}></div>
        <div className="cyber-column" style={{ left: '58%', height: '390px', animationDelay: '6s', animationDuration: '20s' }}></div>
        <div className="cyber-column cyber-col-purple" style={{ left: '74%', height: '250px', animationDelay: '2.5s', animationDuration: '15s' }}></div>
        <div className="cyber-column cyber-col-orange" style={{ left: '90%', height: '310px', animationDelay: '8s', animationDuration: '17s' }}></div>
      </div>

      {/* Decorative Blur Orbs */}
      <div className="glow-orb-1" style={{ position: 'absolute', top: '10%', left: '30%', width: '40%', height: '40%', zIndex: 0, pointerEvents: 'none' }}></div>
      <div className="glow-orb-2" style={{ position: 'absolute', bottom: '10%', right: '30%', width: '35%', height: '35%', zIndex: 0, pointerEvents: 'none' }}></div>

      {/* Logo */}
      <div style={{
        background: 'linear-gradient(135deg, #fff 0%, #a5a5b5 100%)',
        color: '#000',
        width: '44px',
        height: '44px',
        borderRadius: '10px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontWeight: '900',
        fontSize: '24px',
        marginBottom: '25px',
        boxShadow: '0 0 25px rgba(255,255,255,0.25)',
        zIndex: 10
      }}>
        JF
      </div>

      <div style={{
        fontSize: '11px',
        color: '#00e599',
        fontWeight: '800',
        letterSpacing: '2px',
        marginBottom: '15px',
        zIndex: 10
      }}>
        SECURE AUTHORIZATION NODE
      </div>

      {/* Login Card */}
      <div style={{
        backgroundColor: 'rgba(8, 8, 12, 0.75)',
        border: '1px solid rgba(255,255,255,0.06)',
        borderRadius: '16px',
        padding: '40px',
        width: '100%',
        maxWidth: '400px',
        boxShadow: '0 20px 50px rgba(0,0,0,0.8), 0 0 30px rgba(0, 229, 153, 0.02)',
        backdropFilter: 'blur(20px)',
        WebkitBackdropFilter: 'blur(20px)',
        zIndex: 10,
        boxSizing: 'border-box'
      }}>
        <h2 style={{ fontSize: '24px', fontWeight: 'bold', margin: '0 0 8px 0', letterSpacing: '-0.5px' }}>Access Admin Console</h2>
        <p style={{ color: '#666', fontSize: '13px', margin: '0 0 30px 0', lineHeight: '1.4' }}>
          Enter cryptographic validation credentials to retrieve active server tokens.
        </p>

        {error && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            background: 'rgba(255, 95, 86, 0.08)',
            border: '1px solid rgba(255, 95, 86, 0.25)',
            borderRadius: '8px',
            padding: '12px 16px',
            color: '#ff5f56',
            fontSize: '13px',
            marginBottom: '25px',
            fontWeight: 'bold',
            boxShadow: '0 0 10px rgba(255, 95, 86, 0.05)'
          }}>
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '22px' }}>
          
          {/* Username Input */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <label style={{ fontSize: '10px', fontWeight: '800', letterSpacing: '1.5px', color: '#556' }}>ADMINISTRATIVE ID</label>
            <div style={{ position: 'relative' }}>
              <div style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', color: '#445' }}>
                <User size={15} />
              </div>
              <input 
                type="text" 
                placeholder="ID Hash / Account"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                disabled={isLoading}
                style={{
                  backgroundColor: 'rgba(255,255,255,0.01)',
                  border: '1px solid rgba(255,255,255,0.05)',
                  borderRadius: '8px',
                  padding: '12px 14px 12px 40px',
                  color: '#fff',
                  fontSize: '14px',
                  outline: 'none',
                  width: '100%',
                  boxSizing: 'border-box',
                  transition: 'all 0.3s ease',
                  fontFamily: 'monospace'
                }}
                className="feature-badge" // Triggers hover styles from landing.css
              />
            </div>
          </div>

          {/* Password Input */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <label style={{ fontSize: '10px', fontWeight: '800', letterSpacing: '1.5px', color: '#556' }}>CRYPTOGRAPHIC CODE</label>
            <div style={{ position: 'relative' }}>
              <div style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', color: '#445' }}>
                <Lock size={15} />
              </div>
              <input 
                type={showPassword ? "text" : "password"} 
                placeholder="••••••••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={isLoading}
                style={{
                  backgroundColor: 'rgba(255,255,255,0.01)',
                  border: '1px solid rgba(255,255,255,0.05)',
                  borderRadius: '8px',
                  padding: '12px 42px 12px 40px',
                  color: '#fff',
                  fontSize: '14px',
                  outline: 'none',
                  width: '100%',
                  boxSizing: 'border-box',
                  transition: 'all 0.3s ease',
                  fontFamily: 'monospace'
                }}
                className="feature-badge"
              />
              {/* Dynamic Eye Icon Toggle (replaces fake emoji) */}
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={{
                  position: 'absolute',
                  right: '14px',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  background: 'none',
                  border: 'none',
                  color: '#445',
                  cursor: 'pointer',
                  padding: 0,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  outline: 'none'
                }}
              >
                {showPassword ? <EyeOff size={16} color="#00e599" /> : <Eye size={16} />}
              </button>
            </div>
          </div>

          {/* Submit Button */}
          <button 
            type="submit" 
            disabled={isLoading}
            style={{
              backgroundColor: '#00e599',
              color: '#000000',
              border: 'none',
              borderRadius: '8px',
              padding: '13px',
              fontSize: '14px',
              fontWeight: '900',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              marginTop: '10px',
              transition: 'all 0.25s cubic-bezier(0.16, 1, 0.3, 1)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              boxShadow: '0 0 15px rgba(0, 229, 153, 0.2)'
            }}
            className="btn-console"
          >
            {isLoading ? 'Decrypting token...' : 'Authorize Client Session'}
          </button>

        </form>
      </div>

      {/* Footer Link */}
      <div style={{ marginTop: '30px', fontSize: '11px', color: '#445', fontWeight: 'bold', letterSpacing: '1px', zIndex: 10 }}>
        © 2026 JF HACKS SYSTEMS · <Link href="/" style={{ color: '#666', textDecoration: 'none' }}>Return to Landing</Link>
      </div>

    </div>
  );
}

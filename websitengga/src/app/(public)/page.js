import Link from 'next/link';

export default function LandingPage() {
  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#0a0a0a',
      color: '#ffffff',
      fontFamily: 'var(--font-geist-sans), sans-serif',
      display: 'flex',
      flexDirection: 'column',
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Background glow effects */}
      <div style={{
        position: 'absolute',
        top: '-10%',
        left: '20%',
        width: '40%',
        height: '40%',
        background: 'radial-gradient(circle, rgba(0,255,170,0.05) 0%, rgba(0,0,0,0) 70%)',
        zIndex: 0
      }}></div>
      <div style={{
        position: 'absolute',
        bottom: '10%',
        right: '10%',
        width: '50%',
        height: '50%',
        background: 'radial-gradient(circle, rgba(0,255,170,0.03) 0%, rgba(0,0,0,0) 70%)',
        zIndex: 0
      }}></div>

      {/* Navigation */}
      <nav style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '20px 40px',
        borderBottom: '1px solid rgba(255,255,255,0.05)',
        position: 'relative',
        zIndex: 10
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
          <div style={{
            background: '#fff',
            color: '#000',
            width: '40px',
            height: '40px',
            borderRadius: '8px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: 'bold',
            fontSize: '20px'
          }}>Q</div>
          <div>
            <div style={{ fontSize: '18px', fontWeight: 'bold', letterSpacing: '1px' }}>QUANTUM PANEL</div>
            <div style={{ fontSize: '10px', color: '#888', letterSpacing: '2px' }}>ENTERPRISE PANEL</div>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '30px', fontSize: '13px', fontWeight: '600', color: '#aaa' }}>
          <span style={{ cursor: 'pointer', color: '#fff' }}>SECURITY</span>
          <span style={{ cursor: 'pointer' }}>MODULES</span>
          <span style={{ cursor: 'pointer' }}>WORKFLOW</span>
          <span style={{ cursor: 'pointer' }}>API</span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
          <Link href="/login" style={{ color: '#aaa', textDecoration: 'none', fontSize: '14px', fontWeight: '500' }}>
            Sign In
          </Link>
          <Link href="/login" style={{
            backgroundColor: '#00e599',
            color: '#000',
            padding: '10px 24px',
            borderRadius: '6px',
            textDecoration: 'none',
            fontWeight: 'bold',
            fontSize: '14px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            transition: 'all 0.2s'
          }}>
            Console ➔
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <main style={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
        padding: '80px 20px',
        position: 'relative',
        zIndex: 10
      }}>
        
        <div style={{
          border: '1px solid rgba(0, 229, 153, 0.2)',
          background: 'rgba(0, 229, 153, 0.05)',
          color: '#00e599',
          padding: '6px 16px',
          borderRadius: '20px',
          fontSize: '11px',
          fontWeight: 'bold',
          letterSpacing: '1px',
          marginBottom: '40px',
          display: 'flex',
          alignItems: 'center',
          gap: '8px'
        }}>
          <div style={{ width: '6px', height: '6px', backgroundColor: '#00e599', borderRadius: '50%' }}></div>
          QUANTUM PANEL · ENTERPRISE V2.0
        </div>

        <h1 style={{
          fontSize: '85px',
          fontWeight: '800',
          lineHeight: '1.1',
          letterSpacing: '-2px',
          maxWidth: '1000px',
          margin: '0 0 30px 0'
        }}>
          License infrastructure<br/>engineered to scale.
        </h1>

        <p style={{
          fontSize: '22px',
          color: '#a0a0a0',
          maxWidth: '800px',
          lineHeight: '1.6',
          margin: '0 0 50px 0'
        }}>
          The definitive software distribution platform. Multi-layered
          security, cryptographic key generation, strict role-based access,
          and real-time audit logging — all in one unified console.
        </p>

        <div style={{ display: 'flex', gap: '20px' }}>
          <Link href="/login" style={{
            backgroundColor: '#00e599',
            color: '#000',
            padding: '18px 36px',
            borderRadius: '12px',
            textDecoration: 'none',
            fontWeight: 'bold',
            fontSize: '16px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px'
          }}>
            Initialize Workspace 🚀
          </Link>
          <a href="#" style={{
            backgroundColor: '#111',
            border: '1px solid #333',
            color: '#fff',
            padding: '18px 36px',
            borderRadius: '12px',
            textDecoration: 'none',
            fontWeight: 'bold',
            fontSize: '16px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px'
          }}>
            Explore Documentation 📄
          </a>
        </div>

        {/* Badges */}
        <div style={{
          display: 'flex',
          gap: '40px',
          marginTop: '80px',
          fontSize: '11px',
          fontWeight: 'bold',
          letterSpacing: '1px',
          color: '#666'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ color: '#00e599' }}>🛡</span> PDO PREPARED STATEMENTS
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ color: '#00e599' }}>🔒</span> SAMESITE=STRICT SESSIONS
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ color: '#00e599' }}>👥</span> 3-TIER RBAC
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ color: '#00e599' }}>📄</span> IMMUTABLE AUDIT LOGS
          </div>
        </div>

      </main>
    </div>
  );
}

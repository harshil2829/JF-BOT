"use client";

import { useState } from 'react';
import { Search, Key, Plus, Trash2, X } from 'lucide-react';
import { addKeys } from '../actions';
import { useRouter } from 'next/navigation';

function KeyModal({ isOpen, onClose, onSave, productsList }) {
  const [product, setProduct] = useState('');
  const [duration, setDuration] = useState('1d');
  const [keysInput, setKeysInput] = useState('');

  // Extract unique product names from the list
  const finalProducts = productsList && productsList.length > 0 
    ? [...new Set(productsList.map(p => p.name.split('_')[0].toLowerCase()))] 
    : ["hxn", "lk", "hex", "alpha", "boyyah", "ngo", "greed", "streamerx", "brmods", "prime", "harshil", "streamerxsh"];

  if (!isOpen) return null;

  // Initialize selected product if empty
  if (!product && finalProducts.length > 0) {
    setProduct(finalProducts[0]);
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    const keysArray = keysInput
      .split(/[\n,]+/)
      .map(k => k.trim())
      .filter(Boolean);
      
    if (keysArray.length === 0) {
      alert("Please enter at least one key.");
      return;
    }
    onSave(product, duration, keysArray);
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
        borderRadius: '16px', padding: '30px', width: '100%', maxWidth: '450px',
        boxShadow: '0 20px 60px rgba(0,0,0,0.5)'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '25px' }}>
          <h2 style={{ margin: 0, fontSize: '20px' }}>🔑 Add License Keys</h2>
          <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: '#aaa', cursor: 'pointer', padding: '5px' }}>
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', fontSize: '13px', color: '#aaa', marginBottom: '6px' }}>Select Product</label>
            <select value={product} onChange={e => setProduct(e.target.value)} required
              style={{
                width: '100%', padding: '12px 14px', background: 'rgba(255,255,255,0.06)',
                border: '1px solid #333', borderRadius: '10px', color: 'white',
                fontSize: '14px', outline: 'none', boxSizing: 'border-box'
              }}
            >
              {finalProducts.map((p, i) => (
                <option key={i} value={p} style={{ background: '#1a1a2e' }}>{p.toUpperCase()}</option>
              ))}
            </select>
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', fontSize: '13px', color: '#aaa', marginBottom: '6px' }}>Duration</label>
            <select value={duration} onChange={e => setDuration(e.target.value)} required
              style={{
                width: '100%', padding: '12px 14px', background: 'rgba(255,255,255,0.06)',
                border: '1px solid #333', borderRadius: '10px', color: 'white',
                fontSize: '14px', outline: 'none', boxSizing: 'border-box'
              }}
            >
              <option value="1d" style={{ background: '#1a1a2e' }}>1 Day</option>
              <option value="7d" style={{ background: '#1a1a2e' }}>7 Days</option>
              <option value="15d" style={{ background: '#1a1a2e' }}>15 Days</option>
              <option value="30d" style={{ background: '#1a1a2e' }}>30 Days</option>
            </select>
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', fontSize: '13px', color: '#aaa', marginBottom: '6px' }}>License Keys (one per line or comma-separated)</label>
            <textarea value={keysInput} onChange={e => setKeysInput(e.target.value)} required
              placeholder="Paste keys here..."
              rows={6}
              style={{
                width: '100%', padding: '12px 14px', background: 'rgba(255,255,255,0.06)',
                border: '1px solid #333', borderRadius: '10px', color: 'white',
                fontSize: '13px', outline: 'none', boxSizing: 'border-box', fontFamily: 'monospace',
                resize: 'vertical'
              }}
            />
          </div>

          <div style={{ display: 'flex', gap: '10px' }}>
            <button type="button" onClick={onClose} style={{
              flex: 1, padding: '12px', background: 'rgba(255,255,255,0.06)',
              border: '1px solid #333', borderRadius: '10px', color: '#aaa',
              fontSize: '14px', cursor: 'pointer'
            }}>Cancel</button>
            <button type="submit" className="btn-primary" style={{
              flex: 1, padding: '12px', borderRadius: '10px', fontSize: '14px',
              cursor: 'pointer', border: 'none'
            }}>Add Keys</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function KeysClient({ initialProducts }) {
  const [modalOpen, setModalOpen] = useState(false);
  const router = useRouter();

  const handleSave = async (product, duration, keysArray) => {
    await addKeys(product, duration, keysArray);
    alert(`Successfully added ${keysArray.length} keys for ${product.toUpperCase()} (${duration})!`);
    setModalOpen(false);
    router.refresh();
  };

  return (
    <>
      <KeyModal 
        isOpen={modalOpen} 
        onClose={() => setModalOpen(false)} 
        onSave={handleSave} 
        productsList={initialProducts}
      />

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <div>
          <h1 style={{ fontSize: '24px', margin: '0 0 5px 0' }}>Key Management</h1>
          <p style={{ color: 'var(--text-muted)', margin: 0, fontSize: '14px' }}>Manage all your bot keys across different products.</p>
        </div>
        <button onClick={() => setModalOpen(true)} className="btn-primary" style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <Plus size={16} /> Add New Keys
        </button>
      </div>

      {/* Overview Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px', marginBottom: '30px' }}>
        {initialProducts.slice(0, 4).map((p, idx) => (
          <div key={idx} className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '15px' }}>
              <div style={{ background: 'rgba(0, 210, 255, 0.1)', padding: '10px', borderRadius: '10px' }}>
                <Key size={20} color="var(--primary)" />
              </div>
              <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Stock</span>
            </div>
            <h3 style={{ margin: '0 0 5px 0', fontSize: '24px' }}>{p.count}</h3>
            <p style={{ margin: 0, color: 'var(--text-muted)', fontSize: '13px' }}>{p.name.toUpperCase()}</p>
          </div>
        ))}
        {initialProducts.length === 0 && (
          <div className="card">
            <p style={{ margin: 0, color: 'var(--text-muted)', fontSize: '13px' }}>No keys found</p>
          </div>
        )}
      </div>

      {/* Main Table Area */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h3 style={{ margin: 0, fontSize: '16px' }}>Key Inventory</h3>
          
          <div style={{ display: 'flex', gap: '15px' }}>
            <div style={{ position: 'relative' }}>
              <Search size={16} color="var(--text-muted)" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
              <input type="text" placeholder="Search keys or products..." style={{ background: '#111', border: '1px solid #333', color: 'white', padding: '8px 12px 8px 35px', borderRadius: '8px', outline: 'none', fontSize: '14px', width: '250px' }} />
            </div>
          </div>
        </div>

        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '14px' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid #222', color: 'var(--text-muted)' }}>
              <th style={{ padding: '15px 10px', fontWeight: 'normal' }}>Product & Duration</th>
              <th style={{ padding: '15px 10px', fontWeight: 'normal' }}>Total Keys</th>
              <th style={{ padding: '15px 10px', fontWeight: 'normal' }}>Sample Keys</th>
              <th style={{ padding: '15px 10px', fontWeight: 'normal', textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {initialProducts.map((product, idx) => (
              <tr key={idx} style={{ borderBottom: '1px solid #222' }}>
                <td style={{ padding: '15px 10px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <div style={{ width: '36px', height: '36px', background: '#111', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid #333' }}>
                      <Key size={16} color="var(--text-muted)" />
                    </div>
                    <div>
                      <div style={{ fontWeight: '500' }}>{product.name.toUpperCase()}</div>
                    </div>
                  </div>
                </td>
                <td style={{ padding: '15px 10px' }}>
                  <span style={{ background: 'rgba(0, 210, 255, 0.1)', color: 'var(--primary)', padding: '4px 10px', borderRadius: '12px', fontSize: '12px', fontWeight: '500' }}>
                    {product.count} in stock
                  </span>
                </td>
                <td style={{ padding: '15px 10px', color: 'var(--text-muted)', fontSize: '13px' }}>
                  {product.keys.length > 0 ? (
                    <div>
                      <code>{product.keys[0]}</code>
                      {product.keys.length > 1 && <span>, ...</span>}
                    </div>
                  ) : "None"}
                </td>
                <td style={{ padding: '15px 10px', textAlign: 'right' }}>
                  <button onClick={() => alert("Deletion will be implemented later!")} style={{ background: 'transparent', border: '1px solid var(--danger)', color: 'var(--danger)', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer' }}>
                    <Trash2 size={14}/>
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}

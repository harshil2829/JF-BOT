"use client";

import { useState } from 'react';
import { Package, Plus, Edit2, Trash2, X } from 'lucide-react';
import { addProduct, deleteProduct, editProduct } from '../../actions';
import { useRouter } from 'next/navigation';

function ProductModal({ isOpen, onClose, onSave, editData }) {
  const [name, setName] = useState(editData?.name || '');
  const [p1d, setP1d] = useState(editData?.prices?.['1d'] || 50);
  const [p7d, setP7d] = useState(editData?.prices?.['7d'] || 200);
  const [p15d, setP15d] = useState(editData?.prices?.['15d'] || 400);
  const [p30d, setP30d] = useState(editData?.prices?.['30d'] || 600);
  const [section, setSection] = useState(editData?.section || 'Both');

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({
      name,
      prices: { '1d': parseFloat(p1d), '7d': parseFloat(p7d), '15d': parseFloat(p15d), '30d': parseFloat(p30d) },
      section,
      status: editData?.status || 'Active'
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
        background: 'var(--card-bg, #1a1a2e)', border: '1px solid var(--border, #333)',
        borderRadius: '16px', padding: '30px', width: '100%', maxWidth: '450px',
        boxShadow: '0 20px 60px rgba(0,0,0,0.5)'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '25px' }}>
          <h2 style={{ margin: 0, fontSize: '20px' }}>{editData ? '✏️ Edit Product' : '➕ Add Product'}</h2>
          <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: '#aaa', cursor: 'pointer', padding: '5px' }}>
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', fontSize: '13px', color: '#aaa', marginBottom: '6px' }}>Product Name</label>
            <input value={name} onChange={e => setName(e.target.value)} required
              placeholder="e.g. HXN, Alpha, Prime..."
              style={{
                width: '100%', padding: '12px 14px', background: 'rgba(255,255,255,0.06)',
                border: '1px solid var(--border, #333)', borderRadius: '10px', color: 'white',
                fontSize: '14px', outline: 'none', boxSizing: 'border-box'
              }}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '15px' }}>
            {[
              { label: '1 Day Price (₹)', val: p1d, set: setP1d },
              { label: '7 Day Price (₹)', val: p7d, set: setP7d },
              { label: '15 Day Price (₹)', val: p15d, set: setP15d },
              { label: '30 Day Price (₹)', val: p30d, set: setP30d },
            ].map((field, i) => (
              <div key={i}>
                <label style={{ display: 'block', fontSize: '12px', color: '#aaa', marginBottom: '5px' }}>{field.label}</label>
                <input type="number" value={field.val} onChange={e => field.set(e.target.value)} required
                  style={{
                    width: '100%', padding: '10px 12px', background: 'rgba(255,255,255,0.06)',
                    border: '1px solid var(--border, #333)', borderRadius: '10px', color: 'white',
                    fontSize: '14px', outline: 'none', boxSizing: 'border-box'
                  }}
                />
              </div>
            ))}
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', fontSize: '13px', color: '#aaa', marginBottom: '6px' }}>Section</label>
            <select value={section} onChange={e => setSection(e.target.value)}
              style={{
                width: '100%', padding: '12px 14px', background: 'rgba(255,255,255,0.06)',
                border: '1px solid var(--border, #333)', borderRadius: '10px', color: 'white',
                fontSize: '14px', outline: 'none', boxSizing: 'border-box'
              }}
            >
              <option value="Both" style={{ background: '#1a1a2e' }}>Both (Trial + Selling)</option>
              <option value="Trial" style={{ background: '#1a1a2e' }}>Trial Only</option>
              <option value="Selling" style={{ background: '#1a1a2e' }}>Selling Only</option>
            </select>
          </div>

          <div style={{ display: 'flex', gap: '10px' }}>
            <button type="button" onClick={onClose} style={{
              flex: 1, padding: '12px', background: 'rgba(255,255,255,0.06)',
              border: '1px solid var(--border, #333)', borderRadius: '10px', color: '#aaa',
              fontSize: '14px', cursor: 'pointer'
            }}>Cancel</button>
            <button type="submit" className="btn-primary" style={{
              flex: 1, padding: '12px', borderRadius: '10px', fontSize: '14px',
              cursor: 'pointer', border: 'none'
            }}>{editData ? 'Save Changes' : 'Add Product'}</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function ProductsClient({ initialProducts }) {
  const [products, setProducts] = useState(initialProducts || []);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const router = useRouter();

  const handleSave = async (product) => {
    if (editingProduct) {
      await editProduct(editingProduct.name, product);
      setProducts(products.map(p => p.name === editingProduct.name ? product : p));
    } else {
      await addProduct(product);
      setProducts([...products, product]);
    }
    setModalOpen(false);
    setEditingProduct(null);
    router.refresh();
  };

  const handleEdit = (p) => {
    setEditingProduct(p);
    setModalOpen(true);
  };

  const handleDelete = async (name) => {
    if (confirm(`Are you sure you want to delete ${name}?`)) {
      await deleteProduct(name);
      setProducts(products.filter(p => p.name !== name));
      router.refresh();
    }
  };

  return (
    <>
      <ProductModal 
        isOpen={modalOpen} 
        onClose={() => { setModalOpen(false); setEditingProduct(null); }}
        onSave={handleSave}
        editData={editingProduct}
        key={editingProduct ? editingProduct.name : 'new'}
      />

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px', flexWrap: 'wrap', gap: '15px' }}>
        <div>
          <h1 style={{ fontSize: '24px', margin: '0 0 5px 0' }}>Product Management</h1>
          <p style={{ color: 'var(--text-muted)', margin: 0, fontSize: '14px' }}>Add, edit, or remove bot products and subscription plans.</p>
        </div>
        <button onClick={() => { setEditingProduct(null); setModalOpen(true); }} className="btn-primary" style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <Plus size={16}/> Add Product
        </button>
      </div>
      
      {/* Desktop Table */}
      <div className="card" style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '14px', minWidth: '500px' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--border)', color: 'var(--text-muted)' }}>
              <th style={{ padding: '15px 10px', fontWeight: 500 }}>Product Name</th>
              <th style={{ padding: '15px 10px', fontWeight: 500 }}>Prices</th>
              <th style={{ padding: '15px 10px', fontWeight: 500 }}>Section</th>
              <th style={{ padding: '15px 10px', fontWeight: 500 }}>Status</th>
              <th style={{ padding: '15px 10px', fontWeight: 500, textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {products.map((p, i) => (
              <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                <td style={{ padding: '15px 10px', fontWeight: 600 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <div style={{ background: 'rgba(0, 210, 255, 0.1)', padding: '8px', borderRadius: '8px', flexShrink: 0 }}>
                      <Package size={16} color="var(--primary)" />
                    </div>
                    {p.name}
                  </div>
                </td>
                <td style={{ padding: '15px 10px', color: 'var(--success)', fontSize: '12px' }}>
                  {p.prices 
                    ? <>1d: ₹{p.prices['1d']} | 7d: ₹{p.prices['7d']} | 15d: ₹{p.prices['15d']} | 30d: ₹{p.prices['30d']}</>
                    : `₹${p.price}`}
                </td>
                <td style={{ padding: '15px 10px', color: '#b388ff' }}>{p.section || 'Both'}</td>
                <td style={{ padding: '15px 10px' }}><span className="badge positive">{p.status}</span></td>
                <td style={{ padding: '15px 10px', textAlign: 'right', whiteSpace: 'nowrap' }}>
                  <button onClick={() => handleEdit(p)} style={{ background: 'transparent', border: '1px solid #333', color: 'white', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer', marginRight: '10px' }}><Edit2 size={14}/></button>
                  <button onClick={() => handleDelete(p.name)} style={{ background: 'transparent', border: '1px solid var(--danger)', color: 'var(--danger)', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer' }}><Trash2 size={14}/></button>
                </td>
              </tr>
            ))}
            {products.length === 0 && (
              <tr><td colSpan="5" style={{ padding: '20px', textAlign: 'center', color: 'var(--text-muted)' }}>No products found</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  );
}

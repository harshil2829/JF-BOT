"use client";

import { useState } from 'react';
import { Key, Gift, Users, Crown, Settings2, Globe, Wrench, Save } from 'lucide-react';
import { saveSettings } from '../actions';
import { useRouter } from 'next/navigation';

export default function SettingsClient({ initialSettings }) {
  const router = useRouter();
  const [settings, setSettings] = useState(initialSettings || {
    key_claiming: true,
    max_keys_per_day: 'Unlimited',
    auto_expiry_warnings: true,
    daily_rewards: false,
    weekly_bonus: '1x (No bonus)',
    referral_multiplier: '1x (Normal)',
    vip_multiplier: '1.5x',
    maintenance_mode: false
  });
  const [saving, setSaving] = useState(false);

  const toggle = (key) => {
    setSettings(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const handleChange = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const handleSave = async () => {
    setSaving(true);
    await saveSettings(settings);
    alert("Settings saved to MongoDB successfully!");
    setSaving(false);
    router.refresh();
  };

  const ToggleSwitch = ({ checked, onClick }) => (
    <div onClick={onClick} style={{ background: checked ? 'var(--primary)' : '#333', width: '44px', height: '24px', borderRadius: '12px', position: 'relative', cursor: 'pointer', transition: 'background 0.3s' }}>
      <div style={{ background: checked ? 'white' : '#666', width: '20px', height: '20px', borderRadius: '50%', position: 'absolute', left: checked ? '22px' : '2px', top: '2px', transition: 'left 0.3s' }}></div>
    </div>
  );

  return (
    <>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <div>
          <h1 style={{ fontSize: '24px', margin: '0 0 5px 0' }}>Settings</h1>
          <p style={{ color: 'var(--text-muted)', margin: 0, fontSize: '14px' }}>Configure your bot behavior</p>
        </div>
        <button onClick={handleSave} disabled={saving} className="btn-primary" style={{ display: 'flex', gap: '8px', alignItems: 'center', opacity: saving ? 0.7 : 1 }}>
          <Save size={16}/> {saving ? 'Saving...' : 'Save Changes'}
        </button>
      </div>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>
        
        {/* Key Settings */}
        <div className="card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '25px' }}>
            <div style={{ background: 'rgba(0, 210, 255, 0.1)', padding: '10px', borderRadius: '10px' }}>
              <Key size={20} color="var(--primary)" />
            </div>
            <div>
              <h3 style={{ margin: '0 0 5px 0', fontSize: '16px' }}>Key Settings</h3>
              <p style={{ margin: 0, fontSize: '12px', color: 'var(--text-muted)' }}>Configure key claiming behavior</p>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <div>
              <p style={{ margin: '0 0 5px 0', fontSize: '14px', fontWeight: 600 }}>Key Claiming</p>
              <p style={{ margin: 0, fontSize: '12px', color: 'var(--text-muted)' }}>Allow users to claim keys</p>
            </div>
            <ToggleSwitch checked={settings.key_claiming} onClick={() => toggle('key_claiming')} />
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <div>
              <p style={{ margin: '0 0 5px 0', fontSize: '14px', fontWeight: 600 }}>Max Keys Per Day</p>
              <p style={{ margin: 0, fontSize: '12px', color: 'var(--text-muted)' }}>Daily limit for key claims</p>
            </div>
            <select value={settings.max_keys_per_day} onChange={e => handleChange('max_keys_per_day', e.target.value)} style={{ background: '#111', border: '1px solid #333', color: 'white', padding: '8px 12px', borderRadius: '6px', outline: 'none', cursor: 'pointer' }}>
              <option>Unlimited</option>
              <option>1 Key</option>
              <option>5 Keys</option>
            </select>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <p style={{ margin: '0 0 5px 0', fontSize: '14px', fontWeight: 600 }}>Auto Expiry Warnings</p>
              <p style={{ margin: 0, fontSize: '12px', color: 'var(--text-muted)' }}>Notify users before key expiration</p>
            </div>
            <ToggleSwitch checked={settings.auto_expiry_warnings} onClick={() => toggle('auto_expiry_warnings')} />
          </div>
        </div>

        {/* Rewards Settings */}
        <div className="card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '25px' }}>
            <div style={{ background: 'rgba(0, 230, 118, 0.1)', padding: '10px', borderRadius: '10px' }}>
              <Gift size={20} color="var(--success)" />
            </div>
            <div>
              <h3 style={{ margin: '0 0 5px 0', fontSize: '16px' }}>Rewards Settings</h3>
              <p style={{ margin: 0, fontSize: '12px', color: 'var(--text-muted)' }}>Configure rewards and bonuses</p>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <div>
              <p style={{ margin: '0 0 5px 0', fontSize: '14px', fontWeight: 600 }}>Daily Rewards</p>
              <p style={{ margin: 0, fontSize: '12px', color: 'var(--text-muted)' }}>Allow users to claim daily rewards</p>
            </div>
            <ToggleSwitch checked={settings.daily_rewards} onClick={() => toggle('daily_rewards')} />
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <p style={{ margin: '0 0 5px 0', fontSize: '14px', fontWeight: 600 }}>Weekly Bonus Multiplier</p>
              <p style={{ margin: 0, fontSize: '12px', color: 'var(--text-muted)' }}>Bonus points on weekends</p>
            </div>
            <select value={settings.weekly_bonus} onChange={e => handleChange('weekly_bonus', e.target.value)} style={{ background: '#111', border: '1px solid #333', color: 'white', padding: '8px 12px', borderRadius: '6px', outline: 'none', cursor: 'pointer' }}>
              <option>1x (No bonus)</option>
              <option>1.5x</option>
              <option>2x</option>
            </select>
          </div>
        </div>

        {/* Referral Settings */}
        <div className="card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '25px' }}>
            <div style={{ background: 'rgba(41, 121, 255, 0.1)', padding: '10px', borderRadius: '10px' }}>
              <Users size={20} color="#2979ff" />
            </div>
            <div>
              <h3 style={{ margin: '0 0 5px 0', fontSize: '16px' }}>Referral Settings</h3>
              <p style={{ margin: 0, fontSize: '12px', color: 'var(--text-muted)' }}>Configure referral system</p>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <p style={{ margin: '0 0 5px 0', fontSize: '14px', fontWeight: 600 }}>Referral Multiplier</p>
              <p style={{ margin: 0, fontSize: '12px', color: 'var(--text-muted)' }}>Points earned per referral</p>
            </div>
            <select value={settings.referral_multiplier} onChange={e => handleChange('referral_multiplier', e.target.value)} style={{ background: '#111', border: '1px solid #333', color: 'white', padding: '8px 12px', borderRadius: '6px', outline: 'none', cursor: 'pointer' }}>
              <option>1x (Normal)</option>
              <option>2x</option>
            </select>
          </div>
        </div>

        {/* VIP Settings */}
        <div className="card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '25px' }}>
            <div style={{ background: 'rgba(255, 179, 0, 0.1)', padding: '10px', borderRadius: '10px' }}>
              <Crown size={20} color="var(--warning)" />
            </div>
            <div>
              <h3 style={{ margin: '0 0 5px 0', fontSize: '16px' }}>VIP Settings</h3>
              <p style={{ margin: 0, fontSize: '12px', color: 'var(--text-muted)' }}>Configure VIP privileges</p>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <p style={{ margin: '0 0 5px 0', fontSize: '14px', fontWeight: 600 }}>VIP Points Multiplier</p>
              <p style={{ margin: 0, fontSize: '12px', color: 'var(--text-muted)' }}>Bonus multiplier for VIP users</p>
            </div>
            <select value={settings.vip_multiplier} onChange={e => handleChange('vip_multiplier', e.target.value)} style={{ background: '#111', border: '1px solid #333', color: 'white', padding: '8px 12px', borderRadius: '6px', outline: 'none', cursor: 'pointer' }}>
              <option>1.5x</option>
              <option>2x</option>
            </select>
          </div>
        </div>
      </div>

      {/* Advanced Settings */}
      <div className="card" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '25px' }}>
          <div style={{ background: 'rgba(255, 82, 82, 0.1)', padding: '10px', borderRadius: '10px' }}>
            <Settings2 size={20} color="var(--danger)" />
          </div>
          <div>
            <h3 style={{ margin: '0 0 5px 0', fontSize: '16px' }}>Advanced Settings</h3>
            <p style={{ margin: 0, fontSize: '12px', color: 'var(--text-muted)' }}>Advanced configuration options</p>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <div style={{ background: '#111', border: '1px solid #222', borderRadius: '12px', padding: '20px' }}>
            <h4 style={{ display: 'flex', alignItems: 'center', gap: '10px', margin: '0 0 10px 0', fontSize: '14px' }}><Globe size={16}/> Timezone</h4>
            <p style={{ color: 'var(--text-muted)', fontSize: '13px', marginBottom: '15px' }}>Current: UTC</p>
            <button onClick={() => alert("Timezone configuration will be added in the next update!")} style={{ background: 'transparent', border: '1px solid #444', color: 'white', padding: '8px 16px', borderRadius: '8px', cursor: 'pointer', fontSize: '13px' }}>Configure Timezone</button>
          </div>

          <div style={{ background: '#111', border: '1px solid #222', borderRadius: '12px', padding: '20px' }}>
            <h4 style={{ display: 'flex', alignItems: 'center', gap: '10px', margin: '0 0 10px 0', fontSize: '14px' }}><Wrench size={16}/> Maintenance Mode</h4>
            <p style={{ color: 'var(--text-muted)', fontSize: '13px', marginBottom: '15px' }}>Disable bot temporarily for maintenance</p>
            <button onClick={() => toggle('maintenance_mode')} style={{ background: settings.maintenance_mode ? 'var(--success)' : 'var(--danger)', border: 'none', color: 'white', padding: '8px 16px', borderRadius: '8px', cursor: 'pointer', fontSize: '13px' }}>
              {settings.maintenance_mode ? 'Disable Maintenance' : 'Enable Maintenance'}
            </button>
          </div>
        </div>
      </div>
    </>
  );
}

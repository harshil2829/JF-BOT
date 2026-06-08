'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { name: 'Mon', users: 120, keys: 40 },
  { name: 'Tue', users: 132, keys: 55 },
  { name: 'Wed', users: 101, keys: 45 },
  { name: 'Thu', users: 143, keys: 70 },
  { name: 'Fri', users: 190, keys: 100 },
  { name: 'Sat', users: 250, keys: 150 },
  { name: 'Sun', users: 310, keys: 210 },
];

export default function AnalyticsChart() {
  return (
    <div style={{ width: '100%', height: 300, marginTop: '20px' }}>
      <ResponsiveContainer>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
          <XAxis dataKey="name" stroke="#888" tick={{ fill: '#888' }} axisLine={false} tickLine={false} />
          <YAxis stroke="#888" tick={{ fill: '#888' }} axisLine={false} tickLine={false} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #333', borderRadius: '8px' }}
            itemStyle={{ color: '#fff' }}
          />
          <Line type="monotone" dataKey="users" stroke="#00d2ff" strokeWidth={3} dot={{ r: 4, fill: '#00d2ff', strokeWidth: 0 }} activeDot={{ r: 6 }} />
          <Line type="monotone" dataKey="keys" stroke="#b388ff" strokeWidth={3} dot={{ r: 4, fill: '#b388ff', strokeWidth: 0 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, CartesianGrid } from 'recharts';
import { Activity, AlertTriangle } from 'lucide-react';
import { API_BASE } from '../config/api';

export const AnalyticsPage = () => {
  const [incidents, setIncidents] = useState<any[]>([]);

  useEffect(() => {
    axios.get(`${API_BASE}/incidents`).then(res => setIncidents(res.data)).catch(console.error);
  }, []);

  const fireCount = incidents.filter(i => i.type === 'FIRE').length;
  const floodCount = incidents.filter(i => i.type === 'FLOOD').length;
  const smokeCount = incidents.filter(i => i.type === 'SMOKE').length;
  const activeCount = incidents.filter(i => i.status !== 'RESOLVED').length;
  const resolvedCount = incidents.filter(i => i.status === 'RESOLVED').length;

  const typeData = [
    { name: 'FIRE', count: fireCount },
    { name: 'FLOOD', count: floodCount },
    { name: 'SMOKE', count: smokeCount },
  ];

  const timelineData = incidents.reduce((acc, curr) => {
    const date = new Date(curr.created_at).toLocaleDateString();
    const existing = acc.find((item: any) => item.date === date);
    if (existing) {
      existing.incidents++;
    } else {
      acc.push({ date, incidents: 1 });
    }
    return acc;
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold flex items-center gap-3">
        <Activity className="text-primary" /> Analytics & Intelligence
      </h1>

      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-surface border border-gray-800 rounded-xl p-4 text-center">
          <p className="text-gray-400 text-xs mb-1">Total Incidents</p>
          <p className="text-2xl font-bold text-white">{incidents.length}</p>
        </div>
        <div className="bg-surface border border-gray-800 rounded-xl p-4 text-center">
          <p className="text-gray-400 text-xs mb-1">Active</p>
          <p className="text-2xl font-bold text-orange-500">{activeCount}</p>
        </div>
        <div className="bg-surface border border-gray-800 rounded-xl p-4 text-center">
          <p className="text-gray-400 text-xs mb-1">Resolved</p>
          <p className="text-2xl font-bold text-green-500">{resolvedCount}</p>
        </div>
        <div className="bg-surface border border-gray-800 rounded-xl p-4 text-center border-b-4 border-red-500">
          <p className="text-gray-400 text-xs mb-1">Fire</p>
          <p className="text-2xl font-bold text-red-500">{fireCount}</p>
        </div>
        <div className="bg-surface border border-gray-800 rounded-xl p-4 text-center border-b-4 border-blue-500">
          <p className="text-gray-400 text-xs mb-1">Flood</p>
          <p className="text-2xl font-bold text-blue-500">{floodCount}</p>
        </div>
        <div className="bg-surface border border-gray-800 rounded-xl p-4 text-center border-b-4 border-yellow-500">
          <p className="text-gray-400 text-xs mb-1">Smoke</p>
          <p className="text-2xl font-bold text-yellow-500">{smokeCount}</p>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-surface border border-gray-800 rounded-xl p-6 h-96">
          <h2 className="text-xl font-semibold mb-6">Incident Distribution by Type</h2>
          {incidents.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-gray-500">
               <AlertTriangle size={32} className="mb-2 opacity-50" />
               <p>No incidents recorded</p>
            </div>
          ) : (
            <ResponsiveContainer width="100%" height="80%">
              <BarChart data={typeData}>
                <XAxis dataKey="name" stroke="#9CA3AF" />
                <YAxis stroke="#9CA3AF" allowDecimals={false} />
                <Tooltip cursor={{fill: '#374151'}} contentStyle={{backgroundColor: '#1F2937', border: 'none', color: '#fff'}} />
                <Bar dataKey="count" fill="#3B82F6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="bg-surface border border-gray-800 rounded-xl p-6 h-96">
          <h2 className="text-xl font-semibold mb-6">Incidents Over Time</h2>
          {timelineData.length < 2 ? (
            <div className="h-full flex flex-col items-center justify-center text-gray-500">
               <AlertTriangle size={32} className="mb-2 opacity-50" />
               <p>Not enough data for trend analysis</p>
            </div>
          ) : (
            <ResponsiveContainer width="100%" height="80%">
              <LineChart data={timelineData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="date" stroke="#9CA3AF" />
                <YAxis stroke="#9CA3AF" allowDecimals={false} />
                <Tooltip contentStyle={{backgroundColor: '#1F2937', border: 'none', color: '#fff'}} />
                <Line type="monotone" dataKey="incidents" stroke="#EF4444" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>
    </div>
  );
};

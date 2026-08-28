import React, { useEffect, useState } from 'react';
import { Activity, Flame, Droplets, Wind, AlertTriangle } from 'lucide-react';
import axios from 'axios';
import { DisasterMap3D } from '../components/3d/DisasterMap3D';
import { API_BASE, WS_BASE } from '../config/api';

const StatCard = ({ title, value, icon, color }: any) => (
  <div className="bg-surface p-6 rounded-xl border border-gray-800 flex items-center gap-4">
    <div className={`p-4 rounded-lg bg-${color}/10 text-${color}`}>
      {icon}
    </div>
    <div>
      <p className="text-sm text-gray-400">{title}</p>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  </div>
);

export const CommandCenter = () => {
  const [incidents, setIncidents] = useState<any[]>([]);

  useEffect(() => {
    // Fetch initial data
    axios.get(`${API_BASE}/incidents`).then(res => setIncidents(res.data)).catch(console.error);

    // Setup WebSocket
    const ws = new WebSocket(WS_BASE);
    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.type === 'NEW_INCIDENT') {
        axios.get(`${API_BASE}/incidents`).then(res => setIncidents(res.data)).catch(console.error);
      }
    };
    return () => ws.close();
  }, []);

  const activeIncidents = incidents.filter(i => i.status !== 'RESOLVED');

  return (
    <div className="space-y-6">
      <header className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Command Center</h1>
        <div className="flex gap-4">
          <button className="bg-primary hover:bg-blue-600 px-4 py-2 rounded-lg font-medium transition-colors">
            Generate Report
          </button>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard title="Active Incidents" value={activeIncidents.length} icon={<AlertTriangle size={24} />} color="warning" />
        <StatCard title="Fire Alerts" value={activeIncidents.filter(i => i.type === 'FIRE').length} icon={<Flame size={24} />} color="critical" />
        <StatCard title="Flood Alerts" value={activeIncidents.filter(i => i.type === 'FLOOD').length} icon={<Droplets size={24} />} color="primary" />
        <StatCard title="Smoke/Air" value={activeIncidents.filter(i => i.type === 'SMOKE').length} icon={<Wind size={24} />} color="safe" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[600px]">
        <div className="lg:col-span-2 bg-surface rounded-xl border border-gray-800 p-4 flex flex-col">
          <h2 className="text-lg font-semibold mb-4">Live Threat Map</h2>
          <div className="flex-1 bg-gray-900 rounded-lg flex items-center justify-center border border-gray-800 relative overflow-hidden">
             <DisasterMap3D incidents={incidents} />
          </div>
        </div>

        {/* Incident Feed */}
        <div className="bg-surface rounded-xl border border-gray-800 p-4 flex flex-col">
          <h2 className="text-lg font-semibold mb-4">Recent Incidents</h2>
          <div className="flex-1 overflow-y-auto space-y-3">
            {incidents.length === 0 ? (
              <p className="text-gray-500 text-center mt-10">No recent incidents</p>
            ) : (
              incidents.slice(0, 10).map((inc) => (
                <div key={inc.id} className="p-3 bg-gray-900 rounded-lg border border-gray-800">
                  <div className="flex justify-between items-start mb-2">
                    <div className="flex items-center gap-2">
                      <span className={`text-xs font-bold px-2 py-1 rounded bg-opacity-20 ${
                        inc.type === 'FIRE' ? 'text-red-400 bg-red-400' : 
                        inc.type === 'FLOOD' ? 'text-blue-400 bg-blue-400' : 'text-orange-400 bg-orange-400'
                      }`}>
                        {inc.type}
                      </span>
                      <span className={`text-xs font-bold px-2 py-1 rounded bg-opacity-20 ${
                        inc.severity === 'CRITICAL' ? 'text-red-500 bg-red-500' : 
                        inc.severity === 'HIGH' ? 'text-orange-500 bg-orange-500' : 'text-yellow-500 bg-yellow-500'
                      }`}>
                        {inc.severity}
                      </span>
                    </div>
                    <span className="text-xs text-gray-500">{new Date(inc.created_at).toLocaleTimeString()}</span>
                  </div>
                  
                  <p className="text-sm mb-2">{inc.description}</p>
                  
                  <div className="bg-gray-800 p-2 rounded text-xs">
                    <p className="text-gray-400 mb-1">Evidence Score: <span className="text-white font-bold">{inc.evidence_score || 'N/A'}</span></p>
                    <p className="text-gray-400 mb-1">Source: <span className="text-white">{inc.source}</span></p>
                    {inc.evidence_details && inc.evidence_details.sensors && (
                       <ul className="list-disc list-inside text-gray-300 mt-1">
                         {inc.evidence_details.sensors.map((ev: string, i: number) => <li key={i}>{ev}</li>)}
                       </ul>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

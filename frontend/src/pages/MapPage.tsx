import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { DisasterMap3D } from '../components/3d/DisasterMap3D';
import { Map, AlertCircle } from 'lucide-react';
import { API_BASE } from '../config/api';

export const MapPage = () => {
  const [incidents, setIncidents] = useState<any[]>([]);

  useEffect(() => {
    axios.get(`${API_BASE}/incidents`)
      .then(res => setIncidents(res.data))
      .catch(console.error);
  }, []);

  const activeIncidents = incidents.filter(i => i.status !== 'RESOLVED');

  return (
    <div className="space-y-6 h-[calc(100vh-6rem)] flex flex-col">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <Map className="text-primary" /> Live Disaster Map
        </h1>
        {activeIncidents.length === 0 ? (
          <div className="flex items-center gap-2 text-green-400 bg-green-400/10 px-4 py-2 rounded-lg border border-green-400/20">
            <AlertCircle size={18} /> No Active Incidents
          </div>
        ) : (
          <div className="flex items-center gap-2 text-red-500 bg-red-500/10 px-4 py-2 rounded-lg border border-red-500/20">
            <AlertCircle size={18} /> {activeIncidents.length} Active Incident(s)
          </div>
        )}
      </div>
      
      <div className="flex-1 rounded-xl overflow-hidden border border-gray-800 bg-surface relative">
        <DisasterMap3D incidents={incidents} />
      </div>
    </div>
  );
};

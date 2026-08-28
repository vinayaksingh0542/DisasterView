import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Radio, Battery, Wifi, Cpu, AlertTriangle } from 'lucide-react';
import { API_BASE } from '../config/api';

export const DevicesPage = () => {
  const [devices, setDevices] = useState<any[]>([]);

  useEffect(() => {
    axios.get(`${API_BASE}/devices`)
      .then(res => setDevices(res.data))
      .catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold flex items-center gap-3">
        <Cpu className="text-primary" /> Hardware & Edge Devices
      </h1>
      
      {devices.length === 0 ? (
        <div className="bg-surface border border-gray-800 rounded-xl p-8 text-center text-gray-500">
          <AlertTriangle size={48} className="mx-auto mb-4 opacity-50" />
          <h2 className="text-xl font-bold text-gray-300 mb-2">No Connected Devices</h2>
          <p>ESP32 hardware is currently disconnected or not registered.</p>
          
          <div className="max-w-md mx-auto mt-8 bg-gray-900 border border-gray-800 rounded-lg p-6 text-left">
            <h3 className="font-bold text-gray-300 mb-4 border-b border-gray-700 pb-2">Hardware Telemetry Status</h3>
            <div className="space-y-3 font-mono text-sm">
              <div className="flex justify-between text-red-400">
                <span>ESP32 STATUS:</span> <span>OFFLINE</span>
              </div>
              <div className="flex justify-between text-gray-500">
                <span>DHT22:</span> <span>WAITING FOR DEVICE</span>
              </div>
              <div className="flex justify-between text-gray-500">
                <span>MQ135:</span> <span>WAITING FOR DEVICE</span>
              </div>
              <div className="flex justify-between text-gray-500">
                <span>MQ9:</span> <span>WAITING FOR DEVICE</span>
              </div>
              <div className="flex justify-between text-gray-500">
                <span>FLAME SENSOR:</span> <span>WAITING FOR DEVICE</span>
              </div>
              <div className="flex justify-between text-gray-500">
                <span>HC-SR04:</span> <span>WAITING FOR DEVICE</span>
              </div>
              <div className="flex justify-between text-gray-500 pt-2 border-t border-gray-800">
                <span>Edge AI Runtime:</span> <span>CHECKING...</span>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {devices.map(dev => (
            <div key={dev.id} className="bg-surface border border-gray-800 rounded-xl p-6 relative overflow-hidden">
              <div className={`absolute top-0 left-0 w-1 h-full ${dev.status === 'ONLINE' ? 'bg-safe' : 'bg-critical'}`}></div>
              
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-bold flex items-center gap-2">
                    <Radio size={18} className="text-primary" /> {dev.name}
                  </h3>
                  <p className="text-sm text-gray-400">ID: {dev.id}</p>
                </div>
                <div className="flex flex-col items-end">
                  <span className={`px-2 py-1 rounded text-xs font-bold ${
                    dev.status === 'ONLINE' ? 'bg-safe/20 text-safe' : 'bg-critical/20 text-critical'
                  }`}>
                    {dev.status || 'OFFLINE'}
                  </span>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4 text-sm mt-6">
                <div className="flex items-center gap-2 text-gray-300">
                  <Wifi size={16} /> Signal: -65dBm
                </div>
                <div className="flex items-center gap-2 text-gray-300">
                  <Battery size={16} /> {dev.battery_level || 0}%
                </div>
                <div className="col-span-2 mt-2 pt-4 border-t border-gray-800 text-xs text-gray-500 flex justify-between">
                  <span>Location: {dev.location}</span>
                  <span>Last ping: {new Date(dev.last_seen).toLocaleTimeString()}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

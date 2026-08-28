import React, { useState } from 'react';
import axios from 'axios';
import { Play, Activity, CheckCircle } from 'lucide-react';
import { API_BASE } from '../config/api';

export const SettingsPage = () => {
  const [demoStatus, setDemoStatus] = useState('');

  const triggerSimulation = async (type: string) => {
    setDemoStatus(`Triggering ${type} simulation...`);
    try {
      let payload: any = {
        device_id: 'demo-node-01',
        flame_detected: false,
        temperature: 25.0,
        humidity: 50.0,
        water_distance_cm: 200.0,
        mq135_air_quality: 100.0,
        mq9_gas_level: 100.0,
      };

      if (type === 'FIRE') {
        payload.flame_detected = true;
        payload.temperature = 85.0;
        payload.mq9_gas_level = 550.0;
        payload.mq135_air_quality = 300.0;
      } else if (type === 'FLOOD') {
        payload.water_distance_cm = 10.0; // Water level 190cm above baseline
      } else if (type === 'SMOKE') {
        payload.mq135_air_quality = 850.0;
        payload.mq9_gas_level = 250.0;
        payload.temperature = 32.0;
      } else if (type === 'WEAK_EVIDENCE') {
        // Only one marginal sensor reading; below multi-sensor fusion threshold
        payload.temperature = 42.0; // Warm, but no flame, no gas
        payload.mq135_air_quality = 180.0;
      }
      
      const res = await axios.post(`${API_BASE}/sensors`, payload);
      if (res.data.incident_created) {
        setDemoStatus(`${type} generated incident via Sensor Fusion!`);
      } else {
        setDemoStatus(`${type} processed: Normal baseline / No incident triggered (Correct behaviour).`);
      }
      setTimeout(() => setDemoStatus(''), 4000);
    } catch (e) {
      setDemoStatus('Error triggering simulation.');
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Settings & Demo Mode</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-surface border border-gray-800 rounded-xl p-6 space-y-4">
          <h2 className="text-xl font-semibold flex items-center gap-2">
            <Play className="text-primary" /> Live Demo Control Panel (SIMULATED TELEMETRY)
          </h2>
          <p className="text-gray-400 text-sm">
            Use these controls to inject realistic simulated sensor payloads through the <code>/api/sensors</code> endpoint. The exact same Sensor Fusion engine evaluates physical ESP32 packets and these simulation events.
          </p>
          
          <div className="space-y-3">
            <button 
              onClick={() => triggerSimulation('FIRE')}
              className="w-full bg-red-500/10 hover:bg-red-500/20 text-red-500 border border-red-500/50 py-3 rounded-lg font-medium transition-colors"
            >
              Simulate Fire Event (Flame + Elevated Temp + MQ9)
            </button>
            <button 
              onClick={() => triggerSimulation('FLOOD')}
              className="w-full bg-blue-500/10 hover:bg-blue-500/20 text-blue-500 border border-blue-500/50 py-3 rounded-lg font-medium transition-colors"
            >
              Simulate Flood Event (HC-SR04 Water Distance 10cm)
            </button>
            <button 
              onClick={() => triggerSimulation('SMOKE')}
              className="w-full bg-orange-500/10 hover:bg-orange-500/20 text-orange-500 border border-orange-500/50 py-3 rounded-lg font-medium transition-colors"
            >
              Simulate Hazardous Air/Smoke (MQ135 &gt; 800)
            </button>
            <button 
              onClick={() => triggerSimulation('WEAK_EVIDENCE')}
              className="w-full bg-yellow-500/10 hover:bg-yellow-500/20 text-yellow-500 border border-yellow-500/50 py-3 rounded-lg font-medium transition-colors"
            >
              Simulate Weak Evidence / Non-Hazard (Temp 42°C, No Alarm)
            </button>
            <button 
              onClick={() => triggerSimulation('NORMAL')}
              className="w-full bg-green-500/10 hover:bg-green-500/20 text-green-500 border border-green-500/50 py-3 rounded-lg font-medium transition-colors"
            >
              Simulate Normal Baseline (All Clean)
            </button>
          </div>

          {demoStatus && (
            <div className="flex items-center gap-2 text-sm text-green-400 bg-green-400/10 p-3 rounded-lg">
              <CheckCircle size={16} /> {demoStatus}
            </div>
          )}
        </div>

        <div className="bg-surface border border-gray-800 rounded-xl p-6 space-y-4">
          <h2 className="text-xl font-semibold flex items-center gap-2">
            <Activity className="text-primary" /> Edge Hardware Configuration
          </h2>
          <div className="space-y-4 text-sm text-gray-300">
             <div className="flex justify-between items-center pb-2 border-b border-gray-800">
               <span>MQTT Broker URL</span>
               <input type="text" value="tcp://broker.hivemq.com:1883" className="bg-gray-900 border border-gray-700 rounded px-2 py-1 text-white" readOnly />
             </div>
             <div className="flex justify-between items-center pb-2 border-b border-gray-800">
               <span>Telemetry Interval (ms)</span>
               <input type="number" value="5000" className="bg-gray-900 border border-gray-700 rounded px-2 py-1 text-white w-24" readOnly />
             </div>
             <div className="flex justify-between items-center pb-2 border-b border-gray-800">
               <span>Flood Distance Reference (cm)</span>
               <input type="number" value="200" className="bg-gray-900 border border-gray-700 rounded px-2 py-1 text-white w-24" />
             </div>
             <button className="bg-primary hover:bg-blue-600 px-4 py-2 rounded-lg font-medium transition-colors w-full mt-4">
               Save Configuration
             </button>
          </div>
        </div>
      </div>
    </div>
  );
};

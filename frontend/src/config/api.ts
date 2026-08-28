// Production & Development API Configuration for Team Apex 07 DisasterView
const isProd = import.meta.env.PROD;

export const API_BASE = import.meta.env.VITE_API_BASE || (isProd ? '/api' : 'http://localhost:8000/api');

export const WS_BASE = import.meta.env.VITE_WS_BASE || (
  isProd 
    ? `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws`
    : 'ws://localhost:8000/ws'
);

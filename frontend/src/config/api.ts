// Production & Development API Configuration for Team Apex 07 DisasterView
const isProd = import.meta.env.PROD;
 
export const API_BASE = import.meta.env.VITE_API_BASE || (
  isProd
    ? 'https://disasterview-8dvy.onrender.com/api'
    : 'http://localhost:8000/api'
);
 
export const WS_BASE = import.meta.env.VITE_WS_BASE || (
  isProd
    ? 'wss://disasterview-8dvy.onrender.com/ws'
    : 'ws://localhost:8000/ws'
);


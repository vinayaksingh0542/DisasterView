import React from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { ShieldAlert, Map, Activity, Camera, Settings, LayoutDashboard, Radio } from 'lucide-react';

const Sidebar = () => {
  const location = useLocation();
  const links = [
    { name: 'Command Center', path: '/', icon: <LayoutDashboard size={20} /> },
    { name: 'Live Map', path: '/map', icon: <Map size={20} /> },
    { name: 'Incidents', path: '/incidents', icon: <ShieldAlert size={20} /> },
    { name: 'Hardware / Edge', path: '/devices', icon: <Radio size={20} /> },
    { name: 'AI / Vision Demo', path: '/cameras', icon: <Camera size={20} /> },
    { name: 'Analytics', path: '/analytics', icon: <Activity size={20} /> },
    { name: 'Settings', path: '/settings', icon: <Settings size={20} /> },
  ];

  return (
    <div className="w-64 h-screen bg-surface border-r border-gray-800 flex flex-col">
      <div className="p-6 flex items-center gap-3">
        <ShieldAlert className="text-primary" size={28} />
        <span className="text-xl font-bold tracking-wider">DISASTERVIEW</span>
      </div>
      <nav className="flex-1 px-4 py-6 space-y-2">
        {links.map((link) => (
          <Link
            key={link.path}
            to={link.path}
            className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
              location.pathname === link.path ? 'bg-primary/10 text-primary' : 'hover:bg-gray-800 text-gray-400 hover:text-white'
            }`}
          >
            {link.icon}
            <span className="font-medium">{link.name}</span>
          </Link>
        ))}
      </nav>
      <div className="p-4 border-t border-gray-800 text-xs text-gray-500">
        System Status: <span className="text-safe font-bold">ONLINE</span>
      </div>
    </div>
  );
};

export const DashboardLayout = () => {
  return (
    <div className="flex h-screen bg-background text-white overflow-hidden">
      <Sidebar />
      <main className="flex-1 overflow-auto p-6 relative">
        <Outlet />
      </main>
    </div>
  );
};

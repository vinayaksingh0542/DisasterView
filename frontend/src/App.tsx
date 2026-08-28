import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { DashboardLayout } from './layouts/DashboardLayout';
import { CommandCenter } from './pages/CommandCenter';
import { SettingsPage } from './pages/SettingsPage';
import { CamerasPage } from './pages/CamerasPage';
import { IncidentsPage } from './pages/IncidentsPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { DevicesPage } from './pages/DevicesPage';
import { MapPage } from './pages/MapPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<DashboardLayout />}>
          <Route index element={<CommandCenter />} />
          <Route path="map" element={<MapPage />} />
          <Route path="incidents" element={<IncidentsPage />} />
          <Route path="devices" element={<DevicesPage />} />
          <Route path="cameras" element={<CamerasPage />} />
          <Route path="analytics" element={<AnalyticsPage />} />
          <Route path="settings" element={<SettingsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;

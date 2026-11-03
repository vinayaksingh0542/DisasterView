
import React, { useMemo, useState } from 'react';
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup
} from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

type Incident = {
  id: string | number;
  type?: string;
  severity?: string;
  status?: string;
  lat?: number | string;
  lng?: number | string;
  latitude?: number | string;
  longitude?: number | string;
  temperature?: number;
  humidity?: number;
  water_distance_cm?: number;
  location?: string;
  created_at?: string;
  [key: string]: any;
};

const getCoordinates = (incident: Incident) => {
  const lat = Number(incident.lat ?? incident.latitude);
  const lng = Number(incident.lng ?? incident.longitude);

  if (
    !Number.isFinite(lat) ||
    !Number.isFinite(lng) ||
    lat < -90 || lat > 90 ||
    lng < -180 || lng > 180
  ) {
    return null;
  }

  return { lat, lng };
};

const getColor = (incident: Incident) => {
  const type = (incident.type || '').toUpperCase();
  const severity = (incident.severity || '').toUpperCase();

  if (severity === 'CRITICAL') return '#EF4444';
  if (severity === 'HIGH') return '#F59E0B';
  if (type === 'FIRE') return '#EF4444';
  if (type === 'FLOOD') return '#3B82F6';

  return '#EAB308';
};

const createIcon = (incident: Incident) => {
  const color = getColor(incident);

  return L.divIcon({
    className: 'disaster-map-marker',
    html: `
      <div style="
        width: 22px;
        height: 22px;
        background: ${color};
        border: 3px solid white;
        border-radius: 50%;
        box-shadow: 0 0 14px ${color};
      "></div>
    `,
    iconSize: [22, 22],
    iconAnchor: [11, 11]
  });
};

export const DisasterMap3D = ({
  incidents
}: {
  incidents: Incident[];
}) => {
  const [filter, setFilter] = useState('ALL');

  const activeIncidents = useMemo(
    () => incidents.filter(
      incident => incident.status?.toUpperCase() !== 'RESOLVED'
    ),
    [incidents]
  );

  const mappedIncidents = activeIncidents.filter(incident => {
    const coords = getCoordinates(incident);
    if (!coords) return false;

    if (filter === 'ALL') return true;

    return (incident.type || '').toUpperCase() === filter;
  });

  const filters = ['ALL', 'FLOOD', 'FIRE', 'SMOKE'];

  return (
    <div className="w-full h-full min-h-[450px] bg-gray-950 rounded-lg overflow-hidden relative">

      {/* Map Header */}
      <div className="absolute top-4 left-4 z-[1000] flex flex-wrap gap-2">
        {filters.map(item => (
          <button
            key={item}
            onClick={() => setFilter(item)}
            className={`px-3 py-2 rounded-lg text-xs font-bold border ${
              filter === item
                ? 'bg-blue-600 text-white border-blue-500'
                : 'bg-gray-950/90 text-gray-300 border-gray-700'
            }`}
          >
            {item === 'ALL' ? 'All Incidents' : item}
          </button>
        ))}
      </div>

      {/* Incident Count */}
      <div className="absolute top-4 right-4 z-[1000] bg-gray-950/90 text-white px-3 py-2 rounded-lg border border-gray-700 text-xs">
        Active: {activeIncidents.length}
        <br />
        On Map: {mappedIncidents.length}
      </div>

      {/* Real Geographical Map */}
      <MapContainer
        center={[20.5937, 78.9629]}
        zoom={5}
        minZoom={2}
        maxZoom={18}
        scrollWheelZoom={true}
        className="w-full h-full min-h-[450px]"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {mappedIncidents.map(incident => {
          const coords = getCoordinates(incident);
          if (!coords) return null;

          return (
            <Marker
              key={incident.id}
              position={[coords.lat, coords.lng]}
              icon={createIcon(incident)}
            >
              <Popup>
                <div className="min-w-[180px] text-sm">
                  <h3 className="font-bold text-base mb-2">
                    {incident.type || 'DISASTER'}
                  </h3>

                  <p>
                    <b>Severity:</b> {incident.severity || 'Unknown'}
                  </p>

                  <p>
                    <b>Status:</b> {incident.status || 'Active'}
                  </p>

                  <p>
                    <b>Latitude:</b> {coords.lat}
                  </p>

                  <p>
                    <b>Longitude:</b> {coords.lng}
                  </p>

                  {incident.location && (
                    <p><b>Location:</b> {incident.location}</p>
                  )}

                  {incident.temperature != null && (
                    <p><b>Temperature:</b> {incident.temperature} °C</p>
                  )}

                  {incident.humidity != null && (
                    <p><b>Humidity:</b> {incident.humidity}%</p>
                  )}

                  {incident.water_distance_cm != null && (
                    <p>
                      <b>Water Distance:</b> {incident.water_distance_cm} cm
                    </p>
                  )}

                  {incident.created_at && (
                    <p>
                      <b>Reported:</b>{' '}
                      {new Date(incident.created_at).toLocaleString()}
                    </p>
                  )}
                </div>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>

      {/* Map Legend */}
      <div className="absolute bottom-5 right-5 z-[1000] bg-gray-950/90 border border-gray-700 rounded-lg p-3 text-xs text-white space-y-2">
        <div className="font-bold mb-2">Map Legend</div>

        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-red-500"></span>
          Critical / Fire
        </div>

        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-yellow-500"></span>
          High / Smoke
        </div>

        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-blue-500"></span>
          Flood
        </div>
      </div>

      {mappedIncidents.length === 0 && (
        <div className="absolute bottom-5 left-5 z-[1000] bg-gray-950/90 border border-gray-700 rounded-lg px-3 py-2 text-xs text-gray-300">
          No incidents with valid coordinates to display.
        </div>
      )}
    </div>
  );
};

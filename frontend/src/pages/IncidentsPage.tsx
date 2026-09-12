import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { AlertCircle, XCircle } from 'lucide-react';
import { API_BASE } from '../config/api';

export const IncidentsPage = () => {
  const [incidents, setIncidents] = useState<any[]>([]);

  useEffect(() => {
    fetchIncidents();
  }, []);

  const fetchIncidents = () => {
    axios
      .get(`${API_BASE}/incidents`)
      .then(res => setIncidents(res.data))
      .catch(console.error);
  };

  const updateIncident = async (id: string, status: string) => {
    try {
      await axios.patch(`${API_BASE}/incidents/${id}`, { status });

      setIncidents(
        incidents.map(i =>
          i.id === id ? { ...i, status } : i
        )
      );
    } catch (e) {
      console.error('Failed to update incident:', e);
    }
  };

  // Convert backend UTC timestamp to IST
  const formatISTTime = (timestamp: string) => {
    if (!timestamp) return 'N/A';

    try {
      // Backend currently sends UTC without a timezone suffix.
      // Add Z so JavaScript correctly interprets it as UTC.
      const utcTimestamp = timestamp.endsWith('Z')
        ? timestamp
        : `${timestamp}Z`;

      return new Date(utcTimestamp).toLocaleString('en-IN', {
        timeZone: 'Asia/Kolkata',
        dateStyle: 'medium',
        timeStyle: 'medium',
      });
    } catch (error) {
      console.error('Invalid incident timestamp:', timestamp);
      return 'Invalid time';
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">
        Incident Management
      </h1>

      <div className="bg-surface border border-gray-800 rounded-xl overflow-hidden p-6">
        <table className="w-full text-left">
          <thead>
            <tr className="text-gray-500 border-b border-gray-800">
              <th className="pb-3 font-medium">Time</th>
              <th className="pb-3 font-medium">Type</th>
              <th className="pb-3 font-medium">Severity</th>
              <th className="pb-3 font-medium">Evidence Score</th>
              <th className="pb-3 font-medium">
                Description & Evidence
              </th>
              <th className="pb-3 font-medium">Status</th>
              <th className="pb-3 font-medium">Action</th>
            </tr>
          </thead>

          <tbody className="divide-y divide-gray-800">
            {incidents.map((inc) => (
              <tr key={inc.id}>

                {/* INCIDENT TIME — UTC converted to IST */}
                <td className="py-4 text-sm">
                  {formatISTTime(inc.created_at)}
                </td>

                {/* INCIDENT TYPE */}
                <td className="py-4">
                  <span
                    className={`px-2 py-1 rounded text-xs font-bold bg-opacity-20 ${
                      inc.type === 'FIRE'
                        ? 'text-red-400 bg-red-400'
                        : inc.type === 'FLOOD'
                        ? 'text-blue-400 bg-blue-400'
                        : 'text-yellow-400 bg-yellow-400'
                    }`}
                  >
                    {inc.type}
                  </span>
                </td>

                {/* SEVERITY */}
                <td className="py-4 text-sm font-bold text-gray-300">
                  {inc.severity}
                </td>

                {/* EVIDENCE SCORE */}
                <td className="py-4 text-sm font-bold text-white">
                  {inc.evidence_score || 'N/A'}
                </td>

                {/* DESCRIPTION & SENSOR EVIDENCE */}
                <td className="py-4 text-sm max-w-xs">
                  <p>{inc.description}</p>

                  {inc.evidence_details?.sensors && (
                    <div className="mt-1 text-xs text-gray-400">
                      <strong>Sensors:</strong>{' '}
                      {inc.evidence_details.sensors.join(', ')}
                    </div>
                  )}
                </td>

                {/* STATUS */}
                <td className="py-4">
                  <span
                    className={`px-2 py-1 rounded text-xs ${
                      inc.status === 'RESOLVED'
                        ? 'bg-green-500/20 text-green-400'
                        : 'bg-yellow-500/20 text-yellow-400'
                    }`}
                  >
                    {inc.status}
                  </span>
                </td>

                {/* ACTIONS */}
                <td className="py-4">
                  {inc.status !== 'RESOLVED' && (
                    <button
                      className="text-xs bg-gray-800 hover:bg-gray-700 px-3 py-1 rounded transition-colors"
                      onClick={() =>
                        updateIncident(inc.id, 'RESOLVED')
                      }
                    >
                      Mark Resolved
                    </button>
                  )}

                  {inc.status !== 'DISMISSED' && (
                    <button
                      onClick={() =>
                        updateIncident(inc.id, 'DISMISSED')
                      }
                      className="p-2 bg-gray-500/10 text-gray-400 hover:bg-gray-500/20 rounded transition-colors ml-2"
                      title="Dismiss Alert"
                    >
                      <XCircle size={16} />
                    </button>
                  )}
                </td>
              </tr>
            ))}

            {/* NO INCIDENTS */}
            {incidents.length === 0 && (
              <tr>
                <td
                  colSpan={7}
                  className="p-8 text-center text-gray-500"
                >
                  <AlertCircle
                    size={32}
                    className="mx-auto mb-2 opacity-50"
                  />
                  No incidents recorded.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

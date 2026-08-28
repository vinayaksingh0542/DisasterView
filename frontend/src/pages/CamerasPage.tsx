import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { UploadCloud, Camera, CheckCircle, Cpu } from 'lucide-react';
import { API_BASE } from '../config/api';

export const CamerasPage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [results, setResults] = useState<any[]>([]);
  const [inferenceTime, setInferenceTime] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [modelInfo, setModelInfo] = useState<any>(null);
  
  const imgRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    axios.get(`${API_BASE}/models`)
      .then(res => setModelInfo(res.data.fire_smoke))
      .catch(console.error);
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const f = e.target.files[0];
      setFile(f);
      setPreview(URL.createObjectURL(f));
      setResults([]);
      setInferenceTime(null);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const res = await axios.post(`${API_BASE}/inference`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      if (res.data.error) {
        setError(res.data.error);
      } else {
        setResults(res.data.detections || []);
        setInferenceTime(res.data.inference_time_ms || null);
      }
    } catch (err: any) {
      setError(err.message || 'Inference failed');
    }
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold mb-2">AI Software Demonstration</h1>
          <p className="text-gray-400 max-w-2xl">
            Our primary detection pipeline operates entirely on ESP32 environmental sensors. 
            This page demonstrates the <strong>separate</strong> visual AI software module. 
            In the future, this module could process a live camera feed as optional visual evidence to supplement the core sensor fusion.
            Uploading an image here runs local inference and outputs raw detection results.
          </p>
        </div>
        
        {modelInfo && (
          <div className="bg-surface border border-gray-800 p-4 rounded-xl text-sm min-w-[300px]">
             <h3 className="font-bold flex items-center gap-2 mb-2"><Cpu size={16} className="text-primary"/> Active Model Registry</h3>
             <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-gray-300">
               <span className="text-gray-500">Model:</span> <span>{modelInfo.name}</span>
               <span className="text-gray-500">Framework:</span> <span>{modelInfo.framework}</span>
               <span className="text-gray-500">Runtime:</span> <span className="text-safe">{modelInfo.runtime}</span>
               <span className="text-gray-500">Classes:</span> <span className="text-xs truncate">{modelInfo.expected_classes.join(", ")}</span>
             </div>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-surface border border-gray-800 rounded-xl p-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Camera className="text-primary" /> Test Image Upload
          </h2>
          
          <div className="relative border-2 border-dashed border-gray-700 rounded-lg p-2 flex flex-col items-center justify-center text-center bg-gray-900 min-h-[400px]">
            {preview ? (
              <div className="relative inline-block w-full h-full max-h-[500px]">
                <img 
                  ref={imgRef}
                  src={preview} 
                  alt="Upload preview" 
                  className="w-full h-full object-contain"
                />
                {/* Draw Bounding Boxes */}
                {results.map((det, idx) => {
                  // We need to scale the bbox to the rendered image size.
                  // Since object-contain scales the image, we do a rough percentage overlay.
                  if (!imgRef.current) return null;
                  const img = imgRef.current;
                  const naturalW = img.naturalWidth;
                  const naturalH = img.naturalHeight;
                  const [x1, y1, x2, y2] = det.bbox;
                  
                  const left = (x1 / naturalW) * 100;
                  const top = (y1 / naturalH) * 100;
                  const width = ((x2 - x1) / naturalW) * 100;
                  const height = ((y2 - y1) / naturalH) * 100;

                  return (
                    <div 
                      key={idx} 
                      className="absolute border-2 border-red-500 bg-red-500/20"
                      style={{ 
                        left: `${left}%`, top: `${top}%`, width: `${width}%`, height: `${height}%`
                      }}
                    >
                      <span className="absolute -top-6 left-0 bg-red-500 text-white text-xs font-bold px-1 rounded whitespace-nowrap">
                        {det.class.toUpperCase()} {(det.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="text-gray-500 flex flex-col items-center">
                <UploadCloud size={48} className="mb-2 opacity-50" />
                <p>Drag & drop or click to upload</p>
                <p className="text-xs mt-1">Accepts JPG, PNG for visual inference</p>
              </div>
            )}
            <input 
              type="file" 
              accept="image/*" 
              className="absolute inset-0 opacity-0 cursor-pointer" 
              onChange={handleFileChange}
            />
          </div>
          
          <button 
            onClick={handleUpload}
            disabled={!file || loading}
            className="w-full mt-4 bg-primary hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed px-4 py-3 rounded-lg font-bold transition-colors"
          >
            {loading ? 'Executing Neural Network...' : 'Run Computer Vision Inference'}
          </button>
          
          {error && <p className="text-red-500 text-sm mt-3">{error}</p>}
        </div>

        <div className="bg-surface border border-gray-800 rounded-xl p-6 flex flex-col">
          <div className="flex justify-between items-center mb-4">
             <h2 className="text-xl font-semibold flex items-center gap-2">
               <CheckCircle className="text-safe" /> Inference Output
             </h2>
             {inferenceTime && (
                <span className="text-xs text-gray-400 bg-gray-800 px-2 py-1 rounded">
                  Latency: <span className="text-white font-bold">{inferenceTime}ms</span>
                </span>
             )}
          </div>
          
          <div className="bg-gray-900 rounded-lg p-4 flex-1 overflow-y-auto border border-gray-800 font-mono text-sm">
            {results.length === 0 ? (
              <p className="text-gray-500">Awaiting inference execution...</p>
            ) : (
              <div className="space-y-3">
                {results.map((det, idx) => (
                  <div key={idx} className="p-3 bg-gray-800 rounded border border-gray-700">
                    <div className="flex justify-between items-center mb-1">
                      <span className="font-bold text-red-400 uppercase">{det.class}</span>
                      <span className="text-green-400 font-bold">{(det.confidence * 100).toFixed(1)}%</span>
                    </div>
                    <p className="text-xs text-gray-400 mb-1">
                      BBox Coordinates: [{det.bbox.map((b: number) => Math.round(b)).join(', ')}]
                    </p>
                    <p className="text-xs text-gray-500">
                      Evaluated by: {det.model_used || "Unknown Model"}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
          <div className="mt-4 p-3 bg-blue-900/20 border border-blue-900/50 rounded-lg text-xs text-blue-200">
            <strong>NOTE:</strong> If standard YOLOv8 COCO weights are loaded, Fire/Smoke/Flood will NOT be detected. 
            Real disaster classification requires uploading custom `fire_smoke_yolov8.pt` weights to the backend directory.
          </div>
        </div>
      </div>
    </div>
  );
};

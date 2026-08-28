import React, { useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Sphere, MeshDistortMaterial, Html } from '@react-three/drei';
import * as THREE from 'three';

const LocationMarker = ({ position, type, severity, onClick }: any) => {
  const meshRef = useRef<THREE.Mesh>(null);
  const color = type === 'FIRE' ? '#EF4444' : type === 'FLOOD' ? '#3B82F6' : '#F59E0B';
  const size = severity === 'CRITICAL' ? 1.5 : severity === 'HIGH' ? 1.2 : 1;

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime * 2) * 0.2;
    }
  });

  return (
    <group position={position}>
      <mesh ref={meshRef} onClick={onClick}>
        <sphereGeometry args={[0.3 * size, 32, 32]} />
        <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.5} />
      </mesh>
      <Html distanceFactor={15} center>
        <div className="bg-black/80 px-2 py-1 rounded text-xs border border-gray-700 whitespace-nowrap">
          <span className="font-bold" style={{ color }}>{type}</span>
        </div>
      </Html>
    </group>
  );
};

export const DisasterMap3D = ({ incidents }: { incidents: any[] }) => {
  return (
    <div className="w-full h-full bg-gray-900 rounded-lg overflow-hidden relative">
      <Canvas camera={{ position: [0, 5, 10], fov: 45 }}>
        <ambientLight intensity={0.2} />
        <directionalLight position={[10, 10, 5]} intensity={1} />
        <pointLight position={[-10, -10, -10]} intensity={0.5} />
        
        {/* Abstract Terrain */}
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.5, 0]}>
          <planeGeometry args={[50, 50, 64, 64]} />
          <MeshDistortMaterial 
            color="#1F2937" 
            wireframe 
            distort={0.2} 
            speed={1} 
            transparent 
            opacity={0.3} 
          />
        </mesh>

        <gridHelper args={[50, 50, '#374151', '#111827']} />

        {/* Map Incidents to 3D Space */}
        {incidents.filter(i => i.status !== 'RESOLVED').map((inc, index) => {
          // Abstract positioning based on ID or random for demo if lat/lng are 0
          const x = (inc.lat !== 0 ? inc.lat : Math.sin(index) * 5) % 10;
          const z = (inc.lng !== 0 ? inc.lng : Math.cos(index) * 5) % 10;
          
          return (
            <LocationMarker 
              key={inc.id} 
              position={[x, 0, z]} 
              type={inc.type} 
              severity={inc.severity} 
              onClick={() => console.log('Clicked', inc.id)}
            />
          );
        })}

        <OrbitControls 
          enablePan={true} 
          enableZoom={true} 
          enableRotate={true}
          maxPolarAngle={Math.PI / 2 - 0.1}
        />
      </Canvas>
      <div className="absolute bottom-4 right-4 bg-black/60 p-3 rounded-lg border border-gray-700 text-xs">
        <div className="flex items-center gap-2"><div className="w-3 h-3 bg-red-500 rounded-full"></div> Fire</div>
        <div className="flex items-center gap-2"><div className="w-3 h-3 bg-blue-500 rounded-full"></div> Flood</div>
        <div className="flex items-center gap-2"><div className="w-3 h-3 bg-yellow-500 rounded-full"></div> Smoke</div>
      </div>
    </div>
  );
};

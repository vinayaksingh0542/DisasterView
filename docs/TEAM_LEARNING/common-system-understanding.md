# System Understanding

## The Core Problem
SIH PS 26178 asks for an Environmental Intelligence Network. Simply putting sensors on an Arduino isn't enough. We needed a **distributed, scalable architecture** capable of handling AI on the edge, real-time sensor ingestion, and instant visualization.

## How Our System Solves It
1. **Edge-to-Cloud Data Flow:** We don't send heavy video to the cloud. We run YOLOv8 on the edge (Qualcomm Snapdragon pathway) and send only JSON metadata (e.g., `{"type": "fire", "confidence": 0.85, "bbox": [...]}`).
2. **Sensor Fusion:** This is our killer feature. AI can be wrong. Sensors can be wrong. But if the Edge AI sees a fire, AND the ESP32 flame sensor detects IR light, AND the temperature spikes above 60°C, the backend Event Engine immediately upgrades the alert to CRITICAL.
3. **Reactive UI:** The React frontend uses WebSockets. When the backend creates an incident, it broadcasts to all connected Command Centers. The 3D map and dashboard update instantly without polling.

## Technology Choices
- **FastAPI:** Used because it's async natively, making it perfect for handling thousands of IoT devices and WebSocket connections efficiently.
- **SQLite (SQLAlchemy):** We architected for PostgreSQL but use SQLite for the demo to ensure zero-friction setup for the judges.
- **React + Vite:** Extremely fast build tool and frontend library for real-time reactivity.
- **Three.js / React-Three-Fiber:** Used for the 3D visual threat map, providing a true Command Center feel as requested by the Stitch design principles.

# DisasterView System Architecture

**Team:** Team Apex 07  
**Challenge:** Smart India Hackathon (SIH 2026) — Problem Statement 26178  
**System Status:** `SOFTWARE: VERIFIED` | `HARDWARE: NOT YET PHYSICALLY TESTED`

---

## 1. High-Level System Architecture

DisasterView uses a **physical sensor-first paradigm** for primary real-time disaster detection. Computer vision is decoupled as an independent software validation module.

```
+-------------------------------------------------------------------------+
|                       PHYSICAL SENSOR PIPELINE                          |
|                                                                         |
|  ESP32 Hardware Node (Flame + DHT22 + MQ135 + MQ9 + HC-SR04)            |
|                                  | (Wi-Fi / JSON)                       |
|                                  v                                      |
|                       FastAPI /api/sensors Ingestion                    |
|                                  |                                      |
|                                  v                                      |
|                 Multi-Sensor Fusion Engine (Debounce & Rules)           |
|                                  |                                      |
|                                  v                                      |
|                    Incident Engine & Severity Scorer                    |
|                                  |                                      |
|            +---------------------+---------------------+                |
|            |                                           |                |
|            v                                           v                |
|     SQLite / PostgreSQL Database              WebSocket Broadcaster     |
|            |                                           |                |
|            +---------------------+---------------------+                |
|                                  |                                      |
|                                  v                                      |
|                React + Vite Command Center Dashboard                    |
+-------------------------------------------------------------------------+
```

---

## 2. Separate AI Demonstration Module (Software Only)

```
+-------------------------------------------------------------------------+
|                  STANDALONE AI DEMONSTRATION MODULE                     |
|                                                                         |
|  User Image Upload (Test Wildfire / Smoke / Flood Scene)                |
|                                  |                                      |
|                                  v                                      |
|               FastAPI /api/inference (PyTorch Local CPU)                |
|                                  |                                      |
|         +------------------------+------------------------+             |
|         |                                                 |             |
|         v                                                 v             |
|  Fire & Smoke Model                              Flood Classifier       |
|  (touati-kamel/yolov8s-forest-fire)              (prithivMLmods)        |
|         |                                                 |             |
|         +------------------------+------------------------+             |
|                                  |                                      |
|                                  v                                      |
|               Detections & Bounding Box Visualization                   |
|                        (Cameras/AI Page)                                |
+-------------------------------------------------------------------------+
```

---

## 3. Future Camera-Integrated Fusion Architecture (Optional Future Path)

```
+-------------------------------------------------------------------------+
|                  FUTURE CAMERA INTEGRATION ROADMAP                      |
|                                                                         |
|     +------------------+                   +------------------+         |
|     |  ESP32 Sensors   |                   |  Optional Camera |         |
|     +--------+---------+                   +--------+---------+         |
|              |                                      |                   |
|              v                                      v                   |
|     Physical Sensor Evidence             Computer Vision AI Evidence    |
|              |                                      |                   |
|              +-------------------+------------------+                   |
|                                  |                                      |
|                                  v                                      |
|                  Multi-Modal Sensor + Vision Fusion                     |
+-------------------------------------------------------------------------+
```

---

## 4. Hardware Node vs Cloud/Edge Interface

| Component | Protocol | Endpoint / Role |
|---|---|---|
| **ESP32 Sensor Node** | HTTP POST (JSON) | `/api/sensors` |
| **React Dashboard (REST)** | HTTP GET / PATCH / POST | `/api/incidents`, `/api/devices`, `/api/models` |
| **React Dashboard (Live Stream)**| WebSocket (RFC 6455) | `/ws` |
| **Edge AI Software Testing** | HTTP POST (Multipart) | `/api/inference` |

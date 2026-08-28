# DisasterView — Multi-Hazard Disaster Detection & Response System

[![Built by](https://img.shields.io/badge/Team-Team%20Apex%2007-blue.svg)](https://github.com/TeamApex07/DisasterView)
[![Hackathon](https://img.shields.io/badge/SIH-2026%20PS%2026178-orange.svg)](https://www.sih.gov.in/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%20%7C%20Python-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%2018%20%7C%20Vite%20%7C%20Tailwind-blue.svg)](https://react.dev/)
[![Status](https://img.shields.io/badge/Software-VERIFIED-brightgreen.svg)]()
[![Hardware](https://img.shields.io/badge/Hardware-NOT%20YET%20PHYSICALLY%20TESTED-yellow.svg)]()

> **DisasterView** is an end-to-end multi-hazard early detection and incident management system engineered by **Team Apex 07** for **Smart India Hackathon 2026 (PS 26178)**. The system couples an ESP32 multi-sensor edge node with an explainable multi-sensor fusion engine, real-time WebSocket command center, 3D interactive threat map, and a standalone Computer Vision AI validation suite.

---

## 1. System Architecture Overview

The system operates on a **physical sensor-first** paradigm. Computer vision AI models are decoupled into a dedicated demonstration module for edge benchmarking prior to future camera attachment.

```
+-------------------------------------------------------------------------+
|                       PHYSICAL SENSOR PIPELINE                          |
|                                                                         |
|  ESP32 Edge Node (Flame + DHT22 + MQ135 + MQ9 + HC-SR04)                |
|                                  | (Wi-Fi / HTTP POST)                  |
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

## 2. Core Capabilities & Supported Disasters

### 🔥 Fire Detection Sub-system
- **Physical Sensors:** Infrared Flame Sensor + DHT22 Temperature ($>60^\circ\text{C}$) + MQ-9 Combustible Gas ($>300$).
- **Fusion Logic:** Corroborates flame optical trigger with thermal and hydrocarbon spikes. Single sensors produce warnings; multi-sensor agreement triggers `CRITICAL` alert.

### 🌫️ Smoke & Toxic Air Sub-system
- **Physical Sensors:** MQ-135 Hazardous Gas & Particulate Sensor ($>400$) + MQ-9 Carbon Monoxide.
- **Fusion Logic:** Detects hazardous air degradation in non-fire conditions, reporting environmental air threats.

### 🌊 Flood Water Elevation Sub-system
- **Physical Sensors:** HC-SR04 Ultrasonic Rangefinder.
- **Fusion Logic:** Measures real-time water clearance distance $d_{\text{water}}$ against calibrated baseline datum $H_{\text{ref}}$. Triggers `HIGH` ($<50\text{cm}$) and `CRITICAL` ($<20\text{cm}$) flood incidents.

---

## 3. Technology Stack

- **Edge Microcontroller:** ESP32-WROOM-32 (C++ / Arduino IDE / ESP-IDF)
- **Backend Framework:** FastAPI, Uvicorn, SQLAlchemy, Pydantic, WebSockets (Python 3.12)
- **Database:** SQLite (local development) / PostgreSQL (production)
- **Frontend SPA:** React 18, Vite, Tailwind CSS, Lucide Icons, Recharts, Three.js / React Three Fiber
- **Computer Vision Models (Standalone Demo):**
  - Fire & Smoke Detection: `touati-kamel/yolov8s-forest-fire-detection` (Ultralytics PyTorch)
  - Flood Scene Classifier: `prithivMLmods/Flood-Image-Detection` (HuggingFace Transformers)
  - **Runtime:** `LOCAL CPU / PYTORCH` *(Qualcomm QNN edge runtime planned for future silicon deployment)*

---

## 4. Production Deployment & Team Identity

### Production Endpoints
- **Production Dashboard:** `https://teamapex07-disasterview.pages.dev`
- **Production API Base:** `https://teamapex07-disasterview.onrender.com/api`
- **Production WebSocket:** `wss://teamapex07-disasterview.onrender.com/ws`
- **Health Check:** `https://teamapex07-disasterview.onrender.com/health`
- **ESP32 Firmware Target:** `https://teamapex07-disasterview.onrender.com/api/sensors`
- **GitHub Repository:** `https://github.com/TeamApex07/DisasterView`

---

## 5. Local Setup & Quickstart

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### Backend Setup
```bash
cd backend
python -m venv .venv
# On Windows: .venv\Scripts\activate | On Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5174` in your browser.

---

## 6. Complete Documentation Index
- [System Architecture](docs/ARCHITECTURE.md)
- [Sensor Fusion Algorithm](docs/SENSOR_FUSION_ALGORITHM.md)
- [Hardware Wiring Specification](docs/HARDWARE_WIRING.md)
- [Hardware Testing Protocol](docs/HARDWARE_TEST_PROTOCOL.md)
- [AI Architecture & Vision Pipeline](docs/AI_ARCHITECTURE.md)
- [AI Local Validation & Benchmarks](docs/AI_VALIDATION.md)
- [AI Performance Tuning & Profiling](docs/AI_PERFORMANCE.md)
- [Flood AI Model Specification](docs/FLOOD_AI.md)
- [Qualcomm Edge Deployment Strategy](docs/QUALCOMM_DEPLOYMENT.md)
- [Production Deployment Guide](docs/DEPLOYMENT.md)
- [Final Regression & Validation Report](docs/FINAL_VALIDATION.md)

---

## 7. Team & Project Metadata

- **Team Name:** Team Apex 07
- **Problem Statement:** SIH 2026 PS 26178 — AI & IoT Powered Disaster Management
- **Hardware Status:** `SOFTWARE: VERIFIED` | `HARDWARE: NOT YET PHYSICALLY TESTED`

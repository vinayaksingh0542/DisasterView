# DisasterView Production Deployment Guide

**Team:** Team Apex 07  
**System:** DisasterView Multi-Hazard Early Warning System  
**Target Platform:** Render.com (Backend) / Vercel or Cloudflare Pages (Frontend) / Self-Hosted VPS

---

## 1. Production Architecture Overview
- **Backend Service:** FastAPI + Uvicorn with SQLite / PostgreSQL on Render.
- **Frontend SPA:** React + Vite static bundle on Cloudflare Pages / Vercel.
- **Hardware Node:** ESP32 pointing to production HTTPS backend URL.

---

## 2. Production Environment Variables

### Backend Configuration
| Variable | Production Value | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./disasterview.db` (or `postgresql://user:pass@host/db`) | Database connection string |
| `ALLOWED_ORIGINS` | `https://teamapex07-disasterview.pages.dev,https://teamapex07-disasterview.vercel.app` | Allowed CORS origins |
| `TEMP_FIRE_THRESHOLD` | `60.0` | Fire thermal threshold (°C) |
| `MQ9_FIRE_THRESHOLD` | `300.0` | Gas elevation threshold |
| `MQ135_SMOKE_THRESHOLD` | `400.0` | Smoke air quality threshold |
| `FLOOD_CRITICAL_DIST` | `20.0` | Flood critical distance (cm) |
| `FLOOD_HIGH_DIST` | `50.0` | Flood warning distance (cm) |
| `INCIDENT_DEBOUNCE_SECONDS` | `30` | Incident duplicate suppression window |

### Frontend Configuration (`.env.production`)
| Variable | Production Value | Description |
|---|---|---|
| `VITE_API_BASE` | `https://teamapex07-disasterview.onrender.com/api` | Production REST API base |
| `VITE_WS_BASE` | `wss://teamapex07-disasterview.onrender.com/ws` | Production WebSocket endpoint |

---

## 3. Step-by-Step Deployment from Scratch

### Step A: Deploy Backend (Render.com - Free Tier)
1. Fork or push repository to GitHub (`TeamApex07/DisasterView`).
2. Log in to [Render.com](https://render.com) and click **New + Web Service**.
3. Connect GitHub repository and configure:
   - **Name:** `teamapex07-disasterview`
   - **Root Directory:** `backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables from table above.
5. Deploy service. Once live, test `https://teamapex07-disasterview.onrender.com/health`.

### Step B: Deploy Frontend (Cloudflare Pages / Vercel - Free Tier)
1. In Cloudflare Pages or Vercel, connect repository `TeamApex07/DisasterView`.
2. Configure build settings:
   - **Project Name:** `teamapex07-disasterview`
   - **Root Directory:** `frontend`
   - **Framework Preset:** `Vite`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
3. Add Environment Variable:
   - `VITE_API_BASE`: `https://teamapex07-disasterview.onrender.com/api`
   - `VITE_WS_BASE`: `wss://teamapex07-disasterview.onrender.com/ws`
4. Deploy site. Production dashboard will be live at `https://teamapex07-disasterview.pages.dev`.

### Step C: Configure ESP32 Firmware
1. Open [`firmware/main.ino`](../firmware/main.ino).
2. Update Wi-Fi and production endpoint:
   ```cpp
   const char* ssid = "YOUR_WIFI_SSID";
   const char* password = "YOUR_WIFI_PASSWORD";
   const char* serverUrl = "https://teamapex07-disasterview.onrender.com/api/sensors";
   ```
3. Flash the ESP32 node via Arduino IDE.

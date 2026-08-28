# DisasterView Production Deployment Guide

**Team:** Team Apex 07  
**System:** DisasterView Multi-Hazard Early Warning System  
**Deployment Architecture:** Cloudflare Pages (Frontend) + Render.com (Backend) + GitHub Version Control

---

## 1. Production Architecture Overview
- **Backend Service:** FastAPI + Uvicorn with SQLite (Ephemeral) or Render PostgreSQL.
- **Frontend SPA:** React 18 + Vite static bundle hosted on **Cloudflare Pages**.
- **Hardware Node:** ESP32 pointing to production HTTPS backend URL.

---

## 2. Production Environment Variables

### Backend Configuration (Render Environment Settings)
| Variable | Production Value | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./disasterview.db` (or `postgresql://user:pass@host/db`) | Database connection string |
| `ALLOWED_ORIGINS` | `https://teamapex07-disasterview.pages.dev` | Allowed CORS origins (Strict Cloudflare Pages domain) |
| `TEMP_FIRE_THRESHOLD` | `60.0` | Fire thermal threshold (°C) |
| `MQ9_FIRE_THRESHOLD` | `300.0` | Gas elevation threshold |
| `MQ135_SMOKE_THRESHOLD` | `400.0` | Smoke air quality threshold |
| `FLOOD_CRITICAL_DIST` | `20.0` | Flood critical distance (cm) |
| `FLOOD_HIGH_DIST` | `50.0` | Flood warning distance (cm) |
| `INCIDENT_DEBOUNCE_SECONDS` | `30` | Incident duplicate suppression window |

### Frontend Configuration (`frontend/.env.production`)
| Variable | Production Value | Description |
|---|---|---|
| `VITE_API_BASE` | `https://teamapex07-disasterview.onrender.com/api` | Production REST API base |
| `VITE_WS_BASE` | `wss://teamapex07-disasterview.onrender.com/ws` | Production WebSocket endpoint |

---

## 3. Database Architecture & Ephemeral Storage Limitation

> [!WARNING]
> **Production Database State & Limitations:**
> - If deployed with default `DATABASE_URL=sqlite:///./disasterview.db`, Render's free tier filesystem is **ephemeral**. Database records will reset on server restart or redeploy.
> - For persistent production data retention across restarts, provision a **Render PostgreSQL instance** (Free Tier) and provide the connection URL to `DATABASE_URL`.

---

## 4. Step-by-Step Deployment from Scratch

### Step A: Push Code to GitHub
1. Create a repository named `DisasterView` under organization/account `TeamApex07`.
2. Push the local repository:
   ```bash
   git remote add origin https://github.com/TeamApex07/DisasterView.git
   git push -u origin main
   ```

### Step B: Deploy Backend on Render.com (Free Tier)
1. In [Render Dashboard](https://dashboard.render.com), select **New + Web Service**.
2. Connect `TeamApex07/DisasterView` repository.
3. Configure settings:
   - **Service Name:** `teamapex07-disasterview`
   - **Root Directory:** `backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables from Section 2.
5. Deploy service. Once active, verify `https://teamapex07-disasterview.onrender.com/health`.

### Step C: Deploy Frontend on Cloudflare Pages (Free Tier)
1. In [Cloudflare Dashboard](https://dash.cloudflare.com), navigate to **Workers & Pages** -> **Create Application** -> **Pages**.
2. Connect `TeamApex07/DisasterView` repository.
3. Set build configuration:
   - **Project Name:** `teamapex07-disasterview`
   - **Framework Preset:** `Vite`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
4. Configure Environment Variables:
   - `VITE_API_BASE`: `https://teamapex07-disasterview.onrender.com/api`
   - `VITE_WS_BASE`: `wss://teamapex07-disasterview.onrender.com/ws`
5. Click **Save and Deploy**. Cloudflare will assign `https://teamapex07-disasterview.pages.dev`.

### Step D: Configure ESP32 Firmware
1. Open [`firmware/main.ino`](../firmware/main.ino).
2. Set the production target endpoint:
   ```cpp
   const char* ssid = "YOUR_WIFI_SSID";
   const char* password = "YOUR_WIFI_PASSWORD";
   const char* serverUrl = "https://teamapex07-disasterview.onrender.com/api/sensors";
   ```
3. Flash the ESP32 node.

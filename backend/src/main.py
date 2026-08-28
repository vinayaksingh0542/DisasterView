from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .api import routes
from .db.session import engine, Base
import os

app = FastAPI(
    title="DISASTERVIEW Production API - Team Apex 07",
    description="Physical Sensor Fusion & Edge AI Disaster Detection API (SIH 2026 PS 26178)",
    version="1.0.0"
)

# Configurable CORS origins
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",")] if allowed_origins_env != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto-initialize database tables cleanly
Base.metadata.create_all(bind=engine)

app.include_router(routes.router)

@app.get("/")
def read_root():
    return {
        "project": "DisasterView",
        "team": "Team Apex 07",
        "system_status": "ONLINE",
        "pipeline": "ESP32 Sensor Fusion + Standalone AI Module",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    # Verify DB connectivity
    db_status = "HEALTHY"
    try:
        from .db.session import SessionLocal
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
    except Exception as e:
        db_status = f"DEGRADED ({str(e)})"

    return {
        "status": "HEALTHY" if db_status == "HEALTHY" else "DEGRADED",
        "team": "Team Apex 07",
        "database": db_status,
        "api": "ONLINE",
        "websocket": "ENABLED"
    }

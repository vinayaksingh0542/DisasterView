from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from ..db.session import get_db
from ..models.all_models import Device, SensorReading, Incident
from pydantic import BaseModel, Field
import uuid
import datetime
import os
import sys

router = APIRouter()

# WebSocket Manager for Real-time Dashboard Updates
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception:
                self.disconnect(connection)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)

# --- DEVICE SCHEMAS & ROUTES ---
class DeviceCreate(BaseModel):
    name: str
    location: str
    lat: float = 28.6139
    lng: float = 77.2090
    hcsr04_reference_height_cm: float = 200.0

@router.post("/api/devices")
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    db_device = Device(
        id=str(uuid.uuid4()),
        name=device.name,
        location=device.location,
        lat=device.lat,
        lng=device.lng,
        hcsr04_reference_height_cm=device.hcsr04_reference_height_cm,
        status="ONLINE"
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

@router.get("/api/devices")
def get_devices(db: Session = Depends(get_db)):
    return db.query(Device).all()

# --- SENSOR INGESTION & FUSION SCHEMAS ---
class SensorData(BaseModel):
    device_id: str
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    mq135_air_quality: Optional[float] = None
    mq9_gas_level: Optional[float] = None
    flame_detected: bool = False
    water_distance_cm: Optional[float] = None

# Configurable Engineering Thresholds (Sensor Fusion Rules)
TEMP_FIRE_THRESHOLD = float(os.getenv("TEMP_FIRE_THRESHOLD", "60.0"))
MQ9_FIRE_THRESHOLD = float(os.getenv("MQ9_FIRE_THRESHOLD", "300.0"))
MQ135_SMOKE_THRESHOLD = float(os.getenv("MQ135_SMOKE_THRESHOLD", "400.0"))
FLOOD_CRITICAL_DIST = float(os.getenv("FLOOD_CRITICAL_DIST", "20.0"))
FLOOD_HIGH_DIST = float(os.getenv("FLOOD_HIGH_DIST", "50.0"))
DEBOUNCE_SECONDS = int(os.getenv("INCIDENT_DEBOUNCE_SECONDS", "30"))

@router.post("/api/sensors")
async def receive_sensor_data(data: SensorData, db: Session = Depends(get_db)):
    # Record raw telemetry
    reading = SensorReading(
        device_id=data.device_id,
        temperature=data.temperature,
        humidity=data.humidity,
        mq135_air_quality=data.mq135_air_quality,
        mq9_gas_level=data.mq9_gas_level,
        flame_detected=data.flame_detected,
        water_distance_cm=data.water_distance_cm,
        timestamp=datetime.datetime.utcnow()
    )
    db.add(reading)
    
    # Retrieve station location & reference height
    device = db.query(Device).filter(Device.id == data.device_id).first()
    dev_lat = device.lat if device else 28.6139
    dev_lng = device.lng if device else 77.2090
    ref_height = device.hcsr04_reference_height_cm if device else 200.0
    
    # Update device last_seen status
    if device:
        device.last_seen = datetime.datetime.utcnow()
        device.status = "ONLINE"
    
    db.commit()
    
    incident_created = False
    now = datetime.datetime.utcnow()
    debounce_cutoff = now - datetime.timedelta(seconds=DEBOUNCE_SECONDS)

    # Helper function to check recent active incident of same type on this device
    def has_recent_incident(disaster_type: str) -> bool:
        recent = db.query(Incident).filter(
            Incident.type == disaster_type,
            Incident.status == "UNVERIFIED",
            Incident.created_at >= debounce_cutoff
        ).first()
        return recent is not None

    # =========================================================================
    # 1. FIRE SENSOR FUSION
    # =========================================================================
    fire_evidence = []
    if data.flame_detected:
        fire_evidence.append("Flame IR Sensor: TRIGGERED (Active Flame)")
    if data.temperature is not None and data.temperature > TEMP_FIRE_THRESHOLD:
        fire_evidence.append(f"DHT22 Temperature: {data.temperature:.1f}°C (Threshold: >{TEMP_FIRE_THRESHOLD}°C)")
    if data.mq9_gas_level is not None and data.mq9_gas_level > MQ9_FIRE_THRESHOLD:
        fire_evidence.append(f"MQ-9 Combustible Gas Level: {data.mq9_gas_level:.0f} (Threshold: >{MQ9_FIRE_THRESHOLD})")
    
    if len(fire_evidence) > 0:
        if not has_recent_incident("FIRE"):
            # Multi-sensor severity calculation
            is_critical = data.flame_detected and (
                (data.temperature is not None and data.temperature > TEMP_FIRE_THRESHOLD) or 
                (data.mq9_gas_level is not None and data.mq9_gas_level > MQ9_FIRE_THRESHOLD)
            )
            severity = "CRITICAL" if is_critical else "HIGH"
            evidence_score = "CRITICAL" if is_critical else ("HIGH" if data.flame_detected else "MEDIUM")
            
            incident = Incident(
                id=str(uuid.uuid4()),
                type="FIRE",
                severity=severity,
                lat=dev_lat, 
                lng=dev_lng,
                description=f"Multi-sensor fire detection: {len(fire_evidence)} corroborated indicator(s).",
                source="SENSOR_FUSION",
                evidence_score=evidence_score,
                evidence_details={"sensors": fire_evidence, "device_id": data.device_id},
                created_at=now
            )
            db.add(incident)
            db.commit()
            incident_created = True
            await manager.broadcast('{"type": "NEW_INCIDENT", "data": "FIRE"}')

    # =========================================================================
    # 2. SMOKE SENSOR FUSION (Evaluated only when open flame is not present)
    # =========================================================================
    smoke_evidence = []
    if data.mq135_air_quality is not None and data.mq135_air_quality > MQ135_SMOKE_THRESHOLD:
        smoke_evidence.append(f"MQ-135 Air Quality / Particulates: {data.mq135_air_quality:.0f} (Threshold: >{MQ135_SMOKE_THRESHOLD})")
    if data.mq9_gas_level is not None and data.mq9_gas_level > 200.0:
        smoke_evidence.append(f"MQ-9 Gas Co-presence: {data.mq9_gas_level:.0f}")

    if len(smoke_evidence) > 0 and len(fire_evidence) == 0:
        if not has_recent_incident("SMOKE"):
            incident = Incident(
                id=str(uuid.uuid4()),
                type="SMOKE",
                severity="WARNING",
                lat=dev_lat, 
                lng=dev_lng,
                description="Elevated hazardous particulates & toxic air quality detected.",
                source="SENSOR_FUSION",
                evidence_score="MEDIUM" if len(smoke_evidence) == 1 else "HIGH",
                evidence_details={"sensors": smoke_evidence, "device_id": data.device_id},
                created_at=now
            )
            db.add(incident)
            db.commit()
            incident_created = True
            await manager.broadcast('{"type": "NEW_INCIDENT", "data": "SMOKE"}')

    # =========================================================================
    # 3. FLOOD SENSOR FUSION (HC-SR04 ultrasonic distance to water surface)
    # =========================================================================
    if data.water_distance_cm is not None:
        water_level = max(0.0, ref_height - data.water_distance_cm)
        flood_evidence = []
        severity = None
        
        if data.water_distance_cm < FLOOD_CRITICAL_DIST:
            severity = "CRITICAL"
            flood_evidence.append(f"HC-SR04 Clearance Distance: {data.water_distance_cm:.1f}cm (Threshold: <{FLOOD_CRITICAL_DIST}cm)")
            flood_evidence.append(f"Estimated Water Height: {water_level:.1f}cm above reference datum ({ref_height:.0f}cm)")
        elif data.water_distance_cm < FLOOD_HIGH_DIST:
            severity = "HIGH"
            flood_evidence.append(f"HC-SR04 Clearance Distance: {data.water_distance_cm:.1f}cm (Threshold: <{FLOOD_HIGH_DIST}cm)")
            flood_evidence.append(f"Estimated Water Height: {water_level:.1f}cm above reference datum ({ref_height:.0f}cm)")
            
        if severity is not None:
            if not has_recent_incident("FLOOD"):
                incident = Incident(
                    id=str(uuid.uuid4()),
                    type="FLOOD",
                    severity=severity,
                    lat=dev_lat, 
                    lng=dev_lng,
                    description=f"Rapid water elevation detected by ultrasonic rangefinder ({water_level:.1f}cm).",
                    source="SENSOR_FUSION",
                    evidence_score=severity,
                    evidence_details={"sensors": flood_evidence, "device_id": data.device_id},
                    created_at=now
                )
                db.add(incident)
                db.commit()
                incident_created = True
                await manager.broadcast('{"type": "NEW_INCIDENT", "data": "FLOOD"}')
            
    await manager.broadcast('{"type": "NEW_SENSOR_DATA"}')
    return {"status": "success", "incident_created": incident_created}

# --- INCIDENT MANAGEMENT ROUTES ---
@router.get("/api/incidents")
def get_incidents(db: Session = Depends(get_db)):
    return db.query(Incident).order_by(Incident.created_at.desc()).all()

class IncidentStatusUpdate(BaseModel):
    status: str = Field(..., description="UNVERIFIED, ACKNOWLEDGED, RESOLVED, DISMISSED")

@router.patch("/api/incidents/{incident_id}")
async def update_incident_status(incident_id: str, payload: IncidentStatusUpdate, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    incident.status = payload.status
    if payload.status == "RESOLVED":
        incident.resolved_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(incident)
    
    await manager.broadcast('{"type": "INCIDENT_UPDATED", "id": "' + incident_id + '", "status": "' + payload.status + '"}')
    return incident

# --- AI INFERENCE ENGINE INTEGRATION (STANDALONE DEMO MODULE) ---
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
try:
    from ai.inference import EdgeAIInferencer
    ai_inferencer = EdgeAIInferencer()
except Exception as e:
    ai_inferencer = None

@router.get("/api/models")
def get_model_registry():
    if not ai_inferencer:
        return {
            "fire_smoke": {
                "name": "MISSING WEIGHTS",
                "runtime": "LOCAL CPU / PYTORCH",
                "expected_classes": []
            },
            "flood": {
                "name": "MISSING WEIGHTS (NO FAKE AI)",
                "runtime": "LOCAL CPU / PYTORCH",
                "expected_classes": ["NOT CONFIGURED"]
            }
        }
    return ai_inferencer.get_model_info()

@router.post("/api/inference")
async def run_inference(file: UploadFile = File(...)):
    if not ai_inferencer:
        return {"error": "AI Inferencer not loaded.", "detections": []}
    
    image_bytes = await file.read()
    results = ai_inferencer.infer_image(image_bytes)
    
    # Broadcast high-confidence software detection demonstration
    for det in results.get("detections", []):
        if det.get("confidence", 0) > 0.5:
            await manager.broadcast('{"type": "NEW_AI_DETECTION", "data": "' + f'{det["class"].upper()}' + '"}')
             
    return results

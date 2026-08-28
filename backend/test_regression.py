import pytest
import sys
import os
import json

# Setup import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Use a clean in-memory test database
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.db.session import Base, engine, SessionLocal
from backend.src.models.all_models import Device, Incident

client = TestClient(app)

def setup_module():
    Base.metadata.create_all(bind=engine)

def test_1_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["team"] == "Team Apex 07"
    assert data["database"] == "HEALTHY"

def test_2_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["team"] == "Team Apex 07"
    assert data["project"] == "DisasterView"

def test_3_empty_database_state():
    resp_incidents = client.get("/api/incidents")
    assert resp_incidents.status_code == 200
    assert resp_incidents.json() == []

    resp_devices = client.get("/api/devices")
    assert resp_devices.status_code == 200
    assert resp_devices.json() == []

def test_4_device_creation():
    payload = {
        "name": "ESP32 Station Alpha",
        "location": "North Forest Sector 4",
        "lat": 28.6139,
        "lng": 77.2090,
        "hcsr04_reference_height_cm": 200.0
    }
    response = client.post("/api/devices", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "ESP32 Station Alpha"
    assert "id" in data

def test_5_normal_sensor_telemetry_no_incident():
    payload = {
        "device_id": "demo-node-01",
        "temperature": 24.5,
        "humidity": 55.0,
        "mq135_air_quality": 120.0,
        "mq9_gas_level": 80.0,
        "flame_detected": False,
        "water_distance_cm": 195.0
    }
    response = client.post("/api/sensors", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["incident_created"] is False

    # Verify no incident created
    inc_resp = client.get("/api/incidents")
    assert len(inc_resp.json()) == 0

def test_6_fire_sensor_fusion_incident():
    payload = {
        "device_id": "demo-node-01",
        "temperature": 82.0,
        "humidity": 20.0,
        "mq135_air_quality": 350.0,
        "mq9_gas_level": 600.0,
        "flame_detected": True,
        "water_distance_cm": 200.0
    }
    response = client.post("/api/sensors", json=payload)
    assert response.status_code == 200
    assert response.json()["incident_created"] is True

    inc_resp = client.get("/api/incidents")
    incidents = inc_resp.json()
    assert len(incidents) >= 1
    fire_inc = [i for i in incidents if i["type"] == "FIRE"][0]
    assert fire_inc["severity"] == "CRITICAL"
    assert fire_inc["evidence_score"] == "CRITICAL"
    assert "Flame IR Sensor: TRIGGERED" in fire_inc["evidence_details"]["sensors"][0]

def test_7_smoke_sensor_fusion_incident():
    payload = {
        "device_id": "demo-node-01",
        "temperature": 28.0,
        "humidity": 45.0,
        "mq135_air_quality": 820.0,
        "mq9_gas_level": 250.0,
        "flame_detected": False,
        "water_distance_cm": 200.0
    }
    response = client.post("/api/sensors", json=payload)
    assert response.status_code == 200
    assert response.json()["incident_created"] is True

    inc_resp = client.get("/api/incidents")
    incidents = inc_resp.json()
    smoke_inc = [i for i in incidents if i["type"] == "SMOKE"][0]
    assert smoke_inc["severity"] == "WARNING"
    assert smoke_inc["source"] == "SENSOR_FUSION"

def test_8_flood_sensor_fusion_incident():
    payload = {
        "device_id": "demo-node-01",
        "temperature": 22.0,
        "humidity": 80.0,
        "mq135_air_quality": 100.0,
        "mq9_gas_level": 80.0,
        "flame_detected": False,
        "water_distance_cm": 15.0 # Critical clearance distance (<20cm)
    }
    response = client.post("/api/sensors", json=payload)
    assert response.status_code == 200
    assert response.json()["incident_created"] is True

    inc_resp = client.get("/api/incidents")
    incidents = inc_resp.json()
    flood_inc = [i for i in incidents if i["type"] == "FLOOD"][0]
    assert flood_inc["severity"] == "CRITICAL"
    assert "HC-SR04 Clearance Distance: 15.0cm" in flood_inc["evidence_details"]["sensors"][0]

def test_9_incident_status_patch():
    inc_resp = client.get("/api/incidents")
    incidents = inc_resp.json()
    target_id = incidents[0]["id"]

    patch_resp = client.patch(f"/api/incidents/{target_id}", json={"status": "RESOLVED"})
    assert patch_resp.status_code == 200
    data = patch_resp.json()
    assert data["status"] == "RESOLVED"
    assert data["resolved_at"] is not None

def test_10_model_registry_info():
    response = client.get("/api/models")
    assert response.status_code == 200
    data = response.json()
    assert "fire_smoke" in data
    assert "flood" in data
    assert data["fire_smoke"]["runtime"] == "LOCAL CPU / PYTORCH"

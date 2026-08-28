import sys
import os

# Use a fresh test sqlite file
test_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_run.db"))
if os.path.exists(test_db_path):
    try:
        os.remove(test_db_path)
    except:
        pass

os.environ["DATABASE_URL"] = f"sqlite:///{test_db_path}"

# Setup import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from backend.src.db.session import engine, Base
from backend.src.models.all_models import Device, Incident
Base.metadata.create_all(bind=engine)

from backend.src.main import app

client = TestClient(app)

results = []

def record(test_num, name, expected, actual, passed):
    status = "PASS" if passed else "FAIL"
    results.append({
        "num": test_num,
        "test": name,
        "expected": expected,
        "actual": actual,
        "status": status
    })
    print(f"[{status}] Test {test_num}: {name} - {actual}")

# 1. Health endpoint
try:
    r = client.get("/health")
    data = r.json()
    p = r.status_code == 200 and data["status"] == "HEALTHY" and data["team"] == "Team Apex 07"
    record(1, "Backend Health Check", "status=HEALTHY, team=Team Apex 07", f"status={data.get('status')}, team={data.get('team')}", p)
except Exception as e:
    record(1, "Backend Health Check", "status=HEALTHY", str(e), False)

# 2. Root metadata
try:
    r = client.get("/")
    data = r.json()
    p = r.status_code == 200 and data["team"] == "Team Apex 07"
    record(2, "Root Metadata & Team Identity", "team=Team Apex 07", f"team={data.get('team')}", p)
except Exception as e:
    record(2, "Root Metadata & Team Identity", "team=Team Apex 07", str(e), False)

# 3. Empty database state
try:
    r_inc = client.get("/api/incidents")
    r_dev = client.get("/api/devices")
    p = len(r_inc.json()) == 0 and len(r_dev.json()) == 0
    record(3, "Empty Database Graceful Query", "0 incidents, 0 devices", f"{len(r_inc.json())} incidents, {len(r_dev.json())} devices", p)
except Exception as e:
    record(3, "Empty Database Graceful Query", "0 records", str(e), False)

# 4. Device creation
try:
    r = client.post("/api/devices", json={"name": "ESP32 Station Alpha", "location": "Sector 4", "lat": 28.61, "lng": 77.20})
    data = r.json()
    p = r.status_code == 200 and "id" in data
    record(4, "Device Registration", "Device created with UUID", f"status={r.status_code}, id={data.get('id')}", p)
except Exception as e:
    record(4, "Device Registration", "Device created", str(e), False)

# 5. Normal sensor telemetry
try:
    r = client.post("/api/sensors", json={
        "device_id": "demo-node-01",
        "temperature": 25.0, "humidity": 50.0, "mq135_air_quality": 100.0,
        "mq9_gas_level": 80.0, "flame_detected": False, "water_distance_cm": 190.0
    })
    data = r.json()
    p = r.status_code == 200 and data["incident_created"] is False
    record(5, "Normal Sensor Ingestion", "incident_created=False", f"incident_created={data.get('incident_created')}", p)
except Exception as e:
    record(5, "Normal Sensor Ingestion", "No incident", str(e), False)

# 6. Fire Sensor Fusion
try:
    r = client.post("/api/sensors", json={
        "device_id": "demo-node-01",
        "temperature": 85.0, "humidity": 20.0, "mq135_air_quality": 350.0,
        "mq9_gas_level": 650.0, "flame_detected": True, "water_distance_cm": 190.0
    })
    inc_resp = client.get("/api/incidents")
    incidents = inc_resp.json()
    fire_inc = [i for i in incidents if i["type"] == "FIRE"]
    p = len(fire_inc) > 0 and fire_inc[0]["severity"] == "CRITICAL"
    record(6, "Fire Sensor Fusion", "FIRE Incident Severity=CRITICAL", f"Found {len(fire_inc)} FIRE incidents, Severity={fire_inc[0]['severity'] if fire_inc else 'None'}", p)
except Exception as e:
    record(6, "Fire Sensor Fusion", "FIRE CRITICAL", str(e), False)

# 7. Smoke Sensor Fusion
try:
    r = client.post("/api/sensors", json={
        "device_id": "demo-node-01",
        "temperature": 30.0, "humidity": 45.0, "mq135_air_quality": 850.0,
        "mq9_gas_level": 250.0, "flame_detected": False, "water_distance_cm": 190.0
    })
    inc_resp = client.get("/api/incidents")
    incidents = inc_resp.json()
    smoke_inc = [i for i in incidents if i["type"] == "SMOKE"]
    p = len(smoke_inc) > 0 and smoke_inc[0]["severity"] == "WARNING"
    record(7, "Smoke Sensor Fusion", "SMOKE Incident Severity=WARNING", f"Found {len(smoke_inc)} SMOKE incidents, Severity={smoke_inc[0]['severity'] if smoke_inc else 'None'}", p)
except Exception as e:
    record(7, "Smoke Sensor Fusion", "SMOKE WARNING", str(e), False)

# 8. Flood Sensor Fusion
try:
    r = client.post("/api/sensors", json={
        "device_id": "demo-node-01",
        "temperature": 22.0, "humidity": 85.0, "mq135_air_quality": 100.0,
        "mq9_gas_level": 80.0, "flame_detected": False, "water_distance_cm": 12.0
    })
    inc_resp = client.get("/api/incidents")
    incidents = inc_resp.json()
    flood_inc = [i for i in incidents if i["type"] == "FLOOD"]
    p = len(flood_inc) > 0 and flood_inc[0]["severity"] == "CRITICAL"
    record(8, "Flood Sensor Fusion", "FLOOD Incident Severity=CRITICAL", f"Found {len(flood_inc)} FLOOD incidents, Severity={flood_inc[0]['severity'] if flood_inc else 'None'}", p)
except Exception as e:
    record(8, "Flood Sensor Fusion", "FLOOD CRITICAL", str(e), False)

# 9. Incident Resolution PATCH
try:
    inc_resp = client.get("/api/incidents")
    incidents = inc_resp.json()
    target_id = incidents[0]["id"]
    patch_r = client.patch(f"/api/incidents/{target_id}", json={"status": "RESOLVED"})
    p = patch_r.status_code == 200 and patch_r.json()["status"] == "RESOLVED"
    record(9, "Incident Status Resolution (PATCH)", "status=RESOLVED", f"status={patch_r.json().get('status')}", p)
except Exception as e:
    record(9, "Incident Status Resolution (PATCH)", "RESOLVED", str(e), False)

# 10. Model Registry (Lazy Load info check)
try:
    r = client.get("/api/models")
    data = r.json()
    p = "fire_smoke" in data and "status" in data
    record(10, "Model Registry Reporting", "fire_smoke in registry", f"status={data.get('status')}, fire_model={data.get('fire_smoke', {}).get('name')}", p)
except Exception as e:
    record(10, "Model Registry Reporting", "registry info", str(e), False)

all_passed = all(r["status"] == "PASS" for r in results)
print(f"\n==========================================")
print(f"REGRESSION SUITE RESULT: {'ALL 10 TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
print(f"==========================================")

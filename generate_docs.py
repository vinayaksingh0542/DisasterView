import os

DOCS_DIR = "G:/disasterview/docs"
os.makedirs(DOCS_DIR, exist_ok=True)

docs = {
    "AI_MODEL.md": """# AI Model Management

## The Objective
To execute visual AI inference on edge hardware (or Local CPU fallback) to identify disasters.

## Current Implementation
We use a standard Model Registry in `ai/inference.py`. 
Currently, we use `yolov8n.pt` (COCO dataset) to prove the pipeline (image decoding -> PyTorch -> bounding box -> JSON), but explicitly log the lack of disaster classes.

## How to Upgrade to Real Disasters
1. Train a custom YOLOv8 model using a dataset like Roboflow Fire/Smoke.
2. Export to `custom_fire_smoke_yolov8.pt`.
3. Drop the file into `G:/disasterview/ai/`.
4. The system automatically detects it, loads it, and returns accurate fire bounding boxes.
""",
    "SENSOR_FUSION.md": """# Sensor Fusion Engine

## What is it?
Visual AI hallucinates (e.g., calling a red car a fire). Sensors are localized and drift (e.g., MQ135 spikes on perfume).
Sensor Fusion combines them to create an **Evidence Score**.

## How we implemented it
In `backend/src/api/routes.py`, we parse incoming hardware JSON:
- If Flame Sensor is HIGH.
- If Temperature > 60.
- If MQ9 Gas > 300.
We don't just say "Fire". We construct an array of Evidence, then assign a Severity (`CRITICAL` vs `HIGH`).

## Judging Tip
If judges ask about false positives, explain that AI alone isn't trusted. We require physical corroboration from DHT22 or Flame sensors to upgrade an event to CRITICAL.
""",
    "MQ9.md": """# MQ9 Combustible Gas Sensor

## Implementation
The MQ9 detects Carbon Monoxide and combustible gases.
We implemented it via `mq9_gas_level` as a raw analog float in the API and Database.

## Why raw?
Without a calibrated laboratory environment, calculating true PPM (Parts Per Million) is scientifically inaccurate due to baseline drift. We map relative spikes over a baseline to indicate "Elevated" gas during fires.
""",
    "HC_SR04.md": """# HC-SR04 Flood Detection

## The Math
Distance sensor points down at the water.
`Water Level = Reference Height - Measured Distance`

## Our Implementation
In the Database, each Device has a `hcsr04_reference_height_cm` (default 200cm).
When the ESP32 sends a distance of 10cm, the backend calculates a water level of 190cm, surpassing the 20cm critical threshold, generating a FLOOD incident.
""",
    "QUALCOMM.md": """# Qualcomm Edge Integration Pathway

## The Requirement
Running AI efficiently on Snapdragon Hexagon NPU.

## The Reality
Since we develop on standard laptops, we implemented `LOCAL_CPU_RUNTIME` with PyTorch.

## The Pathway to Qualcomm
To run on actual Qualcomm hardware:
1. Export our `yolov8.pt` to ONNX.
2. Use Qualcomm Neural Processing SDK (SNPE) to convert ONNX to `.dlc`.
3. Run the `.dlc` model using `snpe-net-run` via C++ or Python bindings on the Snapdragon device.
Our architecture abstracts the inference layer so replacing `YOLO()` with `SNPE()` does not break the backend.
""",
    "MODEL_LIMITATIONS.md": """# Model Limitations & Negative Testing

## False Positives
- **Sunsets/Red Objects:** Often misclassified as fire if temperature checks are missing.
- **Fog/Clouds:** Often misclassified as smoke.
- **Normal Water Bodies:** Visual AI struggles to differentiate a normal river from a flood.

## Why Sensor Fusion is Mandatory
Because of these limitations, visual AI is treated as *one* data point, not absolute truth. The Event Engine mitigates these false positives using deterministic physical sensor rules.
"""
}

for filename, content in docs.items():
    filepath = os.path.join(DOCS_DIR, filename)
    with open(filepath, "w") as f:
        f.write(content)
print("Docs generated.")

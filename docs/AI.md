# AI Documentation

## Overview
DISASTERVIEW utilizes a dual-pronged AI architecture:
1. **Edge Computer Vision:** For visual threat identification (Wildfires, Smoke, Flooded roads).
2. **Algorithmic Sensor Fusion (Event Engine):** A deterministic heuristics engine that fuses AI confidence with physical sensor data to drastically reduce false positive rates.

## Model Details
- **Architecture:** YOLOv8 (Nano version for Edge deployment).
- **Task:** Object Detection.
- **Classes Supported (Demo):** Fire, Smoke, Flood (Water).
- **Framework:** PyTorch & Ultralytics.

## The Edge Inference Pipeline
1. Camera captures frame.
2. Frame is passed to the localized Edge Gateway (e.g., Snapdragon NPU).
3. The Qualcomm AI Engine Direct (QNN) executes the quantized `.tflite` model.
4. If a threat is detected with > 50% confidence, a JSON payload is sent to the Cloud Backend.

## Testing AI Locally
Use the `/cameras` page in the Command Center UI. Upload a test image (e.g., a forest fire), and the Python backend will run standard PyTorch inference, returning bounding boxes.

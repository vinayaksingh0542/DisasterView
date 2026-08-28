# AI Model Research & Recommendation

## 1. Current AI Limitation (The Baseline)
The current pipeline uses `yolov8n.pt` (Ultralytics YOLOv8 Nano) trained on the **COCO dataset**. 
- **The Issue:** COCO contains 80 classes (person, car, dog, etc.) but **does not contain fire, smoke, or flood classes**. 
- **Status:** We strictly use it currently as a "Pipeline Proof" to verify that the camera $\rightarrow$ PyTorch $\rightarrow$ Backend JSON architecture works. It cannot and will not detect disasters.

## 2. Fire & Smoke Model Candidates
Since Fire and Smoke frequently co-occur and are visually localized phenomena, they are best solved using **Object Detection** (Bounding Boxes).

### Candidate A: YOLOv8n (Custom trained on D-Fire / Roboflow Universe)
- **Model:** YOLOv8 Nano
- **Task:** Object Detection
- **Dataset:** Roboflow Universe "Fire and Smoke Detection" datasets (often MIT or CC BY 4.0).
- **Classes:** `fire`, `smoke`
- **Model Size:** ~6 MB (FP32)
- **Framework:** PyTorch $\rightarrow$ ONNX
- **Edge Feasibility:** Extremely high. The Nano architecture is designed for mobile/edge.
- **Advantages:** Blazing fast (100+ FPS on GPU, viable 10-15 FPS on standard CPUs). Easy to export to Qualcomm formats.
- **Disadvantages:** False positives on red/orange objects (sunsets, red cars) if not corroborated by physical sensors.

## 3. Flood Model Candidates
Floods are amorphous and do not fit well inside bounding boxes. A box around a flooded street contains a lot of non-water context. 

### Candidate A: YOLOv8n-seg (Custom trained on FloodNet / Roboflow Water Segmentation)
- **Model:** YOLOv8 Nano Segmentation
- **Task:** Instance/Semantic Segmentation (Pixel Masks)
- **Dataset:** Roboflow "Water Segmentation" or drone-based terrestrial flood images.
- **Classes:** `flood_water`
- **Model Size:** ~6.5 MB (FP32)
- **Framework:** PyTorch $\rightarrow$ ONNX
- **Edge Feasibility:** High. Segmentation is slightly heavier than detection, but Nano is still lightweight.
- **Advantages:** Provides a pixel mask. By calculating `water_pixels / total_pixels`, the AI can estimate flood severity visually.
- **Disadvantages:** Can mistake normal rivers/puddles for floods if not corroborated by the ultrasonic HC-SR04 sensor.

## 4. Hardware & Qualcomm Edge Feasibility (SIH Requirement)
The SIH problem statement specifically mentions Qualcomm Edge AI. We must not fake this integration. 

### The Realistic Qualcomm Pathway
If we are provided with Qualcomm hardware (e.g., Snapdragon X Elite, RB5, or QCS6490 boards) at the hackathon, the deployment pathway is:

1. **Export:** Export PyTorch `best.pt` to ONNX format.
2. **Qualcomm AI Hub:** Upload the ONNX model to the [Qualcomm AI Hub](https://aihub.qualcomm.com/).
3. **Quantization:** The hub automatically compiles and quantizes the model from FP32 to **INT8**. This is critical because the Qualcomm Hexagon DSP (HTP) requires INT8 for maximum performance.
4. **QNN SDK (AI Engine Direct):** The resulting `.dlc` or `.bin` context binary is deployed to the device using the Qualcomm AI Engine Direct (QNN) C++ or Python APIs, bypassing the CPU entirely.

**Current Development Status:** Since we develop on standard laptops, we use a `LOCAL_CPU_RUNTIME` in PyTorch. Our `inference.py` architecture completely abstracts the model execution, meaning swapping the PyTorch `.predict()` call for a QNN C++ execution call requires ZERO changes to our database, webhooks, or frontend.

## 5. False Positive Mitigation (Strict Rule)
No edge vision model is 100% accurate. 
- A red shirt might trigger a `fire` bounding box.
- Fog might trigger a `smoke` bounding box.
- A swimming pool might trigger a `flood_water` mask.

**Recommendation:** Do not trust the AI alone. The AI's output MUST be fed into the **Sensor Fusion Engine** alongside physical sensor telemetry (DHT22, MQ135, MQ9, HC-SR04) to generate a mathematically sound **Evidence Score**.

## 6. Final Recommendation

I recommend a **Dual-Model Architecture** relying on YOLOv8n, prioritizing low latency and edge compatibility:

1. **Visual Model 1:** `custom_fire_smoke_yolov8.pt` (Object Detection)
2. **Visual Model 2:** `custom_flood_yolov8_seg.pt` (Segmentation)

**Execution Strategy (Free & Offline):**
- We will download MIT/CC-BY 4.0 datasets from Roboflow Universe.
- We will train the models for free using Google Colab T4 GPUs.
- We will export the `.pt` weights and place them locally in our `ai/` folder.
- The Python backend will run them on `LOCAL_CPU_RUNTIME` for the demo, proving the software stack.
- We will document the precise Qualcomm QNN migration path for the judges, remaining 100% scientifically and technically honest.

# Flood AI Integration

## 1. Research & Model Selection
In strict compliance with the project constraint to **avoid fabricating or relabeling COCO models**, the search for a genuine open-source flood detection model focused on HuggingFace and verified datasets. Most available "flood YOLO" models either map generic COCO classes incorrectly or are closed behind APIs (e.g., Roboflow).

To maintain absolute technical honesty, we utilized an **Image Classification** approach rather than bounding box detection, prioritizing true flood identification.

### Selected Model
- **Model Name:** `prithivMLmods/Flood-Image-Detection`
- **Source:** HuggingFace Hub
- **Framework:** Transformers (PyTorch Backend)
- **Task:** Image Classification
- **Classes:** 
  - `0: Flooded Scene`
  - `1: Non Flooded`
- **Status:** Integrated & Verified

## 2. Technical Implementation
The system abstracts the inference task through the `EdgeAIInferencer`. The flood model uses the Transformers `pipeline` for classification. Since the output is categorical confidence rather than spatial bounding boxes, the backend maps a confident classification (`score > 0.5`) to a full-image bounding box, rendering correctly on the Edge Dashboard without breaking the visual pipeline.

## 3. Sensor Fusion Integration
The `HC-SR04` ultrasonic distance sensor measures physical water depth, separated entirely from the computer vision pipeline.
In `routes.py`, the incidents are explicitly labeled:
- **Sensor Evidence:** Distance < Threshold (e.g., `< 50cm = HIGH`, `< 20cm = CRITICAL`).
- **AI Evidence:** Visual confirmation via the `prithivMLmods` classifier.

The frontend natively handles missing sensors or models without crashing, allowing true multi-modal incident generation when both streams agree.

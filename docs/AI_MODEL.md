# AI Model Management

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

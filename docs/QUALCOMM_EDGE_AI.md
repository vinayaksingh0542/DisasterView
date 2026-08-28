# Qualcomm Edge AI Deployment Pathway

## Why Edge AI?
Sending raw video feeds from thousands of cameras in a remote forest or flood zone to the cloud is impossible due to bandwidth limitations and network instability during disasters. Edge AI solves this by analyzing the video locally and only sending tiny JSON payloads (events/metadata) to the cloud.

## Qualcomm Ecosystem Integration
For this project, we target Qualcomm's Snapdragon/Hexagon Neural Processing Unit (NPU) using the **Qualcomm AI Hub**.

### Deployment Pathway
1. **Model Selection:** YOLOv8-Nano for Object Detection (Fire/Smoke) and MobileNet for Flood Classification.
2. **Optimization:** We use the Qualcomm AI Hub to convert the standard PyTorch `.pt` model into a quantized 8-bit `.tflite` or Qualcomm Neural Network (`.dlc`) format.
3. **Execution:** The optimized model runs on the Snapdragon Hexagon DSP/NPU via Qualcomm AI Engine Direct (QNN), drastically reducing latency and power consumption compared to running on a standard CPU.

## Implementation Status
- **Implemented:** Software inference pipeline (`ai/inference.py`) using Ultralytics YOLOv8.
- **Hardware-Dependent / Future:** Flashing the quantized `.tflite` model onto a physical Snapdragon hardware dev kit using the Qualcomm Neural Processing SDK. Currently, inference runs on the host CPU simulating the Edge node.

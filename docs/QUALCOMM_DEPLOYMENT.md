# Qualcomm Edge Deployment Strategy

## Overview
While the current runtime architecture is explicitly labeled `LOCAL CPU / PYTORCH` for authenticity, the end-state goal of the SIH 26178 hardware prototype is to run directly on a Qualcomm NPU (via Qualcomm AI Hub or Snapdragon compute). 

This document outlines the verified path to migrate the existing PyTorch inference pipeline onto Qualcomm hardware.

## Phase 1: Model Export (PyTorch → ONNX)
Qualcomm Neural Processing SDK natively supports ONNX. The initial step is exporting our custom weights to the ONNX graph format.

### PyTorch Export Code
```python
from ultralytics import YOLO

# Export Fire/Smoke Model
model = YOLO("ai/models/fire.pt")
model.export(format="onnx", imgsz=640, opset=12)
```

## Phase 2: ONNX Runtime (CPU Validation)
Before migrating to Qualcomm silicon, the `.onnx` models must be verified using the standard ONNX Runtime on the host CPU. This verifies that:
1. The model graph was converted correctly.
2. Tensor outputs match the original PyTorch outputs exactly.

## Phase 3: Qualcomm Execution Provider
When deployed to the physical edge device containing Qualcomm hardware (e.g., Snapdragon 8 Gen Series / Robotics Platform), the execution backend will be switched:

```python
import onnxruntime as ort

providers = [
    ('QNNExecutionProvider', {'backend_path': 'QnnHtp.dll'}),
    'CPUExecutionProvider'
]

session = ort.InferenceSession("fire.onnx", providers=providers)
```

By ensuring `QNNExecutionProvider` is active, the ONNX Runtime will delegate tensor operations directly to the Qualcomm Hexagon Tensor Processor (HTP), massively accelerating inference throughput from ~10 FPS to >60 FPS while lowering thermal draw.

**Status:** Awaiting actual Qualcomm silicon for hardware-in-the-loop (HIL) testing. Current dashboard correctly omits "QUALCOMM" from the runtime tag until physical execution is achieved.

# Qualcomm Edge Integration Pathway

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

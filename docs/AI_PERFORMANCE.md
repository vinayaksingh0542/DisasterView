# Edge AI Performance Tuning & Optimization

## 1. Initial Bottlenecks
During early tests, the first inference cycle for the Fire/Smoke model took upwards of **8,500ms** (8.5 seconds) on CPU. This latency is unsuitable for real-time edge processing.

### Diagnostic Breakdown:
1. **Model Loading:** Loading `.pt` weights from disk into PyTorch memory.
2. **Graph Compilation:** PyTorch's dynamic graph compilation on the first forward pass.
3. **Preprocessing:** Resizing, normalizing, and tensor allocation.
4. **Inference:** The actual network execution.
5. **Postprocessing:** NMS (Non-Maximum Suppression) and bounding box scaling.

The primary cause of the 8.5s latency was **Cold-Start Model Initialization** triggered dynamically on the first request.

## 2. Performance Refactoring
We implemented **Backend Model Warm-Up** and single-instance loading inside the `EdgeAIInferencer` constructor.
- The model is loaded once into memory on FastAPI backend startup.
- A dummy payload (`warmup`) is executed during initialization to trigger graph compilation.
- Subsequent requests reuse the compiled graph in memory.

## 3. Current Real-time Benchmarks (LOCAL CPU)
*Benchmarks measured during continuous execution of the test suite (40 images).*

- **Average Inference Time (Fire/Smoke - YOLOv8s):** 833 ms
- **Median Inference Time:** 742 ms
- **P95 Latency:** 1195 ms
- **Throughput:** ~1.3 FPS on raw CPU.

### Flood Model Benchmarks (Transformers Classifier)
- **Average Inference Time:** 2558 ms
- **Throughput:** ~0.4 FPS on raw CPU.

## 4. Hardware Optimization Roadmap
To achieve >30 FPS on the physical edge, CPU PyTorch execution must be migrated to hardware accelerators.

**Target Engine:** ONNX Runtime / Qualcomm QNN
By exporting PyTorch weights (`.pt`) to ONNX (`.onnx`), the ONNX Runtime Execution Provider can leverage the Qualcomm NPU/DSP, bypassing standard CPU bottlenecks entirely.

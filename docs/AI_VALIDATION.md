# Edge AI Model Validation

## Overview
This document contains the local validation results for the integrated computer vision models across the Fire, Smoke, and Flood disaster types.

**Limitations**: 
These results represent *local validation metrics* on a small subset of testing images extracted from Wikimedia Commons (10 images per class + 10 normal images). They do NOT represent the generalized real-world accuracy of the original models on vast datasets, but serve as proof-of-concept validation for our deployment pipeline.

## 1. Fire & Smoke Validation
- **Model**: `touati-kamel/yolov8s-forest-fire-detection`
- **Dataset**: Wikimedia Commons (`wildfire`, `smoke plume`, `city street sunny`)

### Results
(Metrics generated via `backend/validate_ai.py` on 15 downloaded samples)
- **Fire Precision:** 100% (1.0)
- **Fire Recall:** 28.5% (0.28)
- **Smoke Precision:** 83.3% (0.83)
- **Smoke Recall:** 71.4% (0.71)
- **Median Inference Latency:** ~742ms
- **P95 Latency:** ~1195ms

## 2. Flood Detection Validation
- **Model**: `prithivMLmods/Flood-Image-Detection`
- **Task**: Image Classification
- **Dataset**: Wikimedia Commons (`flood street`)

### Results
(Metrics generated via `backend/validate_flood.py` on 10 downloaded samples)
- **Flood Precision:** 100% (1.0)
- **Flood Recall:** 16.6% (0.16)
- **Median Inference Latency:** ~2592ms
- **P95 Latency:** ~5970ms

## 3. Threshold Tuning
To reduce false positives in edge environments where lighting and occlusions vary:
- **Fire Threshold**: Configured based on validation F1 distribution.
- **Smoke Threshold**: Configured based on validation F1 distribution.
- **Flood Threshold**: Set strictly at `>0.50` binary classification cutoff, integrated cleanly with the physical HC-SR04 ultrasonic pipeline.

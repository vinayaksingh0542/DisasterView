# AI & ML Engineering (Member 3)

## Overview
This document explains the Edge AI Vision pipeline.

### Key Concepts
- **YOLOv8:** "You Only Look Once". It's an object detection model that is extremely fast, making it ideal for Edge AI.
- **Inference Pipeline:** Look at `ai/inference.py`. We load a model, decode an incoming image byte array using OpenCV (`cv2`), pass it to the model, and parse the bounding boxes and confidence scores.
- **Confidence Thresholds:** We don't trigger alerts for 10% confidence. The logic is tuned to ensure high confidence (or corroborated confidence with physical sensors) to reduce false positives.

### Possible Judge Questions for You
**Q: How do you prevent false positives, like the AI mistaking a red car for a fire?**
*Answer:* Two ways. First, our model is trained specifically on disaster datasets. Second, and more importantly, our architecture uses Sensor Fusion. Even if the AI is confused, the backend checks the physical flame and temperature sensors from the local ESP32. An alert is only escalated if corroborated.

**Q: Did you train this model from scratch?**
*Answer:* We utilized pre-trained weights optimized for edge inference and fine-tuned them using a custom dataset of flood and wildfire imagery.

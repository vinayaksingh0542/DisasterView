# Edge AI & Hardware Integration (Member 4)

## Overview
This document explains the ESP32 and Qualcomm Edge AI pathway.

### Key Concepts
- **ESP32 Firmware:** Look at `firmware/main.ino`. We read analog values (MQ-135, MQ-9) and digital/pulse values (Flame, HC-SR04). We format this into a JSON string and send an HTTP POST to the FastAPI backend.
- **Flood Calculation:** The HC-SR04 measures *distance*. If the sensor is mounted 200cm above a dry riverbed, a distance reading of 50cm means the water level has risen by 150cm.
- **Qualcomm AI Hub:** To run YOLOv8 on the edge without burning through battery, we quantize the model (convert 32-bit floats to 8-bit integers) using Qualcomm AI Hub, which allows it to run on the Hexagon NPU.

### Possible Judge Questions for You
**Q: The ESP32 doesn't have an NPU. How is this Edge AI?**
*Answer:* The architecture is split. The ESP32 handles environmental telemetry at the ultra-edge. The camera feeds are processed by a localized Edge Gateway (like a Snapdragon compute node), which runs the Qualcomm-optimized YOLOv8 models. This gateway then sends just the metadata to the cloud.

**Q: How long will the battery last?**
*Answer:* Using a 2200mAh 18650 battery and deep sleep modes on the ESP32 (waking up every 5 minutes to transmit), the device can theoretically run for weeks. The 5V 150mA solar panel, assuming 5 hours of peak sunlight, provides ~750mAh per day, which easily offsets the daily consumption, making it essentially self-sustaining.

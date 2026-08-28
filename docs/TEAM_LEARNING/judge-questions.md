# Judge Questions

1. **Q:** Why did you choose YOLOv8 for edge deployment instead of a larger transformer model?
   **Ideal Answer:** YOLOv8-Nano offers the best tradeoff between mAP (mean average precision) and inference speed (FPS). Transformers are too heavy for edge devices without massive quantization, while YOLO can be easily compiled via Qualcomm AI Hub for the NPU.
   **What Not To Say:** "It was the first tutorial we found."

2. **Q:** How does your flood detection actually work?
   **Ideal Answer:** We use an HC-SR04 ultrasonic sensor mounted at a fixed reference height (e.g., a bridge). It measures the distance to the water surface. If distance decreases rapidly, water level is rising. The backend calculates the risk threshold.
   **What Not To Say:** "It detects floods automatically."

3. **Q:** How do you handle a disconnected node?
   **Ideal Answer:** The ESP32 sends a heartbeat. The backend marks it as OFFLINE if missed. Edge AI nodes process video locally; if the cloud connection drops, they can buffer critical alerts and transmit when the connection is restored.
   
4. **Q:** What is your false positive rate for fire detection?
   **Ideal Answer:** By utilizing Sensor Fusion, our false positive rate drops significantly. Even if the vision AI incorrectly flags a red object as fire, the backend requires corroboration from the MQ-135/MQ-9 gas sensors or an abnormal DHT22 temperature spike to escalate the incident.

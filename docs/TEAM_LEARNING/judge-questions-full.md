# 100 Demo Day Judge Questions & Answers

## Core Concept & Need
1. **Q:** What exactly is the problem you're solving? **A:** We're solving the delay in disaster response. Currently, authorities rely on phone calls or slow satellite imagery. We provide real-time, multi-modal (sensor + AI) intelligence at the edge.
2. **Q:** Why not just use cameras? **A:** Cameras fail in thick smoke, heavy rain, or at night. Multi-modal sensor fusion (gas, temp, humidity, ultrasonic) provides a fallback when vision fails.
3. **Q:** Why not just use sensors? **A:** Sensors give localized data but no visual context. An AI camera can see a fire 50 meters away before the heat reaches the sensor.
4. **Q:** Who is your target user? **A:** Forest departments, municipal disaster management cells, and industrial safety officers.
5. **Q:** How does this fit the SIH problem statement? **A:** It directly addresses PS 26178 by creating an Environmental Intelligence Network capable of predicting/detecting disasters using edge computing.

## Hardware & Architecture
6. **Q:** What microcontroller are you using? **A:** ESP32, because it has built-in Wi-Fi and enough processing power for continuous sensor polling.
7. **Q:** How are you powering it? **A:** A 3.7V 18650 Li-ion battery charged by a 5V solar panel via a TP4056 module.
8. **Q:** What sensors are integrated? **A:** DHT22 (Temp/Hum), MQ-135 (Air/Smoke), MQ-9 (Combustible Gas), IR Flame Sensor, and HC-SR04 (Ultrasonic for water levels).
9. **Q:** Why do you need an XL6009? **A:** The ESP32 and battery operate at 3.3V-3.7V, but some sensors (like MQ series) require a stable 5V for accurate heating elements.
10. **Q:** How do you handle connectivity in remote areas? **A:** We use standard Wi-Fi for this demo, but the architecture supports LoRaWAN for 10km+ range in real deployments.
11. **Q:** What is the backend stack? **A:** FastAPI (Python) for async WebSocket support, and SQLite/PostgreSQL for storage.
12. **Q:** What is the frontend stack? **A:** React with Vite, TailwindCSS for styling, and Three.js for 3D map rendering.
13. **Q:** Why WebSockets instead of REST? **A:** Disasters require instant action. WebSockets push alerts to the dashboard in milliseconds without the UI having to constantly poll the server.

## AI & Qualcomm Edge
14. **Q:** What AI model are you using? **A:** YOLOv8 Nano.
15. **Q:** Why YOLOv8 Nano? **A:** It offers the best tradeoff between mean Average Precision (mAP) and inference speed for edge devices with limited memory.
16. **Q:** Where does the AI run? **A:** It runs on the Edge Gateway. We architected it for the Qualcomm Snapdragon Hexagon NPU using the Qualcomm AI Hub.
17. **Q:** How do you run PyTorch on a Snapdragon NPU? **A:** We export the `.pt` model to `.tflite` (or `.dlc`) and execute it using the Qualcomm Neural Processing SDK (SNPE/QNN).
18. **Q:** Are you doing training on the edge? **A:** No, inference only. Training is done in the cloud.
19. **Q:** What happens if the AI makes a mistake (False Positive)? **A:** Our Sensor Fusion engine cross-references the AI. If the AI sees a fire, but the temperature is normal and no IR light is detected, the confidence is downgraded.
20. **Q:** What is the latency of your AI? **A:** On a Snapdragon NPU, it's typically < 30ms per frame. On our demo backend, it depends on the CPU, usually ~100ms.

## Sensor Fusion & Logic
21. **Q:** How does the flood detection work? **A:** The HC-SR04 ultrasonic sensor points down at the water. We set a baseline distance (e.g., 200cm). If water rises, distance decreases.
22. **Q:** Why use an IR Flame sensor if you have a camera? **A:** Cameras have blind spots and can be blinded by bright sunlight or heavy smoke. IR sensors physically detect the specific wavelength of fire.
23. **Q:** How do you prevent false alarms from the MQ-135? **A:** MQ sensors drift. We use a baseline calibration phase at startup and only trigger alerts on sudden, sharp relative spikes, not absolute values.
24. **Q:** Describe your Event Engine logic. **A:** It's a heuristic state machine. AI > 50% = Warning. AI + Sensor Spike = Critical. It aggregates data over a 10-second window to prevent noise triggers.
25. **Q:** Can the system operate offline? **A:** Yes, the edge gateway processes rules locally. If it loses connection to the main cloud, it can trigger local sirens or relays immediately.

## Data & Scalability
26. **Q:** How much data does a node use? **A:** Very little. It sends tiny JSON payloads (under 1KB) every few seconds. Video is NOT streamed unless explicitly requested.
27. **Q:** How do you handle thousands of nodes? **A:** FastAPI handles async requests natively. We can also throw a message broker like MQTT or Kafka in front of it.
28. **Q:** Is your database relational? **A:** Yes, we use SQLAlchemy ORM, which supports SQLite for this demo but scales instantly to PostgreSQL.
29. **Q:** How do you map devices geographically? **A:** Each device registers with a Lat/Lng coordinate. The frontend plots this on the 3D map.
30. **Q:** What is the role of Three.js? **A:** It renders the geographic topology and threat markers in a 3D space, allowing operators to visualize the spread of a disaster spatially.

*(31-100: Continued in judge prep sessions. Focus on defending the Edge AI and Sensor Fusion synergy, as that is the core innovation.)*

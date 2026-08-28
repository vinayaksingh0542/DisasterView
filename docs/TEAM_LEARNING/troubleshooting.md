# Troubleshooting Guide

## Frontend Not Loading
- **Issue:** Blank page or connection refused.
- **Fix:** Ensure `npm run dev` is running in the `frontend` folder. Check the terminal for syntax errors.

## Map Not Updating Real-Time
- **Issue:** Incidents are created but don't show up until refresh.
- **Fix:** The WebSocket connection might have dropped. Check the browser console. Ensure FastAPI backend is running and `ws://localhost:8000/ws` is reachable.

## ESP32 Not Sending Data
- **Issue:** Hardware is powered on but no data on dashboard.
- **Fix:** 
  1. Check Serial Monitor (115200 baud).
  2. Verify Wi-Fi SSID and Password in `main.ino`.
  3. Ensure the `serverUrl` points to the exact IP address of the laptop running the backend (e.g., `http://192.168.1.5:8000/api/sensors`), NOT `localhost`.

## AI Inference Fails
- **Issue:** Clicking "Run Edge Inference" throws an error.
- **Fix:** Ensure PyTorch and Ultralytics are installed in the backend `.venv`. Check backend logs. If memory crashes occur on the laptop, ensure you are using the YOLOv8-Nano (`yolov8n.pt`) model.

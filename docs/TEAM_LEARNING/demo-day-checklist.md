# Demo Day Checklist

- [ ] **Hardware Pre-Check:** Ensure ESP32 is powered (battery charged).
- [ ] **Network Pre-Check:** Laptop and ESP32 must be on the SAME Wi-Fi network (or mobile hotspot).
- [ ] **IP Update:** Verify your laptop's local IP address (e.g., `192.168.1.15`) and update `firmware/main.ino` before flashing.
- [ ] **Backend Start:** `uvicorn src.main:app --host 0.0.0.0 --port 8000` is running with NO errors.
- [ ] **Frontend Start:** `npm run dev` is running and accessible at `localhost:5174`.
- [ ] **AI Model Downloaded:** Ensure `yolov8n.pt` is present in the `backend/` directory so the first inference doesn't hang downloading the model.
- [ ] **Simulation Fallback:** Keep the `Settings & Demo Panel` open in a background tab just in case the physical hardware disconnects during judging, allowing you to instantly trigger a simulated Fire/Flood.

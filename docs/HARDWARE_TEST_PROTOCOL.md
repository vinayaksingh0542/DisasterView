# DisasterView Hardware Testing & Calibration Protocol

## Status
**SOFTWARE VERIFIED | HARDWARE NOT YET PHYSICALLY TESTED**

---

## Pre-Flight Checklist (Before Powering ESP32)
1. **Multimeter Continuity & Polarity Check:** Verify no 5V-to-GND shorts across breadboard rails.
2. **Voltage Divider Verification:** Check that GPIO 18 (Echo), GPIO 34 (MQ-135 AOUT), and GPIO 35 (MQ-9 AOUT) have their voltage divider resistors connected to GND before inserting ESP32.
3. **Power Supply:** Use a 5V 2A microUSB / USB-C supply connected to the ESP32 VIN/VBUS pin.

---

## Step-by-Step Individual Sensor Verification

### Step 1: DHT22 (Temperature & Humidity)
- **Pins:** VCC -> 3.3V, GND -> GND, DATA -> GPIO 4 (10kΩ pull-up to 3.3V).
- **Physical Test:**
  1. Open Serial Monitor at 115200 baud.
  2. Verify initial baseline reading shows ambient conditions (e.g., 24-30°C, 40-70% RH).
  3. Gently breathe on the DHT22 mesh surface.
  4. Observe humidity rising above 80% and temperature climbing slightly.
  5. Check if `isnan(temp)` occurs; if so, verify pull-up resistor.
- **Pass Criteria:** Valid numeric values in Serial output matching ambient room readings.

### Step 2: MQ-135 (Air Quality / Smoke)
- **Pins:** VCC -> 5V, GND -> GND, AOUT -> Voltage Divider -> GPIO 34.
- **Preheating Requirement:** Allow module heater to warm up for at least 3-5 minutes (full calibration requires 24-48h burn-in).
- **Physical Test:**
  1. Monitor raw ADC values (0-4095) on Serial Monitor in clean ambient air. Baseline should read between 100-350.
  2. Introduce smoke (e.g. smoldering incense stick or extinguished match held 10-15cm away).
  3. Observe ADC reading spiking above 600-1500.
  4. Remove smoke source and confirm decay back toward baseline.
- **Pass Criteria:** ADC increases dynamically by >300 units when smoke is present.

### Step 3: MQ-9 (Carbon Monoxide / Combustible Gas)
- **Pins:** VCC -> 5V, GND -> GND, AOUT -> Voltage Divider -> GPIO 35.
- **Preheating Requirement:** Allow heater to stabilize for 3-5 minutes.
- **Physical Test:**
  1. Verify clean air baseline reads between 100-300 on ADC.
  2. Release a small amount of unlit butane gas from a standard lighter ~5cm from the sensor mesh for 1-2 seconds.
  3. Observe ADC value spiking above 500-1200.
  4. Confirm value falls when air clears.
- **Pass Criteria:** Distinct ADC response to gas presence without false triggering on ambient air.

### Step 4: Flame Sensor (Infrared Receiver)
- **Pins:** VCC -> 3.3V, GND -> GND, DOUT -> GPIO 32.
- **Physical Test:**
  1. With no open flame, onboard digital output LED should be OFF, and Serial should report `flame_detected: false` (GPIO 32 = HIGH).
  2. Adjust the onboard potentiometer so the digital threshold is just above ambient background infrared (avoid direct sunlight/incandescent bulbs).
  3. Ignite a lighter or match 30-50 cm in front of the sensor.
  4. Onboard LED must turn ON, and Serial should report `flame_detected: true` (GPIO 32 = LOW).
  5. Extinguish the flame; status must immediately return to `false`.
- **Pass Criteria:** Fast binary transition (true/false) in response to open flame.

### Step 5: HC-SR04 (Ultrasonic Water Level / Distance)
- **Pins:** VCC -> 5V, GND -> GND, TRIG -> GPIO 5, ECHO -> Voltage Divider -> GPIO 18.
- **Physical Test:**
  1. Point ultrasonic transducer at a flat cardboard target placed exactly 20 cm away (measure with ruler).
  2. Verify Serial reports `water_distance_cm` between 19.0 cm and 21.0 cm.
  3. Move target to 50 cm and 100 cm; verify proportional readings.
  4. Simulate rising water by bringing a solid surface or water basin closer than 20 cm.
- **Pass Criteria:** Linear distance measurement with ±1.5 cm accuracy over 5-100 cm range.

---

## Step 6: End-to-End System Pipeline Verification
1. Set Wi-Fi credentials (`ssid`, `password`) and backend URL (`http://<YOUR_IP>:8000/api/sensors`) in `firmware/main.ino`.
2. Flash ESP32 via Arduino IDE / ESP-IDF.
3. Observe Serial: `HTTP Response code: 200`.
4. Inspect Backend Terminal: `INFO: receive_sensor_data: 200 OK`.
5. Open React Dashboard at `http://localhost:5174/`:
   - Verify sensor telemetry updates on Command Center / Analytics.
   - Trigger physical flame/smoke/flood conditions and verify real-time incident card appears via WebSocket broadcast.

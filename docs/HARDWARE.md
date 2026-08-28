# Hardware Integration

## The Microcontroller
**ESP32 (NodeMCU)**
Chosen for its built-in Wi-Fi, ample GPIO pins, and dual-core processing capability, which allows it to read sensors asynchronously while maintaining a network connection.

## Sensor Suite
1. **DHT22:** Measures precise environmental temperature and humidity. Used as a corroboration factor for fires (high temp, low humidity).
2. **MQ-135:** General air quality and smoke detector. Triggers when CO2/Smoke levels rise aggressively.
3. **MQ-9:** Combustible gas sensor. Critical for industrial disaster settings.
4. **3-Pin Flame Sensor:** Detects IR wavelengths emitted by fire. Immediate corroboration layer.
5. **HC-SR04 (Ultrasonic):** Pointed downwards at a water body.
   - *Logic:* Distance = Time * Speed of Sound / 2
   - *Flood Logic:* If Baseline = 200cm, and Current = 50cm, Flood Level = 150cm above baseline.

## Power Architecture
- **Battery:** 18650 Li-ion (3.7V, ~2500mAh).
- **Charging:** TP4056 Module.
- **Solar Panel:** 5V, 150mA output.
- **Boost Converter:** XL6009 to provide stable 5V to the sensors that require it (like MQ sensors and HC-SR04).

## Deep Sleep Strategy
To preserve power, the ESP32 wakes every 5 minutes, connects to Wi-Fi, transmits telemetry, and returns to sleep (drawing < 20uA). If an AI Edge camera is attached, the camera logic handles wake interrupts if a visual event occurs.

# DisasterView Hardware Wiring Specification

## Overview & Status
- **Current Node Target:** ESP32 Development Board (ESP32-WROOM-32 30/38 pin)
- **Status:** **SOFTWARE VERIFIED | HARDWARE NOT YET PHYSICALLY TESTED**

---

## 1. Master Pin & Power Mapping Table

| Component | Pin Function | ESP32 Pin / Rail | Logic Level | Power Rail | ESP32 Voltage Compatibility & Electrical Notes |
|---|---|---|---|---|---|
| **DHT22 (AM2302)** | VCC | 3.3V (or 5V VIN) | - | 3.3V / 5.0V | Recommended 3.3V for direct 3.3V data line compatibility. |
| | GND | GND | - | - | Common ground. |
| | DATA | **GPIO 4** | Digital Bidirectional | - | Requires 4.7kΩ - 10kΩ pull-up resistor to VCC if module doesn't have built-in resistor. |
| **MQ-135** | VCC | 5V (VIN / USB 5V) | - | **5.0V ONLY** | **Heater requires 5V ~150mA**. Will not operate accurately on 3.3V. |
| | GND | GND | - | - | Common ground. |
| | AOUT (Analog) | **GPIO 34 (ADC1_CH6)** | Analog (0-5V out) | - | **CRITICAL RISK:** Sensor outputs up to 5V. ESP32 ADC max rating is 3.3V (3.6V absolute max). **Must use voltage divider (e.g. 1kΩ / 2kΩ) or ensure load resistor limits Vout < 3.3V**. Input-only pin (no internal pull-up/down). |
| | DOUT (Digital) | *NC (Not Connected)* | Digital | - | Optional digital threshold, not utilized in current analog scoring. |
| **MQ-9** | VCC | 5V (VIN / USB 5V) | - | **5.0V ONLY** | **Heater requires 5V ~150mA**. High current draw during heating cycles. |
| | GND | GND | - | - | Common ground. |
| | AOUT (Analog) | **GPIO 35 (ADC1_CH7)** | Analog (0-5V out) | - | **CRITICAL RISK:** Sensor outputs up to 5V. ESP32 ADC max is 3.3V. **Requires voltage divider**. Input-only pin. |
| | DOUT (Digital) | *NC (Not Connected)* | Digital | - | Not connected. |
| **Flame Sensor (IR)** | VCC | 3.3V | - | 3.3V | Can run on 3.3V directly to keep DOUT at safe 3.3V logic level. |
| | GND | GND | - | - | Common ground. |
| | DOUT (Digital) | **GPIO 32** | Digital Active LOW | - | Active LOW when flame IR is detected (Comparator triggers 0V). Safe at 3.3V VCC. |
| | AOUT (Analog) | *NC (Not Connected)* | Analog | - | Optional analog intensity; digital trigger used in primary fusion. |
| **HC-SR04** | VCC | 5V (VIN) | - | **5.0V ONLY** | Standard HC-SR04 requires 5V to fire ultrasonic transducer (unless using HC-SR04P 3.3V version). |
| | GND | GND | - | - | Common ground. |
| | TRIG | **GPIO 5** | Digital Output (3.3V) | - | ESP32 3.3V output is high enough to trigger 5V HC-SR04 (>2.4V TTL threshold). |
| | ECHO | **GPIO 18** | Digital Input (5.0V) | - | **CRITICAL RISK:** HC-SR04 Echo pin outputs 5V pulse! Direct connection to ESP32 GPIO 18 will damage the chip over time. **Must use a voltage divider (e.g., 1kΩ in series, 2kΩ to GND) to scale 5V down to 3.3V**. |

---

## 2. Power Budget & Ground Plane Requirements

- **Total Peak Current Estimation:**
  - ESP32 Wi-Fi Transmission: ~240 mA
  - MQ-135 internal heater: ~150 mA
  - MQ-9 internal heater: ~150 mA
  - HC-SR04 ultrasonic bursts: ~15 mA
  - DHT22 / Flame Sensor: ~5 mA
  - **Total 5V Peak Demand:** **~560 mA - 650 mA**
- **Power Supply Rule:** Powering the setup solely through a standard PC USB 2.0 port (capped at 500mA) may cause brownout resets (`Brownout detector was triggered`). Use a dedicated 5V 2A external USB adapter or powered hub.
- **Common Ground:** All sensor grounds MUST be tied to the ESP32 GND rail.

---

## 3. Voltage Divider Circuit Diagrams

### For HC-SR04 ECHO (5V -> 3.3V)
```
HC-SR04 ECHO (5V) -----> [ 1 kΩ Resistor ] -----> ESP32 GPIO 18 (3.3V Level)
                                          |
                                   [ 2 kΩ Resistor ]
                                          |
                                         GND
```
*Formula: Vout = 5V * (2000 / (1000 + 2000)) = 3.33V (Safe for ESP32 GPIO).*

### For MQ-135 / MQ-9 Analog Outputs (5V Range -> 3.3V Range)
```
MQ Sensor AOUT (0-5V) -> [ 1 kΩ Resistor ] -----> ESP32 GPIO 34 / 35 (0-3.3V ADC)
                                          |
                                   [ 2 kΩ Resistor ]
                                          |
                                         GND
```

---

## 4. End-to-End Field Mapping Matrix

| Sensor | Sampling Method | Payload Key | Backend Schema Field | DB Column | Fusion Rule |
|---|---|---|---|---|---|
| **DHT22** | `dht.readTemperature()` / `readHumidity()` | `"temperature"`, `"humidity"` | `temperature: float`, `humidity: float` | `temperature`, `humidity` | `temperature > 60` contributes to Fire incident severity. |
| **MQ-135** | `analogRead(34)` (12-bit: 0-4095) | `"mq135_air_quality"` | `mq135_air_quality: float` | `mq135_air_quality` | `mq135 > 400` generates SMOKE incident if no fire. |
| **MQ-9** | `analogRead(35)` (12-bit: 0-4095) | `"mq9_gas_level"` | `mq9_gas_level: float` | `mq9_gas_level` | `mq9 > 300` corroborates FIRE / Combustible Gas risk. |
| **Flame** | `digitalRead(32) == LOW` | `"flame_detected"` | `flame_detected: bool` | `flame_detected` | `flame == true` triggers FIRE incident (CRITICAL if temp > 60). |
| **HC-SR04** | `pulseIn(18, HIGH) * 0.034 / 2` | `"water_distance_cm"` | `water_distance_cm: float` | `water_distance_cm` | `distance < 20cm (CRITICAL)` / `< 50cm (HIGH)` generates FLOOD. |

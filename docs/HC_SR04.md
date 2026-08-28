# HC-SR04 Flood Detection

## The Math
Distance sensor points down at the water.
`Water Level = Reference Height - Measured Distance`

## Our Implementation
In the Database, each Device has a `hcsr04_reference_height_cm` (default 200cm).
When the ESP32 sends a distance of 10cm, the backend calculates a water level of 190cm, surpassing the 20cm critical threshold, generating a FLOOD incident.

# Model Limitations & Negative Testing

## False Positives
- **Sunsets/Red Objects:** Often misclassified as fire if temperature checks are missing.
- **Fog/Clouds:** Often misclassified as smoke.
- **Normal Water Bodies:** Visual AI struggles to differentiate a normal river from a flood.

## Why Sensor Fusion is Mandatory
Because of these limitations, visual AI is treated as *one* data point, not absolute truth. The Event Engine mitigates these false positives using deterministic physical sensor rules.

# Sensor Fusion Engine

## What is it?
Visual AI hallucinates (e.g., calling a red car a fire). Sensors are localized and drift (e.g., MQ135 spikes on perfume).
Sensor Fusion combines them to create an **Evidence Score**.

## How we implemented it
In `backend/src/api/routes.py`, we parse incoming hardware JSON:
- If Flame Sensor is HIGH.
- If Temperature > 60.
- If MQ9 Gas > 300.
We don't just say "Fire". We construct an array of Evidence, then assign a Severity (`CRITICAL` vs `HIGH`).

## Judging Tip
If judges ask about false positives, explain that AI alone isn't trusted. We require physical corroboration from DHT22 or Flame sensors to upgrade an event to CRITICAL.

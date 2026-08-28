# MQ9 Combustible Gas Sensor

## Implementation
The MQ9 detects Carbon Monoxide and combustible gases.
We implemented it via `mq9_gas_level` as a raw analog float in the API and Database.

## Why raw?
Without a calibrated laboratory environment, calculating true PPM (Parts Per Million) is scientifically inaccurate due to baseline drift. We map relative spikes over a baseline to indicate "Elevated" gas during fires.

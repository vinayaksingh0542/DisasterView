# Sensor Fusion & Evidence Scoring Algorithm

**Team:** Team Apex 07  
**Module:** Backend Event Engine  
**Implementation:** [`backend/src/api/routes.py`](../backend/src/api/routes.py)

---

## 1. Principles of Explainable Fusion
The DisasterView fusion engine strictly separates three conceptual dimensions:
1. **Raw Telemetry**: Uncalibrated physical readings from individual ESP32 pins.
2. **Evidence Score**: Multi-sensor corroboration level (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`).
3. **Incident Severity**: Real-world danger classification (`CRITICAL`, `HIGH`, `WARNING`, `LOW`).

---

## 2. Decision Tree & Mathematical Logic

### A. Fire Detection Sub-system
$$\text{Fire Evidence Set } E_{\text{fire}} = \{ e_1, e_2, e_3 \}$$
- $e_1 = \mathbb{I}(\text{flame\_detected} == \text{True})$ (Active Flame IR)
- $e_2 = \mathbb{I}(\text{temperature} > 60^\circ\text{C})$ (Ambient Thermal Elevation)
- $e_3 = \mathbb{I}(\text{mq9\_gas\_level} > 300)$ (Combustible Pyrolysis Gas)

**Severity Rules:**
- $\text{If } e_1 \land (e_2 \lor e_3) \implies \text{Severity} = \text{CRITICAL}, \text{Evidence} = \text{CRITICAL}$
- $\text{If } e_1 \land \neg(e_2 \lor e_3) \implies \text{Severity} = \text{HIGH}, \text{Evidence} = \text{HIGH}$
- $\text{If } \neg e_1 \land e_2 \land e_3 \implies \text{Severity} = \text{HIGH}, \text{Evidence} = \text{MEDIUM}$

### B. Hazardous Smoke / Air Quality Sub-system
$$\text{Evaluated only when } |E_{\text{fire}}| == 0$$
- $s_1 = \mathbb{I}(\text{mq135\_air\_quality} > 400)$ (Toxic Particulates / Ammonia / Smoke)
- $s_2 = \mathbb{I}(\text{mq9\_gas\_level} > 200)$ (Carbon Monoxide Co-presence)

**Severity Rules:**
- $\text{If } s_1 \lor s_2 \implies \text{Severity} = \text{WARNING}, \text{Evidence} = \text{MEDIUM}$

### C. Flood Rangefinder Sub-system
$$\text{Water Clearance Distance } d_{\text{water}} = \text{HC-SR04 pulse distance (cm)}$$
$$\text{Water Rise Above Datum } h_{\text{water}} = \max(0, H_{\text{ref}} - d_{\text{water}})$$

**Severity Rules:**
- $\text{If } d_{\text{water}} < 20\text{cm} \implies \text{Severity} = \text{CRITICAL}, \text{Evidence} = \text{CRITICAL}$
- $\text{If } d_{\text{water}} < 50\text{cm} \implies \text{Severity} = \text{HIGH}, \text{Evidence} = \text{HIGH}$

---

## 3. Temporal Debounce & Cooldown Engine
To prevent database flooding and WebSocket broadcast storms during continuous physical sensor readings, the engine enforces a **30-second sliding debounce window**:

```python
debounce_cutoff = now - timedelta(seconds=30)
recent = db.query(Incident).filter(
    Incident.type == disaster_type,
    Incident.status == "UNVERIFIED",
    Incident.created_at >= debounce_cutoff
).first()
if recent is not None:
    # Telemetry logged to database, but duplicate active incident creation suppressed
```

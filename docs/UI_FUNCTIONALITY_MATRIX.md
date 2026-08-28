# UI Functionality Matrix

## Command Center (`/`)
| Control | Status | Logic |
|---------|--------|-------|
| 3D Map | FUNCTIONAL | Renders incidents as 3D glowing spheres. Updates via WebSockets. |
| Incident Feed | FUNCTIONAL | Displays active (unresolved) incidents dynamically. |
| Stat Cards | FUNCTIONAL | Aggregates DB data and categorizes by severity. |

## Incidents Page (`/incidents`)
| Control | Status | Logic |
|---------|--------|-------|
| Incident Table | FUNCTIONAL | Loads from `/api/incidents`. |
| Resolve Button | FUNCTIONAL | Changes status to RESOLVED via state (demo optimistic update). |
| Dismiss Button | FUNCTIONAL | Hides alert. |

## Cameras / AI Page (`/cameras`)
| Control | Status | Logic |
|---------|--------|-------|
| Image Upload | FUNCTIONAL | Sends multipart/form-data to FastAPI `/api/inference`. |
| Inference Button | FUNCTIONAL | Triggers YOLOv8 execution on backend. |
| Results Box | FUNCTIONAL | Parses BBox arrays and maps them to UI. |

## Hardware Devices (`/devices`)
| Control | Status | Logic |
|---------|--------|-------|
| Device Cards | FUNCTIONAL | Fetches connected nodes. |
| Battery/Signal UI | FUNCTIONAL | Renders colored indicators based on JSON payload values. |

## Settings & Demo Panel (`/settings`)
| Control | Status | Logic |
|---------|--------|-------|
| Simulate Fire Btn | FUNCTIONAL | Sends POST to `/api/sensors` with high Temp/Flame flag. |
| Simulate Flood Btn | FUNCTIONAL | Sends POST to `/api/sensors` with low distance reading. |

**ZERO DEAD UI RULE STRICTLY ENFORCED.**

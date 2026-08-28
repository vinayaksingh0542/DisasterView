# Backend Engineering (Member 2)

## Overview
This document explains the FastAPI backend.

### Key Concepts
- **FastAPI:** A modern Python web framework. It automatically generates API documentation and handles JSON serialization.
- **SQLAlchemy (ORM):** Look at `src/models/all_models.py`. Instead of writing raw SQL strings, we define Python classes (like `Incident`). SQLAlchemy translates these into SQL tables.
- **Sensor Fusion Logic:** In `src/api/routes.py` under the `/api/sensors` POST route, we receive data. We check if `flame_detected` is true OR `temperature > 60`. If yes, we automatically create a FIRE incident and broadcast it over the WebSocket.

### Possible Judge Questions for You
**Q: How does your backend handle simultaneous sensor inputs from 1000 devices?**
*Answer:* FastAPI is built on ASGI (Asynchronous Server Gateway Interface). This means it can handle thousands of concurrent connections efficiently without blocking the main thread, making it perfect for IoT workloads.

**Q: Why SQLite instead of PostgreSQL for the final deliverable?**
*Answer:* We initially architected for PostgreSQL (and the code is 100% compatible via SQLAlchemy), but to ensure a flawless, zero-dependency demo environment for the judges, we configured SQLAlchemy to use a local SQLite file so it runs instantly anywhere.

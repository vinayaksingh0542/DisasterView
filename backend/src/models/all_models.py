from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.session import Base

class Device(Base):
    __tablename__ = "devices"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    status = Column(String, default="ONLINE") # ONLINE, OFFLINE, WARNING
    last_seen = Column(DateTime, default=datetime.utcnow)
    battery_level = Column(Float, nullable=True)
    firmware_version = Column(String, default="1.0.0")
    # Calibration for HC-SR04
    hcsr04_reference_height_cm = Column(Float, default=200.0)

class SensorReading(Base):
    __tablename__ = "sensor_readings"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    device_id = Column(String, ForeignKey("devices.id"))
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    mq135_air_quality = Column(Float, nullable=True) # Raw/Relative
    mq9_gas_level = Column(Float, nullable=True)     # Raw/Relative Combustible Gas
    flame_detected = Column(Boolean, default=False)
    water_distance_cm = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(String, primary_key=True, index=True)
    type = Column(String) # FLOOD, FIRE, SMOKE
    severity = Column(String) # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String, default="UNVERIFIED") # UNVERIFIED, ACKNOWLEDGED, RESOLVED
    lat = Column(Float)
    lng = Column(Float)
    description = Column(Text, nullable=True)
    ai_confidence = Column(Float, nullable=True)
    source = Column(String) # CAMERA, SENSOR_FUSION, MULTI_SOURCE
    evidence_score = Column(String, nullable=True) # E.g., "HIGH", "CRITICAL"
    evidence_details = Column(JSON, nullable=True) # Dictionary mapping evidence sources to their values
    evidence_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

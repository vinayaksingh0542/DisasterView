import os
from ultralytics import YOLO

fire_model = YOLO("ai/models/fire_smoke.pt")
flood_model = YOLO("ai/models/flood.pt")

print("--- FIRE/SMOKE MODEL ---")
print("Classes:", fire_model.names)
print("Task:", fire_model.task)

print("--- FLOOD MODEL ---")
print("Classes:", flood_model.names)
print("Task:", flood_model.task)

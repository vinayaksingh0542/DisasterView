import cv2
import numpy as np
import os
import time
import logging

try:
    from ultralytics import YOLO
    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False
    
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

logger = logging.getLogger(__name__)

class EdgeAIInferencer:
    def __init__(self):
        if not ULTRALYTICS_AVAILABLE:
            raise RuntimeError("Ultralytics YOLO is not installed.")

        # Architecture Principle: Explicit Runtime for Qualcomm honesty
        self.runtime = "LOCAL CPU / PYTORCH"
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # We explicitly load the VERIFIED Fire model downloaded from HF
        self.fire_model_path = os.path.join(base_dir, "ai", "models", "fire.pt")
        
        self.fire_model = None
        self.flood_model = None

        if os.path.exists(self.fire_model_path):
            try:
                self.fire_model = YOLO(self.fire_model_path)
                logger.info(f"Loaded Fire/Smoke Model: {self.fire_model_path}")
            except Exception as e:
                logger.error(f"Failed to load Fire/Smoke Model: {e}")
        else:
            logger.warning(f"Fire/Smoke weights not found at {self.fire_model_path}")

        # Flood Model uses HuggingFace transformers pipeline (Image Classification)
        if TRANSFORMERS_AVAILABLE:
            try:
                # We initialize without downloading automatically in production, but HF pipeline handles caching
                self.flood_model = pipeline('image-classification', model='prithivMLmods/Flood-Image-Detection')
                logger.info(f"Loaded Flood Classifier: prithivMLmods/Flood-Image-Detection")
            except Exception as e:
                logger.error(f"Failed to load Flood Model: {e}")
                self.flood_model = None
        else:
            logger.warning(f"Transformers unavailable. Flood AI unavailable.")

    def get_model_info(self):
        registry = {}
        
        if self.fire_model:
            registry["fire_smoke"] = {
                "name": "touati-kamel/yolov8s-forest-fire",
                "version": "v1.0",
                "task": "Object Detection",
                "framework": "Ultralytics PyTorch",
                "runtime": self.runtime,
                "expected_classes": ["fire-smoke", "fog", "sol", "fire", "factory-smoke"]
            }
        else:
            registry["fire_smoke"] = {
                "name": "MISSING WEIGHTS",
                "runtime": self.runtime,
                "expected_classes": []
            }
            
        if self.flood_model:
            registry["flood"] = {
                "name": "prithivMLmods/Flood-Image-Detection",
                "version": "v1.0",
                "task": "Image Classification",
                "framework": "Transformers PyTorch",
                "runtime": self.runtime,
                "expected_classes": ["Flooded Scene", "Non Flooded"]
            }
        else:
            registry["flood"] = {
                "name": "MISSING WEIGHTS (NO FAKE AI)",
                "runtime": self.runtime,
                "expected_classes": ["NOT CONFIGURED"]
            }

        return registry

    def infer_image(self, image_bytes: bytes, target_model="fire_smoke"):
        start_time = time.time()
        detections = []
        
        if target_model == "fire_smoke" and self.fire_model:
            np_arr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            try:
                results = self.fire_model.predict(img, verbose=False)
                for r in results:
                    for box in r.boxes:
                        cls_id = int(box.cls[0])
                        conf = float(box.conf[0])
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        
                        # verified classes: {0: 'fire-smoke', 1: 'fog', 2: 'sol', 3: 'fire', 4: 'factory-smoke'}
                        if cls_id == 3:
                            class_name = "FIRE"
                        elif cls_id == 0 or cls_id == 4:
                            class_name = "SMOKE"
                        else:
                            continue # Ignore non-disaster classes
                            
                        detections.append({
                            "class": class_name,
                            "confidence": conf,
                            "bbox": [x1, y1, x2, y2],
                            "model_used": "touati-kamel/yolov8s-forest-fire",
                            "runtime": self.runtime
                        })
            except Exception as e:
                logger.error(f"Fire inference failed: {e}")

        # Flood Model
        if target_model == "flood" and self.flood_model:
            from PIL import Image
            import io
            try:
                image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                results = self.flood_model(image)
                # Pipeline returns list of dicts: [{'label': 'Flooded Scene', 'score': 0.99}, ...]
                
                # Check top result
                top_res = results[0]
                if top_res['label'] == 'Flooded Scene' and top_res['score'] > 0.5:
                    detections.append({
                        "class": "FLOOD",
                        "confidence": top_res['score'],
                        # Classifiers don't have bboxes, return full image coords roughly
                        "bbox": [0, 0, image.width, image.height], 
                        "model_used": "prithivMLmods/Flood-Image-Detection",
                        "runtime": self.runtime
                    })
            except Exception as e:
                logger.error(f"Flood inference failed: {e}")
            
        inference_time_ms = round((time.time() - start_time) * 1000, 2)
        
        return {
            "detections": detections,
            "inference_time_ms": inference_time_ms
        }

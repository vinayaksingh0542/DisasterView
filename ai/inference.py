import os
import time
import logging

logger = logging.getLogger(__name__)

class EdgeAIInferencer:
    def __init__(self):
        self.runtime = "LOCAL CPU / PYTORCH"
        self.ai_enabled = os.getenv("AI_ENABLED", "true").lower() in ("1", "true", "yes")
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.fire_model_path = os.path.join(base_dir, "ai", "models", "fire.pt")
        
        self.fire_model = None
        self.flood_model = None
        self._fire_loaded = False
        self._flood_loaded = False

    def _load_fire_model(self):
        if not self.ai_enabled:
            return None
        if not self._fire_loaded:
            self._fire_loaded = True
            try:
                from ultralytics import YOLO
                if os.path.exists(self.fire_model_path):
                    self.fire_model = YOLO(self.fire_model_path)
                    logger.info(f"Lazy-loaded Fire/Smoke Model: {self.fire_model_path}")
                else:
                    logger.warning(f"Fire/Smoke weights not found at {self.fire_model_path}")
            except Exception as e:
                logger.error(f"Failed to load Fire/Smoke Model: {e}")
                self.fire_model = None
        return self.fire_model

    def _load_flood_model(self):
        if not self.ai_enabled:
            return None
        if not self._flood_loaded:
            self._flood_loaded = True
            try:
                from transformers import pipeline
                self.flood_model = pipeline('image-classification', model='prithivMLmods/Flood-Image-Detection')
                logger.info(f"Lazy-loaded Flood Classifier: prithivMLmods/Flood-Image-Detection")
            except Exception as e:
                logger.error(f"Failed to load Flood Model: {e}")
                self.flood_model = None
        return self.flood_model

    def get_model_info(self):
        if not self.ai_enabled:
            return {
                "status": "DISABLED_IN_PRODUCTION",
                "message": "AI Computer Vision is disabled in production to conserve memory on cloud instances. Core ESP32 sensor fusion is active.",
                "fire_smoke": {
                    "name": "touati-kamel/yolov8s-forest-fire",
                    "status": "DISABLED (AI_ENABLED=false)",
                    "runtime": "DISABLED_IN_PRODUCTION",
                    "expected_classes": ["fire-smoke", "fog", "sol", "fire", "factory-smoke"]
                },
                "flood": {
                    "name": "prithivMLmods/Flood-Image-Detection",
                    "status": "DISABLED (AI_ENABLED=false)",
                    "runtime": "DISABLED_IN_PRODUCTION",
                    "expected_classes": ["Flooded Scene", "Non Flooded"]
                }
            }

        registry = {
            "status": "ENABLED",
            "fire_smoke": {
                "name": "touati-kamel/yolov8s-forest-fire",
                "version": "v1.0",
                "task": "Object Detection",
                "framework": "Ultralytics PyTorch",
                "runtime": self.runtime,
                "status": "LOADED" if self.fire_model is not None else ("CONFIGURED (LAZY_LOAD)" if os.path.exists(self.fire_model_path) else "MISSING_WEIGHTS"),
                "expected_classes": ["fire-smoke", "fog", "sol", "fire", "factory-smoke"]
            },
            "flood": {
                "name": "prithivMLmods/Flood-Image-Detection",
                "version": "v1.0",
                "task": "Image Classification",
                "framework": "Transformers PyTorch",
                "runtime": self.runtime,
                "status": "LOADED" if self.flood_model is not None else "CONFIGURED (LAZY_LOAD)",
                "expected_classes": ["Flooded Scene", "Non Flooded"]
            }
        }
        return registry

    def infer_image(self, image_bytes: bytes, target_model="fire_smoke"):
        if not self.ai_enabled:
            return {
                "error": "AI Inference is disabled in the current environment (AI_ENABLED=false). Hardware sensor fusion remains active.",
                "detections": [],
                "inference_time_ms": 0.0
            }

        start_time = time.time()
        detections = []

        if target_model == "fire_smoke":
            model = self._load_fire_model()
            if model:
                try:
                    import cv2
                    import numpy as np
                    np_arr = np.frombuffer(image_bytes, np.uint8)
                    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                    results = model.predict(img, verbose=False)
                    for r in results:
                        for box in r.boxes:
                            cls_id = int(box.cls[0])
                            conf = float(box.conf[0])
                            x1, y1, x2, y2 = box.xyxy[0].tolist()
                            
                            if cls_id == 3:
                                class_name = "FIRE"
                            elif cls_id == 0 or cls_id == 4:
                                class_name = "SMOKE"
                            else:
                                continue
                                
                            detections.append({
                                "class": class_name,
                                "confidence": conf,
                                "bbox": [x1, y1, x2, y2],
                                "model_used": "touati-kamel/yolov8s-forest-fire",
                                "runtime": self.runtime
                            })
                except Exception as e:
                    logger.error(f"Fire inference failed: {e}")
                    return {
                        "error": f"Fire inference failed: {str(e)}",
                        "detections": [],
                        "inference_time_ms": round((time.time() - start_time) * 1000, 2)
                    }
            else:
                return {
                    "error": "Fire model weights unavailable or failed to load.",
                    "detections": [],
                    "inference_time_ms": 0.0
                }

        if target_model == "flood":
            model = self._load_flood_model()
            if model:
                try:
                    from PIL import Image
                    import io
                    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                    results = model(image)
                    top_res = results[0]
                    if top_res['label'] == 'Flooded Scene' and top_res['score'] > 0.5:
                        detections.append({
                            "class": "FLOOD",
                            "confidence": top_res['score'],
                            "bbox": [0, 0, image.width, image.height],
                            "model_used": "prithivMLmods/Flood-Image-Detection",
                            "runtime": self.runtime
                        })
                except Exception as e:
                    logger.error(f"Flood inference failed: {e}")
                    return {
                        "error": f"Flood inference failed: {str(e)}",
                        "detections": [],
                        "inference_time_ms": round((time.time() - start_time) * 1000, 2)
                    }
            else:
                return {
                    "error": "Flood model unavailable or failed to load.",
                    "detections": [],
                    "inference_time_ms": 0.0
                }

        inference_time_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "detections": detections,
            "inference_time_ms": inference_time_ms
        }

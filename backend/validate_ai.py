import sys
import os
import json
import time

# Setup path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.inference import EdgeAIInferencer

inferencer = EdgeAIInferencer()

test_dirs = {
    "FIRE": "../ai/validation/validation/fire",
    "SMOKE": "../ai/validation/validation/smoke",
    "NORMAL": "../ai/validation/validation/normal"
}

results = []
metrics = {
    "total_images": 0,
    "fire_true_positives": 0,
    "fire_false_positives": 0,
    "fire_false_negatives": 0,
    "smoke_true_positives": 0,
    "smoke_false_positives": 0,
    "smoke_false_negatives": 0,
    "inference_times": []
}

# Warmup
dummy_img = b"\x00"*1000
inferencer.infer_image(dummy_img, "fire_smoke")

for expected_class, d in test_dirs.items():
    if not os.path.exists(d):
        continue
    for f in os.listdir(d):
        if not f.endswith(".jpg"): continue
        path = os.path.join(d, f)
        
        with open(path, "rb") as file:
            data = file.read()
            
        res = inferencer.infer_image(data, "fire_smoke")
        det = res.get("detections", [])
        inf_time = res.get("inference_time_ms", 0)
        
        metrics["total_images"] += 1
        metrics["inference_times"].append(inf_time)
        
        detected_fire = any(d['class'] == 'FIRE' for d in det)
        detected_smoke = any(d['class'] == 'SMOKE' for d in det)
        
        if expected_class == "FIRE":
            if detected_fire: metrics["fire_true_positives"] += 1
            else: metrics["fire_false_negatives"] += 1
            if detected_smoke: metrics["smoke_true_positives"] += 1 # Fire images often have smoke
        elif expected_class == "SMOKE":
            if detected_smoke: metrics["smoke_true_positives"] += 1
            else: metrics["smoke_false_negatives"] += 1
            if detected_fire: metrics["fire_false_positives"] += 1
        elif expected_class == "NORMAL":
            if detected_fire: metrics["fire_false_positives"] += 1
            if detected_smoke: metrics["smoke_false_positives"] += 1
            
        results.append({
            "image": f"{expected_class}/{f}",
            "expected": expected_class,
            "detected": [d['class'] for d in det],
            "time_ms": inf_time
        })

if len(metrics["inference_times"]) > 0:
    times = sorted(metrics["inference_times"])
    metrics["avg_inference_time_ms"] = sum(times) / len(times)
    metrics["median_inference_time_ms"] = times[len(times)//2]
    metrics["p95_inference_time_ms"] = times[int(len(times)*0.95)]

def safe_div(a, b): return a / b if b > 0 else 0.0

fire_tp = metrics["fire_true_positives"]
fire_fp = metrics["fire_false_positives"]
fire_fn = metrics["fire_false_negatives"]

metrics["fire_precision"] = safe_div(fire_tp, fire_tp + fire_fp)
metrics["fire_recall"] = safe_div(fire_tp, fire_tp + fire_fn)

smoke_tp = metrics["smoke_true_positives"]
smoke_fp = metrics["smoke_false_positives"]
smoke_fn = metrics["smoke_false_negatives"]

metrics["smoke_precision"] = safe_div(smoke_tp, smoke_tp + smoke_fp)
metrics["smoke_recall"] = safe_div(smoke_tp, smoke_tp + smoke_fn)

with open("../docs/AI_VALIDATION_RAW.json", "w") as f:
    json.dump({"metrics": metrics, "results": results}, f, indent=2)

print(json.dumps(metrics, indent=2))

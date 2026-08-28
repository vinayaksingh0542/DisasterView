import sys
import os
import json

# Setup path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.inference import EdgeAIInferencer

inferencer = EdgeAIInferencer()

test_dirs = {
    "FLOOD": "../ai/validation/validation/flood",
    "NORMAL": "../ai/validation/validation/normal"
}

results = []
metrics = {
    "total_images": 0,
    "flood_true_positives": 0,
    "flood_false_positives": 0,
    "flood_false_negatives": 0,
    "inference_times": []
}

# Warmup
dummy_img = b"\x00"*1000
try:
    inferencer.infer_image(dummy_img, "flood")
except: pass

for expected_class, d in test_dirs.items():
    if not os.path.exists(d):
        continue
    for f in os.listdir(d):
        if not f.endswith(".jpg"): continue
        path = os.path.join(d, f)
        
        with open(path, "rb") as file:
            data = file.read()
            
        res = inferencer.infer_image(data, "flood")
        det = res.get("detections", [])
        inf_time = res.get("inference_time_ms", 0)
        
        metrics["total_images"] += 1
        metrics["inference_times"].append(inf_time)
        
        detected_flood = any(d['class'] == 'FLOOD' for d in det)
        
        if expected_class == "FLOOD":
            if detected_flood: metrics["flood_true_positives"] += 1
            else: metrics["flood_false_negatives"] += 1
        elif expected_class == "NORMAL":
            if detected_flood: metrics["flood_false_positives"] += 1
            
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

flood_tp = metrics["flood_true_positives"]
flood_fp = metrics["flood_false_positives"]
flood_fn = metrics["flood_false_negatives"]

metrics["flood_precision"] = safe_div(flood_tp, flood_tp + flood_fp)
metrics["flood_recall"] = safe_div(flood_tp, flood_tp + flood_fn)

with open("../docs/FLOOD_VALIDATION_RAW.json", "w") as f:
    json.dump({"metrics": metrics, "results": results}, f, indent=2)

print(json.dumps(metrics, indent=2))

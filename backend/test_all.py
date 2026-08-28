import sys
import os
import json

# Setup path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.inference import EdgeAIInferencer

inferencer = EdgeAIInferencer()

test_images = {
    "FIRE_TEST": "../ai/test_images/fire.jpg",
    "SMOKE_TEST": "../ai/test_images/smoke.jpg",
    "NORMAL_TEST": "../ai/test_images/normal.jpg"
}

results = {}

for name, path in test_images.items():
    if not os.path.exists(path):
        print(f"MISSING {path}")
        continue
    with open(path, 'rb') as f:
        data = f.read()
    res = inferencer.infer_image(data, "fire_smoke")
    results[name] = res

print(json.dumps(results, indent=2))

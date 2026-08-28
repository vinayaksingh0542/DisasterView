import urllib.request
import cv2
import numpy as np
import sys
import os
import json

def download(url, filename):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        arr = np.asarray(bytearray(resp.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
        cv2.imwrite(filename, img)

# Download an obvious fire image
download("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Forest_Fire_in_the_San_Gabriel_Mountains.jpg/320px-Forest_Fire_in_the_San_Gabriel_Mountains.jpg", "ai/test_images/obvious_fire.jpg")

# Test it
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai.inference import EdgeAIInferencer
inferencer = EdgeAIInferencer()

with open("ai/test_images/obvious_fire.jpg", "rb") as f:
    data = f.read()
    
res = inferencer.infer_image(data, "fire_smoke")
print(json.dumps(res, indent=2))

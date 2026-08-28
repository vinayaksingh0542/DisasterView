import os
import sys

# Setup path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datasets import load_dataset
from PIL import Image

def download_data():
    print("Loading dataset...")
    # This dataset has images of fire, smoke, and normal
    ds = load_dataset('marmal88/fire_smoke_detection_1', split='train', streaming=True)
    
    os.makedirs('ai/validation/fire', exist_ok=True)
    os.makedirs('ai/validation/smoke', exist_ok=True)
    os.makedirs('ai/validation/normal', exist_ok=True)
    
    counts = {'fire': 0, 'smoke': 0, 'normal': 0}
    
    for item in ds:
        # We need 10 of each
        if all(c >= 10 for c in counts.values()):
            break
            
        img = item['image']
        # item['label'] needs mapping, assuming 0=normal, 1=fire, 2=smoke?
        # Let's inspect the first item
        print(item)
        break

if __name__ == "__main__":
    download_data()

import os
import time
import json
from duckduckgo_search import DDGS
import urllib.request

def download_images(query, folder, count=10):
    os.makedirs(folder, exist_ok=True)
    with DDGS() as ddgs:
        results = list(ddgs.images(query, max_results=count*2))
        
    downloaded = 0
    for res in results:
        if downloaded >= count:
            break
        url = res['image']
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                with open(os.path.join(folder, f"{downloaded}.jpg"), 'wb') as f:
                    f.write(resp.read())
            downloaded += 1
            print(f"Downloaded {folder}/{downloaded-1}.jpg")
        except Exception as e:
            continue

download_images("forest fire", "ai/validation/fire", 10)
download_images("wildfire smoke", "ai/validation/smoke", 10)
download_images("city street sunny day", "ai/validation/normal", 10)
download_images("severe flood street", "ai/validation/flood", 10)

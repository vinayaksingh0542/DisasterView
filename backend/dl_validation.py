import urllib.request
import json
import os
import cv2
import numpy as np

def get_images(query, n=20):
    query = urllib.parse.quote(query)
    url = f'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&generator=search&gsrsearch={query}&pithumbsize=640&gsrlimit={n}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    urls = []
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            pages = data.get('query', {}).get('pages', {})
            for p in pages.values():
                if 'thumbnail' in p:
                    urls.append(p['thumbnail']['source'])
    except Exception as e:
        print(e)
    return urls

def download(urls, folder, target_count=10):
    os.makedirs(folder, exist_ok=True)
    count = 0
    for i, u in enumerate(urls):
        if count >= target_count:
            break
        try:
            req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                arr = np.asarray(bytearray(resp.read()), dtype=np.uint8)
                img = cv2.imdecode(arr, -1)
                # Save as jpg
                cv2.imwrite(os.path.join(folder, f"{count}.jpg"), img)
                count += 1
        except:
            continue

print("Downloading fire...")
fire_urls = get_images('wildfire', 25)
download(fire_urls, 'ai/validation/fire')

print("Downloading smoke...")
smoke_urls = get_images('smoke plume', 25)
download(smoke_urls, 'ai/validation/smoke')

print("Downloading normal...")
normal_urls = get_images('city street sunny', 25)
download(normal_urls, 'ai/validation/normal')

print("Downloading flood...")
flood_urls = get_images('flood street', 25)
download(flood_urls, 'ai/validation/flood')

print("Done")

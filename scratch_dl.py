import urllib.request
import re
import cv2
import numpy as np

def download(url, filename):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        arr = np.asarray(bytearray(resp.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
        cv2.imwrite(filename, img)

req = urllib.request.Request('https://en.wikipedia.org/wiki/Wildfire', headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')
imgs = re.findall(r'src=\"(//upload\.wikimedia\.org/wikipedia/commons/thumb/[^\"]+\.jpg/[^\"]+)\"', html)

print(imgs[0])
download("https:" + imgs[0], "ai/test_images/fire.jpg")

req2 = urllib.request.Request('https://en.wikipedia.org/wiki/Smoke', headers={'User-Agent': 'Mozilla/5.0'})
html2 = urllib.request.urlopen(req2).read().decode('utf-8')
imgs2 = re.findall(r'src=\"(//upload\.wikimedia\.org/wikipedia/commons/thumb/[^\"]+\.jpg/[^\"]+)\"', html2)
print(imgs2[0])
download("https:" + imgs2[0], "ai/test_images/smoke.jpg")

print("Done")

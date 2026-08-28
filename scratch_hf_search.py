import requests
def search_hf(query):
    url = f'https://huggingface.co/api/models?search={query}&limit=20'
    res = requests.get(url).json()
    for r in res:
        files_url = f"https://huggingface.co/api/models/{r['id']}/tree/main"
        try:
            files = requests.get(files_url).json()
            for f in files:
                if isinstance(f, dict) and f.get('path', '').endswith('.pt'):
                    print(f"Model: {r['id']} - Download: https://huggingface.co/{r['id']}/resolve/main/{f['path']}")
        except: pass

search_hf('yolov8 flood')
search_hf('flood detect')

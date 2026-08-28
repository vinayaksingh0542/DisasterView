from ultralytics import YOLO

def download_models():
    print("Downloading YOLOv8n...")
    model = YOLO("yolov8n.pt") 
    print("Model downloaded successfully!")

if __name__ == "__main__":
    download_models()

from ai.inference import EdgeAIInferencer
import os
import json

inferencer = EdgeAIInferencer()

test_images = {
    "FIRE_TEST": "ai/test_images/fire.jpg",
    "SMOKE_TEST": "ai/test_images/fire.jpg", # Fire images often have smoke too
    "FLOOD_TEST": "ai/test_images/fire.jpg", # Should be negative for flood
    "NORMAL_TEST": "ai/test_images/normal.jpg" # bus.jpg (has no fire)
}

print("=======================================")
print("          AI INFERENCE TEST            ")
print("=======================================")

for test_name, img_path in test_images.items():
    print(f"\n--- {test_name} ---")
    if not os.path.exists(img_path):
        print(f"Error: {img_path} not found.")
        continue
        
    with open(img_path, "rb") as f:
        bytes_data = f.read()
        
    # Test Fire Model
    res_fire = inferencer.infer_image(bytes_data, "fire_smoke")
    print(f"Fire Model Result: {json.dumps(res_fire, indent=2)}")
    
    # Test Flood Model
    res_flood = inferencer.infer_image(bytes_data, "flood")
    print(f"Flood Model Result: {json.dumps(res_flood, indent=2)}")

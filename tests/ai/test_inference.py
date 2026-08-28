import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from ai.inference import EdgeAIInferencer

def run_tests():
    print("--- STARTING AI PIPELINE TESTS ---")
    try:
        inferencer = EdgeAIInferencer()
        registry = inferencer.get_model_info()
        print(f"ACTIVE MODEL: {registry['fire_smoke']['name']}")
        print(f"EXPECTED CLASSES: {registry['fire_smoke']['expected_classes']}")
        print("PIPELINE IS READY TO ACCEPT IMAGES.")
    except Exception as e:
        print(f"AI PIPELINE FAILED TO INITIALIZE: {e}")

if __name__ == "__main__":
    run_tests()

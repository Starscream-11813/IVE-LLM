import json
from config import MODELS
from models import ReplicateModel

client = ReplicateModel()
successes = 0

print("Testing 1 sample for all 16 active models...\n")

for model_key in MODELS:
    print(f"Testing {model_key}...")
    try:
        res = client.generate(
            model_key=model_key,
            prompt="Respond only with the word ACKNOWLEDGEMENT.",
            system_prompt="You are a test script.",
            temperature=0.7
        )
        assert "error" not in res.get("response_text", "").lower()
        print(f"  - Success! Response: {res['response_text'][:50]}")
        successes += 1
    except Exception as e:
        print(f"  - ERROR: {e}")

print(f"\nCompleted: {successes}/{len(MODELS)} succeeded.")

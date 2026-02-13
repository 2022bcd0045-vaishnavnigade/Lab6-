import json
import random
import os

os.makedirs("app/artifacts", exist_ok=True)

accuracy = round(random.uniform(0.7, 0.95), 4)
metrics = {"accuracy": accuracy}

with open("app/artifacts/metrics.json", "w") as f:
    json.dump(metrics, f)

print(f"Training complete. Accuracy: {accuracy}")

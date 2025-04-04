
import requests
import base64
from PIL import Image
from io import BytesIO

# The container is mapped to localhost:8000
ENDPOINT_URL = "http://127.0.0.1:8000/inference"

# Example payload -- adapt to what your server expects
payload = {
    "input": {
        "prompt": "A cat holding a sign that says hello world",
        "height": 512,
        "width": 512,
        "guidance_scale": 3.5,
        "steps": 20
    }
}

response = requests.post(ENDPOINT_URL, json=payload)
response.raise_for_status()

# Suppose the server returns {"image_base64": "..."}
data = response.json()

image_base64 = data["image_base64"]
image_data = base64.b64decode(image_base64)
image = Image.open(BytesIO(image_data))

# Save the image to disk
image.save("generated.png")
print("Saved generated.png")
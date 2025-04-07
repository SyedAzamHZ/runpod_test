#!/usr/bin/env python
"""
Simple script to test the RunPod endpoint using test_input.json
"""

import os
import json
import base64
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
from dotenv import load_dotenv

# Setup
load_dotenv()
RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")
if not RUNPOD_API_KEY:
    print("Error: RUNPOD_API_KEY not found in .env file")
    exit(1)

# Create output dir
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
os.makedirs(output_dir, exist_ok=True)

# Load test input
test_input_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_input.json')
with open(test_input_path, 'r') as f:
    test_data = json.load(f)

# API setup
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {RUNPOD_API_KEY}"
}
ENDPOINT_URL = "https://api.runpod.ai/v2/dhufwq1i38vi4p/runsync"

print(f"Testing with prompt: '{test_data['input']['prompt']}'")

try:
    # Make request
    response = requests.post(ENDPOINT_URL, json=test_data, headers=headers)
    response.raise_for_status()
    data = response.json()
    
    # Process image
    image_base64 = data["output"]["image_base64"]
    image_data = base64.b64decode(image_base64)
    image = Image.open(BytesIO(image_data))
    
    # Save image
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prompt = test_data['input']['prompt'][:20].replace(" ", "_")
    filename = f"{timestamp}_{prompt}.png"
    output_path = os.path.join(output_dir, filename)
    image.save(output_path)
    
    print(f"Success! Image saved to: {output_path}")
    
except Exception as e:
    print(f"Error: {str(e)}") 
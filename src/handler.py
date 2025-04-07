import base64
import io
import os

import torch
from diffusers import FluxPipeline
import runpod.serverless
from dotenv import load_dotenv
# load env variables
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
print("Loading FLUX.1 [dev] Pipeline...")
pipeline = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev"
)
pipeline.enable_model_cpu_offload()
print("Pipeline loaded successfully.")

def handler(event):
    """
    Receives an event with 'input' dict, then uses pipeline to generate an image.
    Returns base64-encoded PNG bytes in its response.
    """
    job_input = event.get("input", {})

    prompt = job_input.get("prompt", "A scenic landscape with mountains")
    height = job_input.get("height", 512)
    width = job_input.get("width", 512)
    guidance_scale = job_input.get("guidance_scale", 3.5)
    steps = job_input.get("steps", 50)
    
    with torch.inference_mode():
        image = pipeline(
            prompt,
            height=height,
            width=width,
            guidance_scale=guidance_scale,
            num_inference_steps=steps,
        ).images[0]

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return {
        "prompt": prompt,
        "height": height,
        "width": width,
        "guidance_scale": guidance_scale,
        "steps": steps,
        "image_base64": image_b64
    }

if __name__ == "__main__":
    print("Starting RunPod Serverless...")
    runpod.serverless.start({"handler": handler})

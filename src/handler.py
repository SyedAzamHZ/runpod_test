import base64
import io

import torch
from diffusers import FluxPipeline
import runpod.serverless

# ------------------------------------------------------------------------------
# 1) Load or initialize your pre-downloaded model here (FLUX.1 [dev]) as a global
#    so that it is only loaded once per container.
# ------------------------------------------------------------------------------

# Adjust for offloading or GPU usage based on memory availability:
# For demonstration, we enable model CPU offload. If you have enough GPU memory
# you can remove `.enable_model_cpu_offload()` and rely purely on GPU usage.
print("Loading FLUX.1 [dev] Pipeline...")
pipeline = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.bfloat16,
    cache_dir="/weights"      # Where we cached the model in our Docker build
)
pipeline.enable_model_cpu_offload()
print("Pipeline loaded successfully.")

# ------------------------------------------------------------------------------
# 2) Handler function for RunPod. 
#    The `event` dict is expected to have a structure like:
#    {
#      "input": {
#         "prompt": "A cat holding a sign that says hello world",
#         "height": 1024,
#         "width": 1024,
#         "guidance_scale": 3.5,
#         "steps": 50
#      }
#    }
# ------------------------------------------------------------------------------

def handler(event):
    """
    Receives an event with 'input' dict, then uses pipeline to generate an image.
    Returns base64-encoded PNG bytes in its response.
    """
    # Extract job input
    job_input = event.get("input", {})

    prompt = job_input.get("prompt", "A scenic landscape with mountains")
    height = job_input.get("height", 512)
    width = job_input.get("width", 512)
    guidance_scale = job_input.get("guidance_scale", 3.5)
    steps = job_input.get("steps", 50)
    
    # Generate the image
    with torch.inference_mode():
        image = pipeline(
            prompt,
            height=height,
            width=width,
            guidance_scale=guidance_scale,
            num_inference_steps=steps,
        ).images[0]

    # Encode image to base64 so we can send it back in JSON
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

# ------------------------------------------------------------------------------
# 3) Start RunPod Serverless
#    This allows local testing via `python handler.py` as well as serverless usage.
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})

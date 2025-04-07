FROM python:3.11.1-buster

# Build args
ARG HF_TOKEN
ARG HF_HUB_DOWNLOAD_TIMEOUT=600

# Set environment variables
ENV HUGGINGFACE_TOKEN=$HF_TOKEN
ENV HF_HUB_DOWNLOAD_TIMEOUT=$HF_HUB_DOWNLOAD_TIMEOUT

WORKDIR /app

COPY builder/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Attempt to log in:
RUN huggingface-cli login --token $HF_TOKEN --add-to-git-credentials || echo "HF login may succeed or fail."

# Pre-fetch the model with an increased timeout
RUN python -c "import torch; from diffusers import FluxPipeline; \
    FluxPipeline.from_pretrained('black-forest-labs/FLUX.1-dev', \
    torch_dtype=torch.bfloat16, cache_dir='/weights')"

COPY src/handler.py /app/handler.py

CMD ["python", "-u", "/app/handler.py"]

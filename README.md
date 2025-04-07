# FLUX.1 RunPod Serverless Endpoint

This project implements a serverless endpoint for the FLUX.1 image generation model using RunPod. It provides an API endpoint that can generate images from text prompts using the FLUX.1 model from Black Forest Labs.

## Project Overview

The project sets up a Docker container that runs a RunPod serverless endpoint for the FLUX.1 image generation model. The endpoint accepts text prompts and other parameters to generate images, returning them as base64-encoded PNG data.

## System Requirements

⚠️ **Important Note on Model Size**: 
- The FLUX.1 model requires approximately 70GB of memory for optimal performance
- Due to these substantial memory requirements, the model is not suitable for local deployment on most machines
- RunPod's cloud infrastructure is used to provide the necessary computational resources
- Recommended RunPod endpoint configuration: 
  - Minimum 80GB RAM
  - GPU with at least 24GB VRAM
  - T4, RTX 3090, A5000, or better GPU recommended

## Project Structure

```
.
├── README.md               # Project documentation
├── Dockerfile             # Container configuration
├── .env                   # Environment variables (git-ignored)
├── .env.example           # Example environment variables
├── requirements.txt       # Project dependencies
├── builder/
│   └── requirements.txt   # Docker build-time dependencies
├── src/
│   └── handler.py        # Main RunPod endpoint handler
├── tests/
│   ├── test_input.json   # Sample test inputs
│   └── run_test.py       # Script to test endpoint using test_input.json
├── output/                # Directory for storing generated images
└── notebooks/
    └── inference.ipynb   # Development and testing notebook
```

### Directory Structure Explanation

- `builder/`: Contains build-time requirements and configurations
- `src/`: Contains the main application code
  - `handler.py`: Implements the RunPod serverless handler
- `tests/`: Contains test files and sample inputs
  - `run_test.py`: Script for testing the endpoint with test_input.json
- `notebooks/`: Contains Jupyter notebooks for development and testing
- `output/`: Directory where generated images are saved

## Architecture Diagram

```
                     Build & Push                      Deploy
┌──────────────┐     ┌─────────────┐     ┌───────────────────┐     ┌─────────────────┐
│              │     │             │     │                   │     │    RunPod       │
│  Local Dev   ├────►│  Dockerfile ├────►│    Docker Hub     ├────►│    Endpoint     │
│              │     │             │     │                   │     │                 │
└──────────────┘     └─────────────┘     └───────────────────┘     │  ┌───────────┐ │
                                                                    │  │  FLUX.1   │ │
                                         ┌─────────────────────────►│  │  Model    │ │
                                         │                          │  └───────────┘ │
                                         │                          └───────┬────────┘
                                         │                                  │
                              ┌─────────────────────┐                      │
                              │   Client Request    │                      │
                              │   (Text Prompt)     │                      │
                              └─────────────────────┘                      │
                                                                          │
                                                                          ▼
                              ┌─────────────────────┐             ┌───────────────┐
                              │   Client Receives   │◄────────────┤  Generated    │
                              │   Base64 Image      │             │  Image        │
                              └─────────────────────┘             └───────────────┘

Flow:
1. Development: Local environment with code and Dockerfile
2. Build & Push: Docker image is built and pushed to Docker Hub
3. Deploy: RunPod pulls image from Docker Hub and creates serverless endpoint with FLUX.1 model
4. Usage: Client sends text prompt to RunPod endpoint
5. Processing: Endpoint uses FLUX.1 model to generate image
6. Response: Generated image is encoded to base64 and returned to client
```

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd runpod-flux
```

2. Create and configure environment variables:
```bash
cp .env.example .env
# Edit .env with your HuggingFace token
```

3. Install dependencies for development:
```bash
pip install -r requirements.txt
```

4. Build the Docker image:
```bash
docker build --build-arg HF_TOKEN=${HF_TOKEN} -t your-dockerhub-username/flux-runpod:latest .
```

5. Push to Docker Hub:
```bash
docker push your-dockerhub-username/flux-runpod:latest
```

## RunPod Deployment

1. Log in to your RunPod account
2. Create a new Serverless Endpoint
3. Select your Docker image
4. Configure endpoint settings:
   - Set minimum memory to 80GB
   - Select appropriate GPU (T4, RTX 3090, A5000, or better)
   - Set desired scaling options

## Testing the Endpoint

### Using the Test Script

To test the endpoint using the provided test_input.json file:

1. Make sure your .env file contains the RUNPOD_API_KEY:
```
RUNPOD_API_KEY=your_runpod_api_key_here
```

2. Update the endpoint URL in the test script:
```python
# Open tests/run_test.py and update this line:
ENDPOINT_URL = "https://api.runpod.ai/v2/your-endpoint-id/runsync"
```

3. Run the test script:
```bash
python tests/run_test.py
```

The script will:
- Load the test input from tests/test_input.json
- Send it to your RunPod endpoint
- Save the generated image to the output directory

### Using the Jupyter Notebook

For interactive testing, you can use the Jupyter notebook:

```bash
jupyter notebook notebooks/inference.ipynb
```

## API Usage

### Request Format

```json
{
    "input": {
        "prompt": "A scenic landscape with mountains",
        "height": 512,
        "width": 512,
        "guidance_scale": 3.5,
        "steps": 50
    }
}
```

### Parameters

- `prompt` (string): The text description of the image to generate
- `height` (int): Image height in pixels (default: 512)
- `width` (int): Image width in pixels (default: 512)
- `guidance_scale` (float): Controls how closely the model follows the prompt (default: 3.5)
- `steps` (int): Number of denoising steps (default: 50)

### Response Format

```json
{
    "prompt": "A scenic landscape with mountains",
    "height": 512,
    "width": 512,
    "guidance_scale": 3.5,
    "steps": 50,
    "image_base64": "base64_encoded_image_data"
}
```

## Error Handling

The endpoint includes error handling for:
- Invalid input parameters
- Model loading issues
- Memory constraints

## License

Please refer to the FLUX.1 model license for usage terms and conditions.


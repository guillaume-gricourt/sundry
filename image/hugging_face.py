import io
import requests
import sys
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
headers = {"Authorization": f"Bearer " + os.environ.get("HUGGING_FACE")}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content


image_bytes = query({"inputs": "a flower in a pot"})

image = Image.open(io.BytesIO(image_bytes))

image.save(sys.argv[1], "jpeg")

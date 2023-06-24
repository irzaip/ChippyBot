import json
import requests
from PIL import Image
import io
import re
from time import time
import trans_id as tr


def buat_gambar(prompt: str):
    API_TOKEN = "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"  # token in case you want to use private API
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "X-Wait-For-Model": "true",
        "X-Use-Cache": "false"
    }
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"


    def query(payload):
        data = json.dumps(payload)
        response = requests.request("POST", API_URL, headers=headers, data=data)

        return Image.open(io.BytesIO(response.content))


    def slugify(text):
        # remove non-word characters and foreign characters
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub(r"\s+", "-", text)
        return text


    prompt = tr.input_modifier(prompt)
    image = query({"inputs": prompt})
    #image.save(f"{slugify(prompt)}-{time():.0f}.png")
    return image
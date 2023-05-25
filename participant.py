import json
import requests

response = requests.get(f'http://127.0.0.1:8000/participant')

aa = json.loads(response.text)
aa['message']
import requests

url = 'http://127.0.0.1:8000/test'

data = {'kalimat': 'saya sudah siap menerima perintah', 'speaker': 'gadis', 'playaudio': 'true', 'requestaudio': 'true'}
params = {'kalimat': 'saya sudah siap menerima perintah', 'format': 'xml', 'platformId': 1}
headers={'Content-Type': 'application/json'}
response = requests.post(url, json=data, headers=headers)
print(response.text)
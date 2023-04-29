## send to api whatsapp-web.js open port

import requests

url = "http://127.0.0.1:5000/api/v1/generate" # Replace with your endpoint URL
message = {
    "system": "you are a friendly assistant, only reply chat with YES or NO.",
    "prompt": "What is your name, sister?", # Replace with your message text
    "from": "6285775300227@c.us", # Replace with the sender number
    "to": "62895352277562@c.us" # Replace with the recipient number in WhatsApp format
}

response = requests.post(url, json=message)

if response.status_code == 200:
    print("Message sent successfully!")
    print(response.text)
else:
    print(f"Error sending message. Status code: {response.status_code}")
    print(response.text)
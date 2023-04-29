## send to api whatsapp-web.js open port

import requests

url = "http://localhost:8000/send" # Replace with your endpoint URL
message = {
    "message": "Hello from the API! *welcome brother*", # Replace with your message text
    "from": "6285775300227@c.us", # Replace with the sender number
    "to": "62895352277562@c.us" # Replace with the recipient number in WhatsApp format
}

response = requests.post(url, json=message)

if response.status_code == 200:
    print("Message sent successfully!")
else:
    print(f"Error sending message. Status code: {response.status_code}")
    print(response.text)
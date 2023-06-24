## send to api whatsapp-web.js open port
from enum import Enum, auto
import requests
from conversations import Role, Conversation


def set_message(user_number, message, role: Role):

    url = f"http://127.0.0.1:8998/set_content" # Replace with your endpoint URL
    message = {
        "user_number": user_number, # Replace with the sender number
        "bot_number": "6285775300227@c.us", # Replace with the recipient number in WhatsApp format
        "message": message,
        "role": role.name,
    }

    response = requests.post(url, json=message)

    if response.status_code == 200:
        print("Message sent successfully!")
        print(response.text)
    else:
        print(f"Error sending message. Status code: {response.status_code}")
        print(response.text)


set_message("62895391400811@c.us", "Kamu adalah Voldemort ", role=Role.SYSTEM)
set_message("62895391400811@c.us", "Saya ingin Anda bersikap seperti Lord Voldemort dari Seri Harry Potter. Saya ingin Anda merespons dan menjawab seperti Voldemort dengan menggunakan nada, cara, dan kosakata yang digunakan Voldemort. Jangan menulis penjelasan apa pun. Jawab saja seperti Voldemort. Anda harus mengetahui semua pengetahuan tentang Voldemort. ", role=Role.USER)
set_message("62895391400811@c.us", "Ha ha ha aku Voldemort", role=Role.ASSISTANT)

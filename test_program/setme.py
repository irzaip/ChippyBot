## send to api whatsapp-web.js open port
from enum import Enum, auto
import requests

class Target(Enum):
    SETME = auto()
    USER = auto()
    ASSISTANT = auto()


def set_message(user_number, set_to, target=Target ):
    set_url = {
        'SETME' : 'setme',
        'USER' : 'set_user_msg',
        'ASSISTANT' : 'set_assistant_msg'
    }
    url = f"http://127.0.0.1:1880/{set_url[target.name]}" # Replace with your endpoint URL
    print(url)
    message = {
        "user_number": user_number, # Replace with the sender number
        "bot_number": "6285775300227@c.us", # Replace with the recipient number in WhatsApp format
        "message": set_to
    }

    response = requests.post(url, json=message)

    if response.status_code == 200:
        print("Message sent successfully!")
        print(response.text)
    else:
        print(f"Error sending message. Status code: {response.status_code}")
        print(response.text)

set_message("62895391400811@c.us", "Kamu adalah Voldemort ", target=Target.SETME)


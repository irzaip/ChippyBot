from conversations import Conversation, Message, Persona
from colorama import Fore, Style, Back
import toml
import random

cfg = toml.load('config.toml')

def run(conv_obj: Conversation, msg_text: str):
    conv_obj.kurangi_funny_counter()
    print(f'{Fore.LIGHTYELLOW_EX}sekarang funny counter {conv_obj.user_name} adalah: {conv_obj.funny_counter}{Fore.RESET}')

    if conv_obj.funny_counter == 0:
        print(f'{Fore.LIGHTYELLOW_EX}sekarang funny counter {conv_obj.user_name} adalah: {conv_obj.funny_counter}{Fore.RESET}')
        return random.choice(cfg['IKLAN']['PESAN'])
    else:
        return ""

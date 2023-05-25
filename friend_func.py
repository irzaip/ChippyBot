from conversations import Conversation, Message, Persona
from colorama import Fore, Style, Back
import toml
import random

cfg = toml.load('config.toml')

def run(conv_obj: Conversation, msg_text: str):
    print(f"{Fore.CYAN}FRIEND sisa messages: {conv_obj.free_tries}{Fore.RESET}")
    conv_obj.

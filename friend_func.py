from conversations import Conversation, Message, Persona
from colorama import Fore, Style, Back
import toml
import counting as ct
import apicall as api
import datetime
import asyncio


cfg = toml.load('config.toml')

async def run(self, conv_obj: Conversation, message: Message):
    msg_text = message.text

    #buat vold, gak perlu memory
    if conv_obj.persona == Persona.VOLD:
        memory = False
    else:
        memory = True


    if conv_obj.free_gpt:
        result = await api.ask_gpt(self, conv_obj, msg_text, memory=memory)
        #result = cobj.run(self.conv_obj, message)
        result = f"{result}\n\n\U0001F48E".strip()
        return result 

    if conv_obj.paid_messages:
        ct.kurangi_paid_messages(conv_obj)
        result = await api.ask_gpt(self, conv_obj, msg_text, memory=memory)
        #result = cobj.run(self.conv_obj, message)
        result = f"{result}\n\n*[{conv_obj.paid_messages}]*".strip()
        return result 
    else:
        return "friend only."
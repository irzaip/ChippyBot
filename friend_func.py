from conversations import Conversation, Message, Persona
from colorama import Fore, Style, Back
import toml
import counting as ct
import apicall as api
import datetime
from db_oper import insert_conv
import asyncio


cfg = toml.load('config.toml')

async def run(self, conv_obj: Conversation, message: Message):
    msg_text = message.text

    if conv_obj.free_gpt:
        result = await api.ask_gpt(self, conv_obj, msg_text)
        #result = cobj.run(self.conv_obj, message)
        insert_conv(conv_obj.user_number,
                    conv_obj.bot_number,
                    int(datetime.datetime.utcnow().timestamp()), 
                    result, cfg['CONFIG']['DB_FILE'])
        result = f"{result}\n\n\U0001F48E".strip()
        return result 

    if conv_obj.paid_messages:
        ct.kurangi_paid_messages(conv_obj)
        result = await api.ask_gpt(self, conv_obj, msg_text)
        #result = cobj.run(self.conv_obj, message)
        insert_conv(conv_obj.user_number,
                    conv_obj.bot_number,
                    int(datetime.datetime.utcnow().timestamp()), 
                    result, cfg['CONFIG']['DB_FILE'])
        result = f"{result}\n\n*[{conv_obj.paid_messages}]*".strip()
        return result 
    else:
        return "friend only."
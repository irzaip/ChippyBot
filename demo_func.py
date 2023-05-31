from conversations import Conversation, ConvMode, Message
from colorama import Fore, Style, Back
import toml
import random
import counting as ct
import apicall as api
import datetime
from db_oper import insert_conv
import asyncio
import interview as iv

cfg = toml.load('config.toml')

async def run(self, conv_obj: Conversation, message: Message):
    msg_text = message.text



    print(f'{Fore.LIGHTYELLOW_EX}sekarang free tries {conv_obj.user_name} adalah: {conv_obj.free_tries}{Fore.RESET}')
    print(f'{Fore.LIGHTYELLOW_EX}sekarang funny counter {conv_obj.user_name} adalah: {conv_obj.funny_counter}{Fore.RESET}')

    if conv_obj.convmode == ConvMode.INTERVIEW:
        return iv.get_answer(conv_obj, message)

    if conv_obj.free_tries:
        ct.kurangi_free_tries(conv_obj)
        result = await api.ask_gpt(self, conv_obj, msg_text)
        insert_conv(conv_obj.user_number,
                    conv_obj.bot_number,
                    int(datetime.datetime.utcnow().timestamp()), 
                    result, cfg['CONFIG']['DB_FILE'])
        result = f"{result}\n\n*[{conv_obj.free_tries}]*\u2713".strip()
        return result 

    rivereply = conv_obj.rivebot.reply("Irza Pulungan", message.text)
    if "<ERROR>" not in rivereply:
        print(f"{Fore.GREEN}{Back.LIGHTMAGENTA_EX}dia mengatakan : {message.text}{Style.RESET_ALL}")
        print(f"{Fore.RED}{Back.WHITE}saya menjawab: {rivereply}{Style.RESET_ALL}")
        await asyncio.sleep(10)
        ct.kurangi_funny_counter(conv_obj)
        return rivereply


    if conv_obj.funny_counter:
        ct.kurangi_funny_counter(conv_obj)
        promo = random.choice(cfg['IKLAN']['PESAN'])
        result = await api.ask_ooba(self, conv_obj, msg_text)
        insert_conv(conv_obj.user_number,
                    conv_obj.bot_number,
                    int(datetime.datetime.utcnow().timestamp()), 
                    result, cfg['CONFIG']['DB_FILE'])
        return f'{result}\n{promo}'

    else:
        ct.kurangi_funny_counter(conv_obj)
        promo = random.choice(cfg['IKLAN']['TRAKTIR'])
        return f'{promo}'

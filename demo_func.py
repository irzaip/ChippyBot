from conversations import Conversation, ConvMode, Message, Persona
from colorama import Fore, Style, Back
import toml
import random
import counting as ct
import apicall as api
import datetime
from db_oper import insert_conv
import asyncio
import interview as iv
import agent1 as ag1

cfg = toml.load('config.toml')

def is_group(phone_number: str) -> bool:
    if phone_number.endswith('@g.us'):
        return True
    else:
        return False
    
def real_sender_(message: Message):
    if is_group(message.user_number):
        return message.author
    else:
        return message.user_number
    

async def run(self, conv_obj: Conversation, message: Message):
    def remove_flood():
        if message.author in conv_obj.anti_flood:
            while message.author in conv_obj.anti_flood:
                conv_obj.anti_flood.remove(message.author) 
        if message.user_number in conv_obj.anti_flood:
            while message.user_number in conv_obj.anti_flood:
                conv_obj.anti_flood.remove(message.user_number) 

    msg_text = message.text

    #check flood
    real_sender = real_sender_(message)
    if real_sender in conv_obj.anti_flood:
        return "Tunggu yaa gaaess, lagi mencoba menjawab temanmu. sabar donk. budayakan antri."
    else:
        conv_obj.anti_flood.append(real_sender)

    print(f'{Fore.LIGHTYELLOW_EX}sekarang free tries {conv_obj.user_name} adalah: {conv_obj.free_tries}{Fore.RESET}')
    print(f'{Fore.LIGHTYELLOW_EX}sekarang funny counter {conv_obj.user_name} adalah: {conv_obj.funny_counter}{Fore.RESET}')
    print(f'{Fore.GREEN}sekarang promo counter {conv_obj.user_name} adalah: {conv_obj.promo_counter}{Fore.RESET}')

    promo = random.choice(cfg['IKLAN']['PROMO'])

    #buat vold, gak perlu memory
    if conv_obj.persona == Persona.VOLD:
        memory = False
    else:
        memory = True

    if conv_obj.convmode == ConvMode.INTERVIEW:
        remove_flood()
        return iv.get_answer(conv_obj, message)

    if msg_text.startswith('carikan'):
        result = ag1.ask_lc(msg_text)
        remove_flood()
        return result

    if conv_obj.free_tries:
        ct.kurangi_free_tries(conv_obj)
        letih = ""
        if conv_obj.free_tries == 0:
            letih = random.choice(cfg['IKLAN']['LETIH'])
        result = await api.ask_gpt(self, conv_obj, msg_text, memory=memory)
        result = f"{letih}{result}\n\n*[{conv_obj.free_tries}]*\u2713".strip()
        remove_flood()
        return result 

    rivereply = conv_obj.rivebot.reply("Irza Pulungan", message.text)
    if "<ERROR>" not in rivereply:
        print(f"{Fore.GREEN}{Back.LIGHTMAGENTA_EX}dia mengatakan : {message.text}{Style.RESET_ALL}")
        print(f"{Fore.RED}{Back.WHITE}saya menjawab: {rivereply}{Style.RESET_ALL}")
        await asyncio.sleep(10)
        ct.kurangi_funny_counter(conv_obj)
        remove_flood()
        if not conv_obj.promo_counter:
            rivereply = f"{rivereply}\n{promo}"
        return rivereply


    if conv_obj.funny_counter:
        ct.kurangi_funny_counter(conv_obj)
        ct.kurangi_promo_counter(conv_obj)
        pesan = random.choice(cfg['IKLAN']['PESAN'])
        result = await api.ask_ooba(self, conv_obj, msg_text)
        remove_flood()
        if not conv_obj.promo_counter:
            return f'{result}\n{pesan}\n{promo}'

        return f'{result}\n{pesan}'

    else:
        ct.kurangi_funny_counter(conv_obj)
        ct.kurangi_promo_counter(conv_obj)
        pesan = random.choice(cfg['IKLAN']['TRAKTIR'])
        remove_flood()
        if not conv_obj.promo_counter:
            return f'{pesan}\n{promo}'

        return f'{pesan}'



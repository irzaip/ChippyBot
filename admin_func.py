from conversations import Conversation, Message, Persona
from colorama import Fore, Style, Back
import persona_func as pf
import shlex
from agent1 import ask_lc
from agent3 import ask_pdf
from db_oper import insert_conv
import datetime
import toml
import apicall as api
import asyncio
import requests

cfg = toml.load('config.toml')

def eta(conv_obj: Conversation) -> str:
    return f"""Assalamualaikum semua.
Nama saya {conv_obj.bot_name}, saya disini membantu kakak-kakak dan abang-abang semua, untuk minta
bantuan saya, tulis nama saya di depan setiap permintaan kalian.

misalnya: *{conv_obj.bot_name} buatkan saya pidato kepresidenan untuk menerima G20 sebagai aliansi indonesia* 

hihi, tapi ya gak gitu juga ya.. kan situ bukan presiden. :))
permintaan harus spesifik dan jelas, supaya saya bisa lebih mudah mengerjakannya. Tapi jangan susah-susah juga yaaa... saya kan cuma robot yg kecil dan imut. :))
"""

def help() -> str:
    return f""".reset: reset to default
.who: check persona and mode
.set x y: set *y* to variable *x*
.get *x*: get the value of *x*
.msg x y: send msg y to var*x*
.list: display all variables keys
.send:
.join:
.intro: 
.others:
.eta: terangkanlah (perkenalan)
""" 

class AdminMemory():
    def __init__(self):
        self.admin_var = {}


admin_memory = AdminMemory()

async def run(msg_proc, conv_obj: Conversation, msg_text: str):
    print(f"{Style.BRIGHT}{Fore.CYAN}ADMIN COMMAND: {msg_text}{Style.RESET_ALL}")
    if msg_text.lower().startswith('.reset'):
        pf.set_persona(Persona.ASSISTANT, conv_obj)
        return pf.set_personality("Maya", "ASSISTANT", "Hai, Aku Maya, aku akan berusaha membantumu", conv_obj)
    if msg_text.lower().startswith('.who'):
        persona = conv_obj.persona
        mode = conv_obj.convmode
        return f'saya sekarang adalah {conv_obj.bot_name} dengan persona:{persona}, mode:{mode}'
    if msg_text.lower().startswith('.?'):
        return help()
    if msg_text.lower().startswith('.eta'):
        return eta(conv_obj)
    if msg_text.lower().startswith('.st'):
        return f"""ft: {conv_obj.free_tries}
fg: {conv_obj.free_gpt}
fc: {conv_obj.funny_counter}
pm: {conv_obj.paid_messages}
prs: {conv_obj.persona}
cm : {conv_obj.convmode}
ct : {conv_obj.convtype}
        """

    command = msg_text.lower().split(" ")
    match command:
        case [".set", setvar, *rest]:
            value = ""
            for i in rest:
                value = f"{value} {i}"
            admin_memory.admin_var[str(setvar)] = value.strip()
            return f"Done setting {str(setvar)} !"
        case [".get", var, *rest]:
            try:
                result = admin_memory.admin_var[str(var)]
                return f"isi dari {var} adalah {result}"
            except:
                return f"isi {var} tidak ada!"
        case [".list"]:
            result = admin_memory.admin_var.keys()
            return f"variabel yg ada : {result}"

    nama_bot = conv_obj.bot_name.lower()
    awalan = msg_text[:len(nama_bot)].lower()
    if awalan == nama_bot:
        msg_text = msg_text[len(conv_obj.bot_name):].strip()


    # BOT COMMANDS
    msgcommand = shlex.split(msg_text.lower())
    match msgcommand:
        case ['eta', *rest]:
            return eta(conv_obj)
        case ['file', filename]:
            return f'{filename} is the filename'
        case ['set', param1, param2]:
            return f'{param1} is set to {param2}'
        case ['pdf', *rest]:
            response = ask_pdf('./BBB.pdf', " ".join(rest))
            insert_conv(conv_obj.user_number,
                        conv_obj.bot_number,
                        int(datetime.datetime.utcnow().timestamp()), 
                        response, cfg['CONFIG']['DB_FILE'])
            return response            
        case ['cari', *rest]:
            response = ask_lc(" ".join(rest))
            insert_conv(conv_obj.user_number,
                        conv_obj.bot_number,
                        int(datetime.datetime.utcnow().timestamp()), 
                        response, cfg['CONFIG']['DB_FILE'])
            return response        
        # case ['gambar', *rest]:
        #     print(" ".join(rest))
        #     response = ask_dalle(conv_obj, " ".join(rest))
        #     return response
        case _ :
            result = await api.ask_gpt(msg_proc, conv_obj, msg_text)
            insert_conv(conv_obj.user_number,
                        conv_obj.bot_number,
                        int(datetime.datetime.utcnow().timestamp()), 
                        result, cfg['CONFIG']['DB_FILE'])
            result = f"{result}\n\n\u2764".strip()
            return result 



def build_prompt() -> str:
    prompt_build = ""
    for i in range(1,11):
        if str(i) in admin_memory.admin_var:
            prompt_build = f"{prompt_build} {admin_memory.admin_var[str(i)]}" 
    return prompt_build


async def notify_admin(message: str):
    for i in cfg['CONFIG']['ADMIN_NUMBER']:
        result = await send_to_phone(i, cfg['CONFIG']['BOT_NUMBER'], message)
    return result

async def send_to_phone(user_number: str, bot_number: str, message: str):
    """send langsung ke WA, tapi ke *user_number*, bukan ke bot_number"""
    message = {
        "message": message, # Replace with your message text
        "from": bot_number, # Replace with the sender number
        "to": user_number # Replace with out bot number
    } # type: ignore

    response = requests.post(cfg['WHATSAPP']['SEND_URL'], json=message)

    if response.status_code == 200:
        return "Message sent successfully!"
    else:
        return f"Error sending message. Status code: {response.status_code}"


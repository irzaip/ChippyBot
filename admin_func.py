from conversations import Conversation, Message, Persona
from colorama import Fore, Style, Back

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

def run(conv_obj: Conversation, msg_text: str) -> str:
    print(f"{Style.BRIGHT}{Fore.CYAN}{msg_text}{Style.RESET_ALL}")
    if msg_text.lower().startswith('.reset'):
        conv_obj.set_persona(Persona.ASSISTANT)
        return conv_obj.set_personality("Maya", "AST", "Hai, Aku Maya, aku akan berusaha membantumu")
    if msg_text.lower().startswith('.who'):
        persona = conv_obj.persona
        mode = conv_obj.mode
        return f'saya sekarang adalah {conv_obj.bot_name} dengan persona:{persona}, mode:{mode}'
    if msg_text.lower().startswith('.?'):
        return help()
    if msg_text.lower().startswith('.eta'):
        return eta(conv_obj)

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

def build_prompt() -> str:
    prompt_build = ""
    for i in range(1,11):
        if str(i) in admin_memory.admin_var:
            prompt_build = f"{prompt_build} {admin_memory.admin_var[str(i)]}" 
    return prompt_build

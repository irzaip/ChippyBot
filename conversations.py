from pydantic import BaseModel
from enum import Enum, auto
from rivescript import RiveScript # type: ignore
from dataclasses import dataclass
import toml
import requests
import asyncio
import json
from typing import Literal

cfg = toml.load('config.toml')

WORD_LIMIT = 1000
whatsapp_web_url = "http://localhost:8000/send" # Replace with your endpoint URL


# Model untuk validasi input pada endpoint /interval
class Interval(BaseModel):
    obj_num: int
    interval: float

class Persona(str, Enum):
    ASSISTANT = auto()
    USTAD = auto()
    HRD = auto()
    CONTENT_MANAGER = auto()
    CONTENT_CREATOR = auto()
    PSYCHOLOG = auto()
    ROLEPLAY = auto()
    KOBOLD = auto()
    

class Role(str, Enum):
    SYSTEM = auto()
    USER = auto()
    ASSISTANT = auto()

class Script(str, Enum):
    BRAIN = auto()
    DEPARSE = auto()
    JS_OBJECTS = auto()
    JSON_SERVER = auto()
    PARSER = auto()
    SESSIONS = auto()
    NEWCOMER = auto()
    INTERVIEW = auto()

class ConvMode(str, Enum):
    CHITCHAT = auto()
    ASK = auto()
    THINK = auto()
    QUIZ = auto()
    TIMED = auto()
    INTERVIEW = auto()
    YESNO = auto()
    CHAIN = auto()



class Message(BaseModel):
    """class message untuk perpindahan dari WA"""
    text: str
    user_number: str
    bot_number: str
    timestamp: int
    notifyName: str = ""
    type: str
    client: str
    author: str = ""
    hasMedia: bool = False
    message: dict = {}

    def toJSON(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
class InjectedMessage(BaseModel):
    """class message untuk injection system prompt"""
    system_str: str
    user_number: str
    bot_number: str = "6285775300227@c.us"
    send_msg : str

class MessageContent(BaseModel):
    """Class untuk bikin system.message ataupun role message content"""
    user_number: str
    bot_number: str = "6285775300227@c.us"
    message: str
    role: str = "SYSTEM"

class Conversation():
    """create conversation object unique to user"""
    def __init__(self, user_number: str, bot_number: str) -> None:
        if not bot_number:
            bot_number = "6285775300227@c.us"
        self.bot_name = "Maya"
        self.rivebot = RiveScript()
        self.rivebot.load_directory('./rive/brain')
        self.rivebot.sort_replies()
        self.mode=ConvMode.CHITCHAT
        self.interval = 600
        self.wait_time = 0
        self.messages = []
        self.botquestions = []
        self.WORD_LIMIT = WORD_LIMIT
        self.temperature = 0.7
        self.intro_msg = "Baik kita mulai tanya-jawab"
        self.outro_msg = "OK. semua sudah selesai, terima kasih"
        self.user_number = user_number
        self.bot_number = bot_number
        self.persona = Persona.ASSISTANT
        self.need_group_prefix = True
        self.last_question = 0
        self.question_asked = ""
        self.user_name = ""
        self.user_fullinfo = {}
        self.add_system("Kamu adalah Maya, Assisten yang baik. Kamu akan selalu menjawab dengan singkat menggunakan kata yang kuat dan jelas.")
        self.add_role_user("Kamu akan menjadi teman dalam chat, nama kamu Maya, dan pembuat kamu adalah Irza Pulungan, dia seorang programmer yang baik dan berbudi, kamu menjawab dengan singkat dengan gaya bahasa Raditya Dika. Saya akan mulai dengan menyapa kamu setelah ini. HALO")
        self.add_role_assistant("Halo, nama saya Maya, ada yang bisa saya bantu?")


    def add_last_question(self) -> None:
        self.last_question += 1

    def reset_last_question(self) -> None:
        self.last_question = 0

    def reset_botquestions(self) -> None:
        self.botquestions = []

    def reset_interview(self) -> None:
        self.last_question = 0
        self.botquestions = []

    def set_script(self, script: Script) -> None:
        all_scripts = {
            'BRAIN' : './rive/brain',
            'DEPARSE' : './rive/deparse',
            'JS-OBJECTS' : './rive/js-objects',
            'JSON-SERVER' : './rive/json-server',
            'PARSER' : './rive/parser',
            'SESSIONS' : './rive/sessions',
            'NEWCOMER' : './rive/newcomer',
            'INTERVIEW' : './rive/interview',
        }
        self.rivebot = RiveScript()
        self.rivebot.load_directory(all_scripts[script.name])
        self.rivebot.sort_replies()
        print(f"Loaded {script}")

    def reinit_rive(self, script_file) -> None:
        self.rivebot.load_directory(script_file)
        self.rivebot.sort_replies()

    def rivereply(self, message) -> str:
        reply = self.rivebot.reply("localuser", message)
        return reply

    def add_system(self, message: str) -> None:
        self.messages.append({"role" : "system", "content": message})

    def change_system(self, message: str) -> None:
        self.messages[0]['content'] = message
    
    def reset_system(self) -> None:
        self.messages = []
        
    def add_role_user(self, message: str) -> None:
        self.messages.append({"role": "user", "content" : message})
        
    def add_role_assistant(self, message: str) -> None:
        self.messages.append({"role" : "assistant", "content" : message})
     
    def get_user_number(self) -> str:
        return self.user_number
    
    def get_bot_number(self) -> str:
        return self.bot_number
        
    def __str__(self) -> str:
        return f"user{self.user_number}"

    def __repr__(self) -> str:
        return f"user{self.user_number}"
    
    def set_mode(self, mode: ConvMode) -> None:
        self.mode = mode

    def set_interval(self, interval: int) -> None:
        self.interval = interval

    def set_persona(self, persona: Persona) -> None:
        self.persona = persona
    
    def set_intro_msg(self, intro_msg: str) -> None:
        self.intro_msg = intro_msg

    def set_outro_msg(self, outro_msg: str) -> None:
        self.outro_msg = outro_msg
    
    def set_bot_name(self, bot_name: str) -> None:
        self.bot_name = bot_name

    def set_temperature(self, temperature: float) -> None:
        self.temperature = temperature

    def set_question_asked(self, question_asked: str) -> None:
        self.question_asked = question_asked

    def get_last_question(self) -> tuple:
        for i, item in enumerate(self.botquestions):
            if not item.answer:
                print("INDEX QUEST: ", i)
                return (i, len(self.botquestions))
                break
        return (len(self.botquestions),len(self.botquestions))

    async def send_msg(self, message: str) -> Literal['Done']:
        """send langsung ke WA, tapi ke *user_number*, bukan ke bot_number"""
        message = {
            "message": message, # Replace with your message text
            "from": self.bot_number, # Replace with the sender number
            "to": self.user_number, # Replace with out bot number
        } # type: ignore

        print(message)
        response = requests.post(whatsapp_web_url, json=message)

        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print(f"Error sending message. Status code: {response.status_code}")
            print(response.text)
        return "Done"

    async def timedcall(self) -> None:
        print("Method dipanggil pada objek dengan nama:", self.user_number)
        await self.send_msg("Method timer")

    async def start_coroutine(self) -> None:
        while True:
            await self.timedcall()
            await asyncio.sleep(self.interval)

    def get_params(self) -> str:
        """Mengeluarkan dalam bentuk json string (sudah termasuk json.dumps)"""
        obj = {
            'messages' : self.messages,
            'bot_name' : self.bot_name,
            'intro_msg' : self.intro_msg,
            'outro_msg' : self.outro_msg,
            'interval' : self.interval,
            'persona' : self.persona,
            'need_group_prefix' : self.need_group_prefix,
            'mode' : self.mode,
            'question_asked' : self.question_asked,
            'temperature' : self.temperature,
            'wait_time' : self.wait_time,
            'user_name' : self.user_name,
            'user_fullinfo' : self.user_fullinfo,
        }
        return json.dumps(obj)

    def put_params(self, j: str) -> str:
        """Sudah termasuk json.loads (masukan hanya si string dari db)"""
        obj = json.loads(j)
        self.messages = obj['messages']
        self.bot_name = obj['bot_name']
        self.intro_msg = obj['intro_msg']
        self.outro_msg = obj['outro_msg']
        self.interval = obj['interval']
        self.persona = obj['persona']
        self.need_group_prefix = obj['need_group_prefix']
        self.mode = obj['mode']
        self.question_asked = obj['question_asked']
        self.temperature = obj['temperature']
        self.wait_time = obj['wait_time']
        self.user_name = obj['user_name']
        self.user_fullinfo = obj['user_fullinfo']
        return "Done"
    
    def set_lisa_hrd(self) -> None:
        self.last_question = 0
        self.botquestions = []
        self.persona = Persona.HRD
        

@dataclass
class BotQuestion():
    id: int
    question: str
    answer: str = ""
    metadata: str = ""
    koherensi: int = 1
    multiplier: int = 1
    score: int = 1
    comment: str = ""




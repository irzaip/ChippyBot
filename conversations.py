from pydantic import BaseModel
from enum import Enum, auto
from rivescript import RiveScript
from dataclasses import dataclass
import nltk
import requests
import asyncio
import openai
import time
import random

MAX_TOKEN = 4192
WORD_LIMIT = 1000
whatsapp_web_url = "http://localhost:8000/send" # Replace with your endpoint URL


# Model untuk validasi input pada endpoint /interval
class Interval(BaseModel):
    obj_num: int
    interval: float

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
    def __init__(self, user_number, bot_number):
        if not bot_number:
            bot_number = "6285775300227@c.us"
        self.rivebot = RiveScript()
        self.rivebot.load_directory('./rive/brain')
        self.rivebot.sort_replies()
        self.mode=ConvMode.CHITCHAT
        self.interval = 600
        self.wait_time = 0
        self.messages = []
        self.botquestions = []
        self.MAX_TOKEN = MAX_TOKEN
        self.WORD_LIMIT = WORD_LIMIT
        self.temperature = 0.7
        self.intro_msg = "Baik kita mulai tanya-jawab"
        self.outro_msg = "OK. semua sudah selesai, terima kasih"
        self.user_number = user_number
        self.bot_number = bot_number
        self.add_system("Kamu adalah Maya, Assisten yang baik. Kamu akan selalu menjawab dengan singkat menggunakan kata yang kuat dan jelas.")
        self.add_role_user("Kamu akan menjadi teman dalam chat, nama kamu Maya, dan pembuat kamu adalah Irza Pulungan, dia seorang programmer yang baik dan berbudi, kamu menjawab dengan singkat dengan gaya bahasa Raditya Dika. Saya akan mulai dengan menyapa kamu setelah ini. HALO")
        self.add_role_assistant("Halo, nama saya Maya, ada yang bisa saya bantu?")

    def set_script(self, script: Script):
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

    def reinit_rive(self, script_file):
        self.rivebot.load_directory(script_file)
        self.rivebot.sort_replies()

    def rivereply(self, message):
        reply = self.rivebot.reply("localuser", message)
        return reply

    def add_system(self, message):
        self.messages.append({"role" : "system", "content": message})

    def change_system(self, message):
        self.messages[0]['content'] = message
    
    def reset_system(self, message):
        self.messages = []
        self.add_system(message)
        
    def add_role_user(self, message):
        self.messages.append({"role": "user", "content" : message})
        
    def add_role_assistant(self, message):
        self.messages.append({"role" : "assistant", "content" : message})
    
    def get_user(self):
        return self.user_number
    
    def get_bot(self):
        return self.bot_number
        
    def __str__(self):
        return f"user{self.user_number}"

    def __repr__(self):
        return f"user{self.user_number}"
    

    def get_last_question(self) -> tuple:
        for i, item in enumerate(self.botquestions):
            if not item.answer:
                print("INDEX QUEST: ", i)
                return (i, len(self.botquestions))
                break
        return (len(self.botquestions),len(self.botquestions))

    async def send_msg(self, message: str) -> None:
        """send langsung ke WA, tapi ke *user_number*, bukan ke bot_number"""
        message = {
            "message": message, # Replace with your message text
            "from": self.bot_number, # Replace with the sender number
            "to": self.user_number # Replace with out bot number
        }

        response = await requests.post(whatsapp_web_url, json=message)

        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print(f"Error sending message. Status code: {response.status_code}")
            print(response.text)

    async def timedcall(self):
        print("Method dipanggil pada objek dengan nama:", self.user_number)
        await self.send_msg("Method timer")

    async def start_coroutine(self):
        while True:
            await self.timedcall()
            await asyncio.sleep(self.interval)
    
@dataclass
class BotQuestion():
    id: int
    question: str
    answer: str = ""
    metadata: str = ""
    koherensi: int = 1
    multiplier: int = 1
    score: int = 1


class MsgProcessor:
    def __init__(self, conv_obj: Conversation):
        self.name = "Process"
        self.Conversation = conv_obj
        self.response = ""
        #self.run(conv_obj, message)

    def whata(self):
        return "This is a SUPPER CALLING"
    
    def run(self, message: str) -> str:

        if self.Conversation.mode != ConvMode.ASK:
            reply = self.Conversation.rivereply(message)
            print("MY REPLY : ----->" , reply)
            if reply == "BBB":
                if "dalle" not in message:
                    self.response = self.ask_gpt(self.Conversation, message)
                    return self.response
                self.response = self.ask_dalle(self.Conversation, message)
                return self.response
            else:
                return reply
        (i,k) = self.Conversation.get_last_question()
        if i < (k-1):
            self.Conversation.botquestions[i].answer = message
            return self.Conversation.botquestions[i+1].question
        self.Conversation.mode = ConvMode.CHITCHAT
        self.Conversation.set_script(Script.BRAIN)
        return self.Conversation.outro_msg
    
        if (self.count_words(self.Conversation.messages) > self.Conversation.WORD_LIMIT):
            self.Conversation.messages = self.reduce_conversation(self.Conversation.messages)
        return self.response

    def count_words(self, messages: list) -> int:
        "Menghitung kata dalam iterasi sebuah value dict"
        words = []
        for i in messages:
            words.extend(nltk.word_tokenize(i['content']))
        return len(words)

    def reduce_conversation(self, messages: list) -> list:
        """memotong conversation menjadi setengah percakapan"""
        print(len(messages))
        for i in messages:
            print(i['content'])
        half_way = int(len(messages) / 2 + 1)
        messages = messages[:1] + messages[half_way:]
        return messages

    def ask_gpt(self, conv_obj: Conversation, prompt: str) -> str:
        """
        Akses API ke OpenAI, dari prompt menjadi hasil string
        
        input: masuknya list dari Object Conversation.messages
        """
        # cek panjang conversation, potong setengah bila lebih dari TOKEN_LIMIT

        conv_obj.messages.append({"role" : "user", "content" : prompt})
        #print("WORD COUNTS:--------------------------> ", conv_obj.count_words(conv_obj.messages))

        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conv_obj.messages,
        max_tokens=2000,
    #      n=1,
    #      stop=None,
    #      temperature=0.7,
        )
        ## the calling
        message = response.choices[0].message.content
        conv_obj.messages.append({"role" : "assistant", "content" : message})
        time.sleep(random.randint(2,7))
        return message

    def ask_dalle(self, conv_obj: Conversation, prompt: str):
        """generate dalle"""

        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512",
        )

        message = response["data"][0]["url"]
        return message

               

    

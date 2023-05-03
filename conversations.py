from pydantic import BaseModel
from enum import Enum, auto
from rivescript import RiveScript
from dataclasses import dataclass

class Role(str, Enum):
    SYSTEM = auto()
    USER = auto()
    ASSISTANT = auto()


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
    def __init__(self, user_number, bot_number, messages):
        self.rivebot = RiveScript()
        self.rivebot.load_directory('./rive/brain')
        self.rivebot.sort_replies()
        self.messages = []
        self.max_token = 4192
        self.temperature = 0.7
        self.user_number = user_number
        self.bot_number = bot_number
        self.add_system("Kamu adalah Maya, Assisten yang baik. Kamu akan selalu menjawab dengan singkat menggunakan kata yang kuat dan jelas.")
        self.add_role_user("Kamu akan menjadi teman dalam chat, nama kamu Maya, dan pembuat kamu adalah Irza Pulungan, dia seorang programmer yang baik dan berbudi, kamu menjawab dengan singkat dengan gaya bahasa Raditya Dika. Saya akan mulai dengan menyapa kamu setelah ini. HALO")
        self.add_role_assistant("Halo, nama saya Maya, ada yang bisa saya bantu?")

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
    
    def process(self, func, messages, message):
        self.response = func(messages, message)
        return self.response

@dataclass
class BotQuestion():
    id: int
    question: str
    answer: str = ""
    multiplier: int = 1
    score: int = 1




        
    
    
                  
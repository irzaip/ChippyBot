from conversations import Conversation, Message, ConvMode, Persona, Script, Role
import sqlite3
import time, random
from agent1 import ask_lc
from agent3 import ask_pdf
from agent7 import agent_liza
import nltk
import openai
import datetime
import re, shlex
import toml
from db_oper import insert_conv

cfg = toml.load('config.toml')

class MsgProcessor:
    def __init__(self, conv_obj: Conversation, db_file: str):
        self.name = "Process"
        self.conv_obj = conv_obj
        self.response = ""
        self.persona = conv_obj.persona
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def process(self, message: Message):

        """Terima pesan dari WA"""
        nama_bot = self.conv_obj.bot_name.lower()
        awalan = message.text[:len(nama_bot)].lower()
        #abaikan msg group ini
        if (self.conv_obj.need_group_prefix) and (message.author != '') and ( nama_bot != awalan ):
            return None

        #potong awalan
        if awalan == nama_bot:
            message.text = message.text[len(self.conv_obj.bot_name):].strip()

        #buang aja karakter unicode
        message.text = message.text.encode('ascii', errors='ignore').decode()

        if message.text.startswith('RESET'):
            self.conv_obj.reset_system()
            self.conv_obj.set_bot_name("Maya")
            self.conv_obj.add_system(cfg['AST']['M_S'])
            self.conv_obj.add_role_user(cfg['AST']['M_U'])
            self.conv_obj.add_role_assistant(cfg['AST']['M_A'])  
            return "Maya disini, Oke menjadi Asisten"               

        print("-------------------------------------------------")
        print("Message:",message)
        print("-------------------------------------------------")
        insert_conv(self.conv_obj.user_number, self.conv_obj.bot_number, int(message.timestamp), message.text, 'cipibot.db')

        msgcommand = shlex.split(message.text.lower())
        match msgcommand:
            case ['file', filename]:
                return f'{filename} is the filename'
            case ['set', param1, param2]:
                return f'{param1} is set to {param2}'
            case ['pdf', *rest]:
                response = ask_pdf('./BBB.pdf', " ".join(rest))
                insert_conv(self.conv_obj.user_number,
                            self.conv_obj.bot_number,
                            int(datetime.datetime.utcnow().timestamp()), 
                            response, 'cipibot.db')
                return response            
            case ['lch', *rest]:
                response = ask_lc(" ".join(rest))
                insert_conv(self.conv_obj.user_number,
                            self.conv_obj.bot_number,
                            int(datetime.datetime.utcnow().timestamp()), 
                            response, 'cipibot.db')
                return response        
            case ['dalle', *rest]:
                print(" ".join(rest))
                response = self.ask_dalle(self.conv_obj, " ".join(rest))
                return response
            case ['hrd', *rest]:
                self.conv_obj.reset_system()
                self.conv_obj.set_bot_name("Lisa")
                self.conv_obj.add_system(cfg['HRD']['M_S'])
                self.conv_obj.add_role_user(cfg['HRD']['M_U'])
                self.conv_obj.add_role_assistant(cfg['HRD']['M_A'])  
                return "Lisa disini, Oke menjadi HRD"               
            case ['ast', *rest]:
                self.conv_obj.reset_system()
                self.conv_obj.set_bot_name("Maya")
                self.conv_obj.add_system(cfg['AST']['M_S'])
                self.conv_obj.add_role_user(cfg['AST']['M_U'])
                self.conv_obj.add_role_assistant(cfg['AST']['M_A'])  
                return "Maya disini, Oke menjadi Asisten"               
            case ['vol', *rest]:
                self.conv_obj.reset_system()
                self.conv_obj.set_bot_name("Vol")
                self.conv_obj.add_system(cfg['VOL']['M_S'])
                self.conv_obj.add_role_user(cfg['VOL']['M_U'])
                self.conv_obj.add_role_assistant(cfg['VOL']['M_A'])  
                return "Aku Voldemort, panggil aku Vol, bersiaplah budak!"               
            case ['wh', *rest]:
                self.conv_obj.reset_system()
                self.conv_obj.set_bot_name("wh")
                self.conv_obj.add_system(cfg['WH']['M_S'])
                self.conv_obj.add_role_user(cfg['WH']['M_U'])
                self.conv_obj.add_role_assistant(cfg['WH']['M_A'])  
                return "Aku Whitty, si wh, apa masalahmu?"               


        if self.conv_obj.mode == ConvMode.YESNO:
            if "y" in message.text.lower():
                return "Kamu menjawab ya"
            if "t" in message.text.lower():
                return "Kamu menjawab tidak"


        if self.conv_obj.mode == ConvMode.ASK:
            #mengisi answer yg masih kosong.
            (i,k) = self.conv_obj.get_last_question()
            if i < (k-1):
                self.conv_obj.botquestions[i].answer = message.text
                try:
                    r_text = self.conv_obj.botquestions[i+1].question
                    return r_text
                except Exception as e:
                    print(e)                 
            self.conv_obj.mode = ConvMode.CHITCHAT
            self.conv_obj.set_script(Script.BRAIN)
            return self.conv_obj.outro_msg

        if self.persona == Persona.ASSISTANT:
            #cobj = AssistantPersona(conv_obj=self.conv_obj)
            result = self.ask_gpt(self.conv_obj, message.text)
            #result = cobj.run(self.conv_obj, message)
            insert_conv(self.conv_obj.user_number,
                        self.conv_obj.bot_number,
                        int(datetime.datetime.utcnow().timestamp()), 
                        result, 'cipibot.db')
            return result 

        return "pfft..."

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
        # cek panjang conversation

        conv_obj.messages.append({"role" : "user", "content" : prompt})

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


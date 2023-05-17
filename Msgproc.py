from conversations import Conversation, Message, ConvMode, Persona, Script
import sqlite3
import time, random, requests
from agent1 import ask_lc
from agent3 import ask_pdf
import nltk
import openai
import datetime
import shlex
import toml, json
from typing import Union
from db_oper import insert_conv
from trans_id import input_modifier,output_modifier
from admin_func import *
from reduksi import trim_msg

cfg = toml.load('config.toml')

class MsgProcessor:
    def __init__(self, conv_obj: Conversation, db_file: str) -> None:
        self.name = "Process"
        self.conv_obj = conv_obj
        self.response = ""
        self.persona = conv_obj.persona
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def is_admin(self, message: Message) -> bool:
        admin_number = cfg['CONFIG']['ADMIN_NUMBER']
        if message.user_number in admin_number or message.author in admin_number:
            return True
        return False
    
    def process(self, message: Message) -> Union[str, None, str]:
        """Prosedur ini memproses Terima pesan dari WA"""

        #ADMIN COMMAND.
        if self.is_admin(message) and message.text.startswith('.'):
            if message.text.lower().startswith('.reset'):
                self.conv_obj.set_persona(Persona.ASSISTANT)
                return self.set_personality("Maya", "AST", "Hai, Aku Maya, aku akan berusaha membantumu")
            if message.text.lower().startswith('.who'):
                persona = self.conv_obj.persona
                mode = self.conv_obj.mode
                return f'saya sekarang adalah {self.conv_obj.bot_name} dengan persona:{persona}, mode:{mode}'
            if message.text.lower().startswith('.?'):
                return admin_help(self)
            if message.text.lower().startswith('.eta'):
                return admin_eta(self)
            
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



        print("-------------------------------------------------")
        print("Message:",message)
        print("-------------------------------------------------")

        human_say = "HUMAN: "+message.text
        insert_conv(self.conv_obj.user_number, self.conv_obj.bot_number, int(message.timestamp), human_say, 'cipibot.db')

        # BOT COMMANDS
        msgcommand = shlex.split(message.text.lower())
        match msgcommand:
            case ['eta', *rest]:
                return admin_eta(self)
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
            case ['cari', *rest]:
                response = ask_lc(" ".join(rest))
                insert_conv(self.conv_obj.user_number,
                            self.conv_obj.bot_number,
                            int(datetime.datetime.utcnow().timestamp()), 
                            response, 'cipibot.db')
                return response        
            case ['gambar', *rest]:
                print(" ".join(rest))
                response = self.ask_dalle(self.conv_obj, " ".join(rest))
                return response
            case ['hrd', *rest]:
                self.conv_obj.set_persona(Persona.HRD)
                return self.set_personality("Lisa", "HRD", "Sekarang aku Lisa, siap membantu persoalan HRD")
            case ['ast', *rest]:
                self.conv_obj.set_persona(Persona.ASSISTANT)
                return self.set_personality("Maya", "AST", "Hai, Aku Maya, aku akan berusaha membantumu")
            case ['vol', *rest]:
                self.conv_obj.set_persona(Persona.ASSISTANT)
                return self.set_personality("Vol", "VOL",  "Hai budak, siapkan tentaraku sekarang!")
            case ['wh', *rest]:
                self.conv_obj.set_persona(Persona.ASSISTANT)
                return self.set_personality("Wh", "WH", "Aku Whitty, panggil aku wh, aku sangat moody")
            case ['mgm', *rest]:
                self.conv_obj.set_persona(Persona.ASSISTANT)
                return self.set_personality("Mgm", "MGM", "Akulah MEGUMIN, panggil aku mgm")
            case _ :
                pass

        # PROCESS BY PERSONA AND MODE
        if self.conv_obj.mode == ConvMode.YESNO:
            if "y" in message.text.lower():
                return "Kamu menjawab ya"
            if "t" in message.text.lower():
                return "Kamu menjawab tidak"

        if self.conv_obj.mode == ConvMode.ASK:
            if "ok" in message.text.lower():
                return "oke juga"

        if self.conv_obj.mode == ConvMode.INTERVIEW:
            #mengisi answer yg masih kosong.
            (i,k) = self.conv_obj.get_last_question()
            if i < (k-1):
                self.conv_obj.botquestions[i].answer = message.text
                try:
                    r_text = self.conv_obj.botquestions[i+1].question
                    self.conv_obj.set_question_asked(r_text)
                    return r_text
                except Exception as e:
                    print(e)                 
            self.conv_obj.mode = ConvMode.CHITCHAT
            self.conv_obj.set_script(Script.BRAIN)
            return self.conv_obj.outro_msg

        if self.persona == Persona.KOBOLD:
            result = self.ask_kobold(self.conv_obj, message.text)
            insert_conv(self.conv_obj.user_number,
                        self.conv_obj.bot_number,
                        int(datetime.datetime.utcnow().timestamp()), 
                        result, 'cipibot.db')
            return result 

        if self.persona == Persona.ASSISTANT:
            #cobj = AssistantPersona(conv_obj=self.conv_obj)
            result = self.ask_gpt(self.conv_obj, message.text)
            #result = cobj.run(self.conv_obj, message)
            insert_conv(self.conv_obj.user_number,
                        self.conv_obj.bot_number,
                        int(datetime.datetime.utcnow().timestamp()), 
                        result, 'cipibot.db')
            return result 

        # JUST RETURN IT
        return "pfft..."
    
    def set_personality(self, bot_name: str, conf_section: str, reply_with: str) -> str:
        self.conv_obj.reset_system()
        self.conv_obj.set_bot_name(bot_name)
        self.conv_obj.add_system(cfg[conf_section]['M_S'])
        self.conv_obj.add_role_user(cfg[conf_section]['M_U'])
        self.conv_obj.add_role_assistant(cfg[conf_section]['M_A'])  
        return reply_with

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
        conv_obj.messages = trim_msg(conv_obj.messages)
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
        message = response.choices[0].message.content # type: ignore
        conv_obj.messages.append({"role" : "assistant", "content" : message})
        time.sleep(random.randint(2,7))
        return message

    def ask_dalle(self, conv_obj: Conversation, prompt: str): # type: ignore
        """generate dalle"""

        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512",
        )

        message = response["data"][0]["url"] # type: ignore
        return message

    def ask_kobold(self, conv_obj: Conversation, prompt: str) -> str:

        conv_obj.messages.append({"role" : "user", "content" : prompt})
        messages = input_modifier("".join([" ".join(cnt['content']) for cnt in conv_obj.messages]))
        print(messages)
        data = {
            'prompt': messages,
            'temperature': 0.7,
            'top_p': 0.9,
        }
        response = requests.post(f"http://127.0.0.1:5000/api/v1/generate", json=data)
                

        reply = json.loads(response.text)
        print(reply)
        reply = output_modifier(reply['results'][0]['text'])
        conv_obj.messages.append({'role': "assistant", "content": reply})
        return reply


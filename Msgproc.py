from conversations import Conversation, Message, ConvMode, Persona, Script, ConvType
import sqlite3
import time, random, requests
from agent1 import ask_lc
from agent3 import ask_pdf
import openai
import datetime
import shlex
import toml
from typing import Union
from db_oper import insert_conv
from trans_id import input_modifier,output_modifier
import admin_func as admin
from reduksi import trim_msg
#from queue import Queue
import asyncio
import time
from colorama import Fore, Back, Style
import demo_func as demo

cfg = toml.load('config.toml')



class MsgProcessor:
    def __init__(self, db_file: str) -> None:
        self.name = "Process"
        #self.conv_obj = conv_obj
        self.queue = asyncio.Queue()
        self.queue2 = asyncio.Queue()
        self.response = ""
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.antrian1 = 0
        self.antrian2 = 0
        self.on_maintenance = False


    def is_admin(self, message: Message) -> bool:
        admin_number = cfg['CONFIG']['ADMIN_NUMBER']
        if message.user_number in admin_number or message.author in admin_number:
            return True
        return False

    #LOOP TIKET UNTUK OOBA - tidur 2 detik tapi antri
    async def process_queue_ooba(self):
        while True:
            try:
                tiket = await self.queue2.get()
                print(f'panggilan untuk antrian {tiket} !!')
                await asyncio.sleep(2)
            except:
                print(f'tidak ada antrian')
                await asyncio.sleep(0.01)
                self.queue.task_done()


    #LOOP TIKET UNTUK CHATGPT - tidur 20 detik antar request
    async def process_queue_gpt(self):
        while True:
            try:
                tiket = await self.queue.get()
                print(f'panggilan untuk antrian {tiket} !!')
                await asyncio.sleep(20)
            except:
                print(f'tidak ada antrian')
                await asyncio.sleep(0.01)
                self.queue.task_done()


    async def process(self, conv_obj: Conversation, message: Message) -> Union[str, None, str]:
        """Prosedur ini memproses Terima pesan dari WA"""

        #ADMIN COMMAND.
        if self.is_admin(message) and message.text.startswith('.'):
            return admin.run(conv_obj, message.text)
            
        nama_bot = conv_obj.bot_name.lower()
        awalan = message.text[:len(nama_bot)].lower()
        #abaikan msg group ini
        if (conv_obj.need_group_prefix) and (message.author != '') and ( nama_bot != awalan ):
            return None

        #potong awalan
        if awalan == nama_bot:
            message.text = message.text[len(conv_obj.bot_name):].strip()

        #ignore looping error send
        if message.text.lower().startswith("ada error"):
            return None

        #
        #PRA PROCESSING MESSAGE - buang aja karakter unicode dan quote
        message.text = str(message.text)
        message.text = message.text.encode('ascii', errors='ignore').decode()
        message.text = message.text.replace("'"," ").replace('"',' ')


        print("-------------------------------------------------")
        print(f"{Fore.GREEN}{Style.BRIGHT}Message:",message)
        print(f"{Style.RESET_ALL}-------------------------------------------------")

        human_say = "HUMAN: "+message.text
        insert_conv(conv_obj.user_number, conv_obj.bot_number, int(message.timestamp), human_say, self.db_file)

        # BOT COMMANDS
        msgcommand = shlex.split(message.text.lower())
        match msgcommand:
            case ['eta', *rest]:
                return admin.eta(conv_obj)
            case ['file', filename]:
                return f'{filename} is the filename'
            case ['set', param1, param2]:
                return f'{param1} is set to {param2}'
            case ['pdf', *rest]:
                response = ask_pdf('./BBB.pdf', " ".join(rest))
                insert_conv(conv_obj.user_number,
                            conv_obj.bot_number,
                            int(datetime.datetime.utcnow().timestamp()), 
                            response, self.db_file)
                return response            
            case ['cari', *rest]:
                response = ask_lc(" ".join(rest))
                insert_conv(conv_obj.user_number,
                            conv_obj.bot_number,
                            int(datetime.datetime.utcnow().timestamp()), 
                            response, self.db_file)
                return response        
            case ['gambar', *rest]:
                print(" ".join(rest))
                response = self.ask_dalle(conv_obj, " ".join(rest))
                return response
            case ['hrd', *rest]:
                conv_obj.set_persona(Persona.HRD)
                return conv_obj.set_personality("Lisa", "HRD", "Sekarang aku Lisa, siap membantu persoalan HRD")
            case ['ast', *rest]:
                conv_obj.set_persona(Persona.ASSISTANT)
                return conv_obj.set_personality("Maya", "AST", "Hai, Aku Maya, aku akan berusaha membantumu")
            case ['vol', *rest]:
                conv_obj.set_persona(Persona.ASSISTANT)
                return conv_obj.set_personality("Maya", "VOL",  "Hai budak, siapkan tentaraku sekarang!")
            case ['wh', *rest]:
                conv_obj.set_persona(Persona.ASSISTANT)
                return conv_obj.set_personality("Wh", "WH", "Aku Whitty, panggil aku wh, aku sangat moody")
            case ['mgm', *rest]:
                conv_obj.set_persona(Persona.ASSISTANT)
                return conv_obj.set_personality("Mgm", "MGM", "Akulah MEGUMIN, panggil aku mgm")
            case _ :
                pass

        # on maintenance
        if self.on_maintenance and not self.is_admin(message):
            print(f"{Fore.RED}{Back.WHITE}Called.. But ON MAINTENANCE NOW{Fore.WHITE}{Back.BLACK}")
            return "*BRB* - Be Right Back .. ZzzZzz ZZzzzz.."

        if (conv_obj.convtype == ConvType.ADMIN) or conv_obj.free_gpt:
            result = await self.ask_gpt(conv_obj, message.text)
            insert_conv(conv_obj.user_number,
                        conv_obj.bot_number,
                        int(datetime.datetime.utcnow().timestamp()), 
                        result, self.db_file)
            result = f"{result}\n\n\u2764".strip()
            return result 

        if conv_obj.convtype == ConvType.FRIEND:
            if conv_obj.paid_messages:
                conv_obj.kurangi_paid_messages
                result = await self.ask_gpt(conv_obj, message.text)
                #result = cobj.run(self.conv_obj, message)
                insert_conv(conv_obj.user_number,
                            conv_obj.bot_number,
                            int(datetime.datetime.utcnow().timestamp()), 
                            result, self.db_file)
                result = f"{result}\n\n*[{conv_obj.paid_messages}]*".strip()
                return result 

        promo = ""    
        if conv_obj.convtype == ConvType.DEMO:
            promo = demo.run(conv_obj, message.text)
            if conv_obj.free_tries:
                conv_obj.kurangi_free_tries()
                result = await self.ask_gpt(conv_obj, message.text)
                insert_conv(conv_obj.user_number,
                            conv_obj.bot_number,
                            int(datetime.datetime.utcnow().timestamp()), 
                            result, self.db_file)
                result = f"{result}\n\n*[{conv_obj.free_tries}]*\u2713".strip()
                return result 


        ##EXTRA PROCESS RIVE
        if not self.is_admin(message):
            rivereply = conv_obj.rivebot.reply("Irza Pulungan", message.text)
            if "<ERROR>" not in rivereply:
                print(f"{Fore.GREEN}{Back.LIGHTMAGENTA_EX}dia mengatakan : {message.text}{Style.RESET_ALL}")
                print(f"{Fore.RED}{Back.WHITE}saya menjawab: {rivereply}")
                await asyncio.sleep(10)
                return rivereply


        # PROCESS BY PERSONA AND MODE
        if conv_obj.convmode == ConvMode.YESNO:
            if "y" in message.text.lower():
                return "Kamu menjawab ya"
            if "t" in message.text.lower():
                return "Kamu menjawab tidak"

        if conv_obj.convmode == ConvMode.ASK:
            if "ok" in message.text.lower():
                return "oke juga"

        if conv_obj.convmode == ConvMode.INTERVIEW:
            #mengisi answer yg masih kosong.
            (i,k) = conv_obj.get_last_question()
            if i < (k-1):
                conv_obj.botquestions[i].answer = message.text
                try:
                    r_text = conv_obj.botquestions[i+1].question
                    conv_obj.set_question_asked(r_text)
                    return r_text
                except Exception as e:
                    print(e)                 
            conv_obj.convmode = ConvMode.CHITCHAT
            conv_obj.set_script(Script.BRAIN)
            return conv_obj.outro_msg


        if conv_obj.persona == Persona.ASSISTANT:
            #cobj = AssistantPersona(conv_obj=self.conv_obj)
            result = await self.ask_ooba(conv_obj, message.text)
            #result = cobj.run(self.conv_obj, message)
            insert_conv(conv_obj.user_number,
                        conv_obj.bot_number,
                        int(datetime.datetime.utcnow().timestamp()), 
                        result, self.db_file)
            result = f"{result}\n\n{promo}".strip()
            return result 

        # JUST RETURN IT
        return "pfft..."
    
    async def ask_gpt(self, conv_obj: Conversation, prompt: str) -> str:
        """
        Akses API ke OpenAI, dari prompt menjadi hasil string        
        input: masuknya list dari Object Conversation.messages
        """
        self.antrian1 += 1
        print(f'sekarang antrian: {self.antrian1}. > put')
        self.queue.put_nowait(self.antrian1)

        while self.queue.qsize() > 0:
            print(f'{Style.DIM}masih ada {self.queue.qsize()} antrian{Style.NORMAL}')
            await asyncio.sleep(1)

        print(f'tiket sudah di proses. mari kita kerjakan {self.antrian1}')

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

    def build_pre_prompt(self, conv_obj: Conversation) -> str:
        result = ""
        for i in conv_obj.messages:
            if i['role'] == 'system':
                result = result + input_modifier(f"{i['content']}\n")
            if i['role'] == 'user':
                result = result + input_modifier(f"\nSaya:{i['content']}\n")
            if i['role'] == 'assistant':
                result = result + input_modifier(f"\nMaya:{i['content']}\n")
        return result

    async def ask_ooba(self, conv_obj: Conversation, prompt: str):

        self.antrian2 += 1
        print(f'sekarang antrian: {self.antrian2}. > put')
        self.queue2.put_nowait(self.antrian2)

        while self.queue2.qsize() > 0:
            print(f'masih ada {self.queue2.qsize()} antrian')
            await asyncio.sleep(1)

        print(f'tiket sudah di proses. mari kita kerjakan {self.antrian2}')


        intro = self.build_pre_prompt(conv_obj)
        req = intro + input_modifier(f"Saya:{prompt}\n{conv_obj.bot_name}:")
        request = {
            'prompt': req,
            'max_new_tokens': 80,
            'do_sample': True,
            'temperature': 0.8,
            'top_p': 0.4,
            'typical_p': 1,
            'repetition_penalty': 1.18,
            'top_k': 40,
            'min_length': 2,
            'no_repeat_ngram_size': 0,
            'num_beams': 1,
            'penalty_alpha': 0,
            'length_penalty': 1.2,
            'early_stopping': True,
            'seed': -1,
            'add_bos_token': True,
            'truncation_length': 2048,
            'ban_eos_token': False,
            'skip_special_tokens': True,
            'stopping_strings': ['Saya:','.','Me:'],

        }
        conv_obj.messages.append({'role': 'user', 'content': output_modifier(prompt)})
        print(f'{Fore.CYAN}{req}{Fore.WHITE}')
        response = requests.post("http://127.0.0.1:5000/api/v1/generate", json=request)

        if response.status_code == 200:
            result = response.json()['results'][0]['text']
            conv_obj.messages.append({'role': 'assistant', 'content': output_modifier(result)})
            print('\n\nResponse:\n')
            intro = intro + f"\n\nSaya:{prompt}\nMaya:{result}"
            print(f'{Fore.CYAN}{intro}{Fore.WHITE}\n\n')
            return output_modifier(result)
        else:
            return None
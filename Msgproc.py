from conversations import Conversation, Message, ConvMode, Persona, Script, ConvType
import sqlite3
import toml
from typing import Union
import db_oper as dbo
import admin_func as admin

#from queue import Queue
import asyncio
from colorama import Fore, Back, Style
import demo_func as demo
import friend_func as friend
import apicall as api
import counting as ct
import interview as iv
import gold_func as gold
import platinum_func as platinum
import persona_func as pf
import agent_info_cs as cs
import sd_agent as sd

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
        if (message.user_number in admin_number) or (message.author in admin_number):
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

    def is_ignored(self, message: Message):
        if (message.author in cfg['IGNORE']['IGNORE']) or (message.user_number in cfg['IGNORE']['IGNORE']):
            return True
        else:
            return False

    async def process(self, conv_obj: Conversation, message: Message) -> Union[str, None, str]:
        """Prosedur ini memproses Terima pesan dari WA"""
        #ct.pra_proses(conv_obj)
        print( f"{Fore.MAGENTA}ft:{conv_obj.free_tries}, ct:{conv_obj.convtype}, fc:{conv_obj.funny_counter}{Style.RESET_ALL}")
            
        nama_bot = conv_obj.bot_name.lower()
        awalan = message.text[:len(nama_bot)].lower()

        if self.is_ignored(message):
            print(f'{Fore.WHITE}{Back.RED}MESSAGE IGNORED{Fore.RESET}{Back.RESET}')
            return None

        print(f"admin: {self.is_admin(message)}, dot:{message.text.startswith('.')}")
        #ADMIN COMMAND.
        if self.is_admin(message) and (nama_bot == awalan):
            return await admin.run(self, conv_obj, message.text) 

        if message.text.startswith('.'):
            if self.is_admin(message):
                return await admin.run(self, conv_obj, message.text)

        if "konfirmasi" in message.text.lower():
            if message.author:
                await admin.notify_admin(f'konfirmasi signal from group {message.user_number} or {message.author}')
            else:
                await admin.notify_admin(f'konfirmasi signal at japrian {message.user_number}')

        if "info_cs" in message.text.lower():
            conv_obj.persona = Persona.ASSISTANT
            pf.set_persona(Persona.SALES_CS, conv_obj)
            conv_obj.free_gpt = True
            print(f'{Fore.RED}{Back.WHITE}ADA SIGNAL INFO_CS DARI {message.user_number}{Fore.RESET}{Back.RESET}')
            await admin.notify_admin(f'signal INFO_CS dari user {message.user_number}')
            dbo.insert_info_cs(conv_obj.user_number, int(message.timestamp), cfg['CONFIG']['DB_FILE'])
            return cfg['SALES_CS']['GREETING']            

        #abaikan msg group ini, kecuali panjang.
        if (conv_obj.need_group_prefix) and (message.author != '') and ( nama_bot != awalan ):
            #kecuali postingan panjang.
            if len(message.text.lower().split(" ")) > 25:
                print(f'{Fore.RED}{Back.WHITE}LONG POSTING DETECTED!.. i will comment{Fore.RESET}{Back.RESET}')
                preprompt = f"Maya berikan jawaban berupa komentar baik dan pendek pada postingan ini. Jangan gunakan hashtag dalam jawaban.\n\n"
                try:
                    result = await api.ask_gpt(self, conv_obj, f'{preprompt}{message.text}')
                    return result
                except:
                    return None
            return None

        #potong awalan
        if awalan == nama_bot:
            message.text = message.text[len(conv_obj.bot_name):].strip()

        #ignore looping error admin notif send
        if message.text.lower().startswith("ada error") or message.text.lower().startswith("konfirmasi signal"):
            return None

        
        # PRA PROCESSING MESSAGE - buang aja karakter unicode dan quote
        message.text = str(message.text)
        message.text = message.text.encode('ascii', errors='ignore').decode()
        message.text = message.text.replace("'"," ").replace('"',' ')


        print("-------------------------------------------------")
        print(f"{Fore.GREEN}{Style.BRIGHT}Message:",message)
        print(f"{Style.RESET_ALL}-------------------------------------------------")

        #TODO: Please to be removed or changed
        human_say = "HUMAN: "+message.text
        dbo.insert_conv(conv_obj.user_number, conv_obj.bot_number, int(message.timestamp), human_say, self.db_file)

        # on maintenance
        if self.on_maintenance and not self.is_admin(message):
            print(f"{Fore.RED}{Back.WHITE}Called.. But ON MAINTENANCE NOW{Fore.WHITE}{Back.BLACK}")
            return "*BRB* - Be Right Back .. ZzzZzz ZZzzzz.."

        if conv_obj.persona == Persona.SALES_CS:
            return cs.info_cs(conv_obj=conv_obj, query=message.text)

        if conv_obj.free_gpt:
            return await friend.run(self, conv_obj, message)

        if conv_obj.convtype == ConvType.ADMIN:
            return await admin.run(self, conv_obj, message.text) 

        if conv_obj.convtype == ConvType.PLATINUM:
            return await platinum.run(self, conv_obj, message)

        if conv_obj.convtype == ConvType.GOLD:
            return await gold.run(self, conv_obj, message)

        if conv_obj.convtype == ConvType.FRIEND:
            return await friend.run(self, conv_obj, message)

        if conv_obj.convtype == ConvType.DEMO:
            return await demo.run(self, conv_obj, message)

        # PROCESS BY PERSONA AND MODE
        if conv_obj.convmode == ConvMode.YESNO:
            if "y" in message.text.lower():
                return "Kamu menjawab ya"
            if "t" in message.text.lower():
                return "Kamu menjawab tidak"

        if conv_obj.convmode == ConvMode.ASK:
            if "ok" in message.text.lower():
                return "oke juga"


        # JUST RETURN IT
        return "pfft..."

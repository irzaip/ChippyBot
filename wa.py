from fastapi import FastAPI
import logging
from conversations import Message, BotQuestion, ConvMode, Script
from conversations import MessageContent, Conversation, MsgProcessor
import requests, os, openai, random, time
from typing import List
import asyncio
import nest_asyncio


CONFIG = {}
CONFIG['logdir'] = './log/'
TOKEN_LIMIT = 1000
BOT_NUMBER = "6285775300227@c.us"
ADMIN_NUMBER = "62895352277562@c.us"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=CONFIG['logdir'] + 'wa.log'
)

app = FastAPI()
conversations = {}
whatsapp_web_url = "http://localhost:8000/send" # Replace with your endpoint URL
nest_asyncio.apply()

def notify_admin(message: str):
    send_to_phone(ADMIN_NUMBER, BOT_NUMBER, message)

def no_process(conv_obj: Conversation, prompt: str) -> str:
    return prompt
 
def send_to_phone(user_number: str, bot_number: str, message: str) -> None:
    """send langsung ke WA, tapi ke *user_number*, bukan ke bot_number"""
    message = {
        "message": message, # Replace with your message text
        "from": bot_number, # Replace with the sender number
        "to": user_number # Replace with out bot number
    }

    response = requests.post(whatsapp_web_url, json=message)

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Error sending message. Status code: {response.status_code}")
        print(response.text)


def reformat_phone(text: str) -> str:
    """Ambil hanya nomor telfon saja, tanpa ending @c.us"""
    return 'user'+ str(text.split("@")[0])

def add_conversation(user_number:str, bot_number: str, message: str) -> None:
    """create new conversation object"""
    conversations.update({user_number : Conversation(user_number, bot_number)})


def save_log(user_number: str) -> None:
    """cari object di conversations dict lalu save jadi log file"""
    if user_number not in conversations:
        return print(f"Conversation dengan {user_number} tidak ada")
    dir = CONFIG['logdir']
    filepath = str(user_number) + ".log"
          
    # Create the log directory if it doesn't exist
    if not os.path.exists(dir):
        os.makedirs(dir)

    # Write to the log file
    try:
        with open(dir + filepath, "a") as f:
            for i in conversations[user_number].messages:
                f.writelines(str(i)+'\n',)
    except Exception as e:
        print("Error writing to file:", str(e))

def return_brb() -> str:
    alasan = ["ada tamu.","angkat jemuran.", "karet kendor.", "kasih makan kucing", "ada tamu dateng.", "atep bolong.", "ada kebocoran.", "ada radiasi radioaktif."]
    message = "*BRB* - be right back, " + random.choice(alasan)
    return message

# Fungsi untuk memulai menjalankan setiap coroutine pada setiap objek
async def start_coroutines():
    coroutines = [obj.start_coroutine() for obj in conversations.values()]
    await asyncio.gather(*coroutines)

# Jalankan coroutines di background menggunakan event loop
async def start_background_tasks():
    loop = asyncio.get_running_loop()
    tasks = [loop.create_task(start_coroutines())]
    await asyncio.gather(*tasks)


@app.post("/messages")
async def receive_message(message: Message):
    """Terima pesan dari WA"""
    if (message.author != '') and (message.text[0:3].lower() != 'gpt'):
        return None
    
    #kalau ada depan gpt. buang.
    if (message.text[0:3].lower() == 'gpt'):
        message.text = message.text[3:]

    #buang aja karakter unicode
    message.text = message.text.encode('ascii', errors='ignore').decode()
    print("-------------------------------------------------")
    print("Message:",message)
    print("-------------------------------------------------")

    if message.type == 'chat':
        #response_text = f"You received a message from {message.user_number}: {message.text}"
        if message.user_number not in conversations:
            conversations.update({message.user_number : Conversation(message.user_number, message.bot_number)})

        #pass conversation object to process
        conversation_obj = conversations[message.user_number]

        try:
            #response_text = process_msg(conversation_obj, message.text)
            Proc_obj = MsgProcessor(conversation_obj)
            response_text = Proc_obj.run(message.text)
        except Exception as err:
            print(">>>>>>>>>>>>>>>> ERROR : " + f"{str(err)}<<<<<<<<<<<<<<<<<<<<<")
            notify_admin(f"Ada error {str(err)}nih!")
            return {"message" : return_brb()}
                
        # logging.debug("Returned response: " + str(response_text))
        return {"message": str(response_text)}
    else:
        logging.error("Not Chat Type")
        return return_brb()

@app.get("/print_messages/{user_number}")
async def print_messages(user_number: str) -> str:
    """Keluarkan log percakapan dengan nomor tertentu"""
    if user_number in conversations:
        return {"messages" : str(conversations[user_number].messages)}
    else:
        logging.error(f"save_log error finding user_number: {str(user_number)}")

@app.get("/save_logs")
async def save_logs():
    """save semua logs conversation ke dalam file log"""
    for i in conversations.keys():
        try:
            save_log(i)
            return {"save":"done"}
        except:
            logging.error("Error saving logs")

@app.post("/set_content")
async def set_content(message_content: MessageContent):
    "Inject conversation ke dalam object Conversation"
    roles = {
        'SYSTEM': 'reset_system',
        'USER': 'add_role_user',
        'ASSISTANT': 'add_role_assistant'
    }
    content = message_content.message

    if message_content.user_number not in conversations:
        add_conversation(message_content.user_number, message_content.bot_number, content)

    usr_num = str(conversations[message_content.user_number]) 
    getattr(conversations[message_content.user_number], roles[message_content.role] )(content)
    logging.debug(f"Inject:{message_content.role}:{content} to {message_content.user_number}")


@app.put('/botquestion/{user_number}')
async def put_botquestion(user_number: str, botquestion: List[BotQuestion]):
    # Menambahkan data yang diterima ke dalam list

    if user_number not in conversations:
        conv_obj = conversations.update({user_number : Conversation(user_number, BOT_NUMBER)})

    conv_obj = conversations[user_number]
    conv_obj.botquestions.extend(botquestion)
    return {'message': 'Data berhasil ditambahkan!'}

@app.get('/convmode/{user_number}/{convmode}')
async def convmode(user_number: str, convmode: ConvMode):
    if user_number not in conversations: 
        return {'detail' : 'user dont exist'}
    conversations[user_number].mode = convmode
    return {'detail' : f'set to {convmode}'}

@app.get('/botq/{user_number}')
async def get_botq(user_number: str):    
    return {'message': str(conversations[user_number].botquestions) }

@app.get('/getmode/{user_number}')
async def getmode(user_number: str):    
    return {'message': str(conversations[user_number].mode) }

@app.get('/run_question/{user_number}/{id}')
async def run_question(user_number: str, id: int = 1):
    if user_number not in conversations:
        return {'message' : 'user not exist'}
    conv = conversations[user_number]
    send_to_phone(user_number, BOT_NUMBER, conv.botquestions[id].question)
    return {'message' : 'done'}

@app.get('/start_question/{user_number}')
async def start_question(user_number: str):
    if user_number not in conversations:
        return {'message' : 'user not exist'}
    conv = conversations[user_number]
    conv.mode = ConvMode.ASK
    send_to_phone(user_number, BOT_NUMBER, conv.intro_msg)
    send_to_phone(user_number, BOT_NUMBER, conv.botquestions[0].question)
    return {'message' : 'done'}



@app.get('/set_script/{user_number}/{script}')
async def set_script(user_number: str, script: Script):
    if user_number not in conversations:
        {'detail' : 'user dont exist'}
    print(script)
    conversations[user_number].set_script(script)
    return {'message' : f"set to {script}"}


# Endpoint untuk merubah interval pada objek tertentu
@app.put("/interval/{user_number}/{interval}")
async def change_interval(user_number: str, interval: int):
    if user_number not in conversations:
        return {"message" : "user does not exist"}
    obj = conversations[user_number]
    obj.interval = interval
    return {"message": f"sudah di set menjadi {interval}"}


# Endpoint untuk memulai menjalankan method pada setiap objek
@app.get("/call_method")
async def start_method_call():
    await start_background_tasks()
    return {"message": "Method dijalankan pada setiap objek."}


@app.get("/botquestions/{user_number}")
async def botquestions(user_number: str):
    """check seluruh tanya-jawab di object conversation milik user"""
    if user_number not in conversations:
        return {'message' : 'user not found'}
    
    result = ""
    for id,item in enumerate(conversations[user_number].botquestions):
        result = result + f"{item.question}:{item.answer}\n"
    return {'message' : result}

@app.get("/obj_info/{user_number}")
async def obj_info(user_number: str):
    """Return the object in all conversation"""
    if user_number not in conversations:
        return {'message' : 'user does not exist'}
    conv = conversations[user_number]
    result = { 'botquestions' : conv.botquestions, 
              'interval' : conv.interval,
              'mode' : conv.mode,
              'wait_time' : conv.wait_time,
              'max_token' : conv.MAX_TOKEN,
              'word_limit' : conv.WORD_LIMIT,
              'temperature' : conv.temperature,
             }
    return {'message' : result}

@app.put("/set_interview/{user_number}")
async def set_interview(user_number: str, intro: str, outro: str):
    if user_number not in conversations:
        return {'message' : 'user does not exist'}
    conversations[user_number].intro_msg = intro
    conversations[user_number].outro_msg = outro
    return {'mesage' : 'done set intro and outro'}

@app.get("/ping")
async def ping():
    return {"message" : "pong"}


start_background_tasks()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8998)


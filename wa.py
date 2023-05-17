from fastapi import FastAPI
from conversations import Message, BotQuestion, ConvMode, Script
from conversations import MessageContent, Conversation, Persona
from Msgproc import MsgProcessor
import requests, os, random, sys
from typing import List, Union
import asyncio
import nest_asyncio
import random, string
import logging
from db_oper import new_db_connection, update_db_connection, get_db_all_connection, get_db_connection
import toml

cfg = toml.load('config.toml')

CONFIG = {}

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=cfg['CONFIG']['LOGDIR'] + 'wa.log'
)

app = FastAPI()
conversations = {}
result = get_db_all_connection('cipibot.db')

def add_conversation(user_number:str, bot_number: str) -> None:
    """create new conversation object"""    
    conversations.update({user_number : Conversation(user_number, bot_number)})
    result = get_db_connection(user_number=user_number, bot_number=bot_number, db_name='cipibot.db') 
    if not result:
        new_db_connection(user_number=user_number, bot_number=bot_number, result=conversations[user_number].get_params(), db_name='cipibot.db')


for i in result:
    add_conversation(i[0],i[1])
for i in result:
    conversations[i[0]].put_params(i[2])

whatsapp_web_url = "http://localhost:8000/send" # Replace with your endpoint URL
nest_asyncio.apply()

if sys.version_info < (3, 10):
    print("Tak bisa jalan di python < 3.10")
    sys.exit()

def notify_admin(message: str) -> None:
    send_to_phone(cfg['CONFIG']['ADMIN_NUMBER'], cfg['CONFIG']['BOT_NUMBER'], message)

def generate_filename() -> str:
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(10))
 
def send_to_phone(user_number: str, bot_number: str, message: str) -> None:
    """send langsung ke WA, tapi ke *user_number*, bukan ke bot_number"""
    message = {
        "message": message, # Replace with your message text
        "from": bot_number, # Replace with the sender number
        "to": user_number # Replace with out bot number
    } # type: ignore

    response = requests.post(whatsapp_web_url, json=message)

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Error sending message. Status code: {response.status_code}")
        print(response.text)


def reformat_phone(text: str) -> str:
    """Ambil hanya nomor telfon saja, tanpa ending @c.us"""
    return 'user'+ str(text.split("@")[0])


def save_log(user_number: str) -> None:
    """cari object di conversations dict lalu save jadi log file"""
    if user_number not in conversations:
        return print(f"Conversation dengan {user_number} tidak ada")
    dir = cfg['CONFIG']['LOGDIR']
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
async def start_coroutines() -> None:
    coroutines = [obj.start_coroutine() for obj in conversations.values()]
    await asyncio.gather(*coroutines)

# Jalankan coroutines di background menggunakan event loop
async def start_background_tasks() -> None:
    loop = asyncio.get_running_loop()
    tasks = [loop.create_task(start_coroutines())]
    await asyncio.gather(*tasks)

@app.put("/set_bot_name/{user_number}/{bot_name}")
async def set_bot_name(user_number: str, bot_name: str) -> Union[dict, dict, None]:
    if user_number not in conversations:
        return {'message':'user dont exist'}
    try:
        conversations[user_number].set_bot_name(bot_name)
    except Exception as e:
        return {'message' : e}
    return {'message': 'done'}


@app.post("/messages")
async def receive_message(message: Message) -> dict[str, str] | str:
    """Fungsi terpenting menerima pesan dari WA web"""
    if message.user_number not in conversations:
        add_conversation(user_number=message.user_number, bot_number=message.bot_number)
    
    if message.type == 'chat':
        #response_text = f"You received a message from {message.user_number}: {message.text}"
        if message.user_number not in conversations:
            conversations.update({message.user_number : Conversation(message.user_number, message.bot_number)})

        #pass conversation object to process
        conversation_obj = conversations[message.user_number]
        if message.notifyName:
            conversation_obj.user_name = message.notifyName

        try:
            #response_text = process_msg(conversation_obj, message.text)
            Proc_obj = MsgProcessor(conversation_obj, 'cipibot.db')
            response_text = Proc_obj.process(message)
            if response_text == None:
                return {'data': 'none'}
        except Exception as err:
            print(">>>>>>>>>>>>>>>> ERROR : " + f"{str(err)}<<<<<<<<<<<<<<<<<<<<<")
            notify_admin(f"Ada error {str(err)}nih!")
            return {"message" : return_brb()}

        update_db_connection(user_number=message.user_number, bot_number=message.bot_number, result=conversation_obj.get_params(), db_name='cipibot.db')
        # logging.debug("Returned response: " + str(response_text))
        return {"message": str(response_text)}
    else:
        logging.error("Not Chat Type")
        return return_brb()

@app.get("/print_messages/{user_number}")
async def print_messages(user_number: str) -> str: # type: ignore
    """Keluarkan log percakapan dengan nomor tertentu"""
    if user_number in conversations:
        return {"messages" : str(conversations[user_number].messages)} # type: ignore
    else:
        logging.error(f"save_log error finding user_number: {str(user_number)}")

@app.get("/save_logs")
async def save_logs() -> dict[str, str] | None:
    """save semua logs conversation ke dalam file log"""
    for i in conversations.keys():
        try:
            save_log(i)
            return {"save":"done"}
        except:
            logging.error("Error saving logs")

@app.post("/set_content")
async def set_content(message_content: MessageContent) -> dict[str, str]:
    "Inject conversation ke dalam object Conversation"
    roles = {
        'SYSTEM': 'reset_system',
        'USER': 'add_role_user',
        'ASSISTANT': 'add_role_assistant'
    }
    content = message_content.message

    if message_content.user_number not in conversations:
        add_conversation(message_content.user_number, message_content.bot_number)

    getattr(conversations[message_content.user_number], roles[message_content.role] )(content)
    logging.debug(f"Inject:{message_content.role}:{content} to {message_content.user_number}")
    return {'message': 'Done'}

@app.put('/create_conv/{user_number}/{bot_number}')
async def create_conv(user_number: str, bot_number: str) -> dict[str, str]:
    if user_number not in conversations:
        add_conversation(user_number, bot_number)
        return {'message': 'done creation'}
    return {'message': "already exist"}

@app.put('/botquestion/{user_number}')
async def put_botquestion(user_number: str, botquestion: List[BotQuestion]) -> dict[str, str]:
    # Menambahkan data yang diterima ke dalam list

    if user_number not in conversations:
        conv_obj = conversations.update({user_number : Conversation(user_number, cfg['CONFIG']['BOT_NUMBER'])})

    conv_obj = conversations[user_number]
    conv_obj.botquestions.extend(botquestion)
    return {'message': 'Data berhasil ditambahkan!'}

@app.put('/set_mode/{user_number}/{convmode}')
async def set_mode(user_number: str, convmode: ConvMode) -> dict[str, str]:
    if user_number not in conversations: 
        return {'detail' : 'user dont exist'}
    conversations[user_number].set_mode(convmode)
    return {'detail' : f'set to {convmode}'}

@app.get('/botq/{user_number}')
async def get_botq(user_number: str) -> dict[str, str]:    
    return {'message': str(conversations[user_number].botquestions) }

@app.get('/getmode/{user_number}')
async def getmode(user_number: str) -> dict[str, str]:    
    return {'message': str(conversations[user_number].mode) }

@app.get('/run_question/{user_number}/{id}')
async def run_question(user_number: str, id: int = 1) -> dict[str, str]:
    if user_number not in conversations:
        return {'message' : 'user not exist'}
    conv = conversations[user_number]
    send_to_phone(user_number, cfg['CONFIG']['BOT_NUMBER'], conv.botquestions[id].question)
    return {'message' : 'done'}

@app.get('/start_question/{user_number}')
async def start_question(user_number: str) -> dict[str, str]:
    if user_number not in conversations:
        return {'message' : 'user not exist'}
    conv = conversations[user_number]
    conv.mode = ConvMode.ASK
    send_to_phone(user_number, cfg['CONFIG']['BOT_NUMBER'], conv.intro_msg)
    send_to_phone(user_number, cfg['CONFIG']['BOT_NUMBER'], conv.botquestions[0].question)
    conv.question_asked = conv.botquestions[0].question
    return {'message' : 'done'}


@app.get('/set_script/{user_number}/{script}')
async def set_script(user_number: str, script: Script) -> dict[str, str]:
    """Merubah macam-macam script mukakmu lah."""
    if user_number not in conversations:
        return {'detail' : 'user dont exist'}
    conversations[user_number].set_script(script)
    return {'message' : f"set to {script}"}

@app.get('/reset_botquestions/{user_number}')
async def reset_botquestion(user_number: str) -> dict[str, str]:
    if user_number not in conversations:
        return {'detail' : 'user dont exist'}
    conversations[user_number].reset_botquestions()
    return {'message' : 'reset done'}


# Endpoint untuk merubah interval pada objek tertentu
@app.put("/set_interval/{user_number}/{interval}")
async def change_interval(user_number: str, interval: int) -> dict[str, str]:
    if user_number not in conversations:
        return {"message" : "user does not exist"}
    conversations[user_number].set_interval(interval)
    return {"message": f"sudah di set menjadi {interval}"}


# Endpoint untuk memulai menjalankan method pada setiap objek
@app.get("/call_method")
async def start_method_call() -> dict[str, str]:
    await start_background_tasks()
    return {"message": "Method dijalankan pada setiap objek."}


@app.get("/botquestions/{user_number}")
async def botquestions(user_number: str) -> dict[str, str]:
    """check seluruh tanya-jawab di object conversation milik user"""
    if user_number not in conversations:
        return {'message' : 'user not found'}
    
    result = ""
    for id,item in enumerate(conversations[user_number].botquestions):
        result = result + f"{item.question}:{item.answer}\n"
    return {'message' : result}

@app.put("/set_persona/{user_number}/{persona}")
async def set_persona(user_number: str, persona: Persona) -> dict[str, str]:
    if user_number not in conversations:
        return {'message': 'user not found'}
    
    conversations[user_number].set_persona(persona)
    return {'message' : f'set to {persona}'}


@app.get("/obj_info/{user_number}")
async def obj_info(user_number: str) -> Union[dict, dict, None]:
    """Return the object in all conversation"""
    if user_number not in conversations:
        return {'message' : 'user does not exist'}
    conv = conversations[user_number]
    result = {'messages' : conv.messages, 
              'botquestions' : conv.botquestions, 
              'question_asked' : conv.question_asked,
              'interval' : conv.interval,
              'mode' : conv.mode,
              'wait_time' : conv.wait_time,
              'max_token' : cfg['CONFIG']['MAX_TOKEN'],
              'word_limit' : conv.WORD_LIMIT,
              'temperature' : conv.temperature,
             }
    return {'message' : result}

@app.put("/set_interview/{user_number}")
async def set_interview(user_number: str, data: dict) -> dict[str, str]:
    if user_number not in conversations:
        return {'message' : 'user does not exist'}
    conversations[user_number].set_intro_msg(data['intro_msg'])
    conversations[user_number].set_outro_msg(data['outro_msg'])
    return {'mesage' : 'done set intro and outro'}

@app.get('/test_send/{user_number}')
async def test_send(user_number: str)-> dict:
    if user_number not in conversations:
        return {'message' : 'user does not exist'}
    response = await conversations[user_number].send_msg("Hello")
    if response.ok:
        return {'message' : response.text}
    else:
        return {'message' : 'error sending test'}

@app.get("/ping")
async def ping() -> dict[str, str]:
    return {"message" : "pong"}

@app.get("/list_conversations")
async def list_conversations() -> dict:
    list_conv = []
    all_conv = list(conversations.keys())
    print(all_conv)
    for i in all_conv:
        item = f"{conversations[i].user_number}###{conversations[i].user_name}" 
        list_conv.append(item)
        
    return {'message' : list_conv}

    
    
#start_background_tasks()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8998)


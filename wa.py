from fastapi import FastAPI
import logging
from conversations import Role, Message, InjectedMessage, MessageContent, Conversation, BotQuestion, ConvMode
import requests, os, openai, random, time, nltk
from typing import List


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
all_conversation = {}
whatsapp_web_url = "http://localhost:8000/send" # Replace with your endpoint URL


def notify_admin(message):
    send_to_phone(ADMIN_NUMBER, BOT_NUMBER, message)
    

    

def ask_gpt(conv_obj: Conversation, prompt: str) -> str:
    """
    Akses API ke OpenAI, dari prompt menjadi hasil string
    
    input: masuknya list dari Object Conversation.messages
    """
    # cek panjang conversation, potong setengah bila lebih dari TOKEN_LIMIT

    conv_obj.messages.append({"role" : "user", "content" : prompt})
    print("WORD COUNTS:--------------------------> ", conv_obj.count_words(conv_obj.messages))

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
 
def send_to_phone(user_number, bot_number, message) -> None:
    """send langsung ke WA, tapi ke *user_number*, bukan ke bot_number"""
    message = {
        "message": message, # Replace with your message text
        "from": user_number, # Replace with the sender number
        "to": bot_number # Replace with out bot number
    }

    response = requests.post(whatsapp_web_url, json=message)

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Error sending message. Status code: {response.status_code}")
        print(response.text)


def reformat_phone(text) -> str:
    """Ambil hanya nomor telfon saja, tanpa ending @c.us"""
    return 'user'+ str(text.split("@")[0])

def add_conversation(user_number, bot_number, message) -> None:
    """create new conversation object"""
    all_conversation.update({user_number : Conversation(user_number, bot_number, message)})

def intervent():
    return True

def process_msg(conversation_obj: Conversation, message) -> str:
    """Buat action untuk object Conversation -> buat object apabila belum ada"""

    if conversation_obj.mode == ConvMode.ASK:
        print("***************ASK*************************")

    reply = conversation_obj.rivereply(message)
    print("MY REPLY: ----> ",reply)
    if reply == "BBB":
        return getattr(conversation_obj, 'process')(ask_gpt,conversation_obj, message)
    else:
        return reply

def save_log(user_number):
    """cari object di all_conversation dict lalu save jadi log file"""
    if user_number not in all_conversation:
        return print(f"Conversation dengan {user_number} tidak ada")
    dir = CONFIG['logdir']
    filepath = str(user_number) + ".log"
          
    # Create the log directory if it doesn't exist
    if not os.path.exists(dir):
        os.makedirs(dir)

    # Write to the log file
    try:
        with open(dir + filepath, "a") as f:
            for i in all_conversation[user_number].messages:
                f.writelines(str(i)+'\n',)
    except Exception as e:
        print("Error writing to file:", str(e))

def return_brb():
    alasan = ["ada tamu.","angkat jemuran.", "karet kendor.", "kasih makan kucing", "ada tamu dateng.", "atep bolong.", "ada kebocoran.", "ada radiasi radioaktif."]
    message = "*BRB* - be right back, " + random.choice(alasan)
    return message

@app.post("/messages")
async def receive_message(message: Message):
    """Terima pesan dari WA"""
    if (message.author != '') and (message.text[0:3].lower() != 'gpt'):
        return None
    
    #kalau ada depan gpt. buant.
    if (message.text[0:3].lower() == 'gpt'):
        message.text = message.text[3:]

    #buang aja karakter unicode
    message.text = message.text.encode('ascii', errors='ignore').decode()
    print("-------------------------------------------------")
    print("Message:",message)
    print("-------------------------------------------------")

    if message.type == 'chat':
        #response_text = f"You received a message from {message.user_number}: {message.text}"
        if message.user_number not in all_conversation:
            all_conversation.update({message.user_number : Conversation(message.user_number, message.bot_number, message)})

        #pass conversation object to process
        conversation_obj = all_conversation[message.user_number]
        try:
            response_text = process_msg(conversation_obj, message.text)
        except Exception as err:
            print(">>>>>>>>>>>>>>>> ERROR : " + f"{str(type(err))}<<<<<<<<<<<<<<<<<<<<<")
            notify_admin(f"Ada error {str(type(err))}nih!")
        
        # logging.debug("Returned response: " + str(response_text))
        return {"message": str(response_text)}
    else:
        logging.error("Not Chat Type")
        return return_brb()

@app.get("/print_messages/{user_number}")
async def print_messages(user_number):
    """Keluarkan log percakapan dengan nomor tertentu"""
    if user_number in all_conversation:
        return {"messages" : str(all_conversation[user_number].messages)}
    else:
        logging.error(f"save_log error finding user_number: {str(user_number)}")

@app.get("/save_logs")
async def save_logs():
    """save semua logs conversation ke dalam file log"""
    for i in all_conversation.keys():
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

    if message_content.user_number not in all_conversation:
        add_conversation(message_content.user_number, message_content.bot_number, content)

    usr_num = str(all_conversation[message_content.user_number]) 
    getattr(all_conversation[message_content.user_number], roles[message_content.role] )(content)
    logging.debug(f"Inject:{message_content.role}:{content} to {message_content.user_number}")


@app.put('/botquestion/{user_number}')
async def put_botquestion(user_number, botquestion: List[BotQuestion]):
    # Menambahkan data yang diterima ke dalam list

    if user_number not in all_conversation:
        conv_obj = all_conversation.update({user_number : Conversation(user_number, BOT_NUMBER , "")})

    conv_obj = all_conversation[user_number]
    conv_obj.botquestions.extend(botquestion)
    return {'message': 'Data berhasil ditambahkan!'}

@app.get('/convmode/{user_number}/{convmode}')
async def convmode(user_number, convmode: ConvMode):
    if user_number not in all_conversation: 
        return {'detail' : 'user dont exist'}
    all_conversation[user_number].mode = convmode
    return {'detail' : f'set to {convmode}'}

@app.get('/botq/{user_number}')
async def get_botq(user_number):    
    return {'message': str(all_conversation[user_number].botquestions) }

@app.get('/getmode/{user_number}')
async def getmode(user_number):    
    return {'message': str(all_conversation[user_number].mode) }

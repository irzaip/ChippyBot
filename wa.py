from fastapi import FastAPI
import logging
from conversations import Role, Message, InjectedMessage, MessageContent, Conversation
import requests, os, openai, random, time, nltk

CONFIG = {}
CONFIG['logdir'] = './log/'
TOKEN_LIMIT = 1800

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
    pass

def count_words(messages: list) -> int:
    "Menghitung kata dalam iterasi sebuah value dict"
    words = []
    for i in messages:
        words.extend(nltk.word_tokenize(i['content']))
    return len(words)

def reduce_conversation(messages: list) -> list:
    """memotong conversation menjadi setengah percakapan"""
    print(len(messages))
    for i in messages:
        print(i['content'])
    half_way = int(len(messages) / 2 + 1)
    messages = messages[:1] + messages[half_way:]
    return messages
    

def ask_gpt(messages: list, prompt: str) -> str:
    """
    Akses API ke OpenAI, dari prompt menjadi hasil string
    
    input: masuknya list dari Object Conversation.messages
    """
    # cek panjang conversation, potong setengah bila lebih dari TOKEN_LIMIT
    print("WORD COUNTS:--------------------------> ", count_words(messages))
    if count_words(messages) > TOKEN_LIMIT:
        messages = reduce_conversation(messages)
        logging.debug
        ('conversation-trunctate the message')

    messages.append({"role" : "user", "content" : prompt})

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages,
     max_tokens=2000,
#      n=1,
#      stop=None,
#      temperature=0.7,
    )

    try:
        message = response.choices[0].message.content
    except:
        alasan = ["ada tamu.","angkat jemuran.", "karet kendor.", "kasih makan kucing", "ada tamu dateng.", "atep bolong.", "ada kebocoran.", "ada radiasi radioaktif."]
        message = "*BRB* - be right back," + random.choice(alasan)
        notify_admin("Error access GPT")

    messages.append({"role" : "assistant", "content" : message})
    time.sleep(random.randint(2,7))
    return message
 
def send_to_phone(to_number, from_number, message) -> None:
    """send langsung ke WA, tapi ke *user_number*, bukan ke bot_number"""
    message = {
        "message": message, # Replace with your message text
        "from": from_number, # Replace with the sender number
        "to": to_number # Replace with out bot number
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

def process_msg(conversation_obj: Conversation, message, **kwargs) -> str:
    """Buat action untuk object Conversation -> buat object apabila belum ada"""
    if 'action' in kwargs:
        messages=all_conversation[conversation_obj.user_number].messages
        return all_conversation[conversation_obj.user_number].process(kwargs['action'],messages, message)


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


@app.post("/messages")
async def receive_message(message: Message):
    """Terima pesan dari WA"""
    print("Message:",message)
    if message.type == 'chat':
        #response_text = f"You received a message from {message.user_number}: {message.text}"
        if message.user_number not in all_conversation:
            all_conversation.update({message.user_number : Conversation(message.user_number, message.bot_number, message)})

        #pass conversation object to process
        conversation_obj = all_conversation[message.user_number]
        response_text = process_msg(conversation_obj, message.text, action=ask_gpt)
        logging.debug("Returned response: " + str(response_text))
        return {"message": str(response_text)}
    else:
        logging.error("Not Chat Type")
        return {"message" : "uncompatible"}

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



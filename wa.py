from fastapi import FastAPI
from pydantic import BaseModel
from test_program.grad_io import *
import logging
from conversations import Conversation

CONFIG = {}
CONFIG['logdir'] = './log/'

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=CONFIG['logdir'] + 'wa.log'
)

app = FastAPI()
all_conversation = {}

class Message(BaseModel):
    text: str
    from_number: str
    to_number: str
    timestamp: int
    notifyName: str = ""
    type: str
    client: str

def get_number_only(text: str) -> str:
    try:
        return text.split("@")[0]
    except:
        return text


def reformat_phone(text):
    return 'user'+ str(text.split("@")[0])

def process(from_number, to_number, message, **kwargs):
    """Buat action untuk object Conversation -> buat object apabila belum ada"""
    if from_number not in all_conversation:
        all_conversation.update({from_number : Conversation(from_number, to_number, message)})
    if 'action' in kwargs:
        return all_conversation[from_number].process(kwargs['action'], message)
    
def add_convo(from_number, to_number, message):
    all_conversation.update({from_number : Conversation(from_number, to_number, message)})

def save_log(from_number):
    """
    cari object di all_conversation dict lalu save jadi log file
    
    """
    if from_number not in all_conversation:
        return print(f"Conversation dengan {from_number} tidak ada")
    dir = CONFIG['logdir']
    filepath = str(from_number) + ".log"
    
        
    # Create the log directory if it doesn't exist
    if not os.path.exists(dir):
        os.makedirs(dir)

    # Write to the log file
    try:
        with open(dir + filepath, "a") as f:
            for i in all_conversation[from_number].messages:
                f.writelines(str(i)+'\n',)
    except Exception as e:
        print("Error writing to file:", str(e))


@app.post("/messages")
async def receive_message(message: Message):
    print("Message:",message)
    if message.type == 'chat':
        #response_text = f"You received a message from {get_number_only(message.from_number)}: {message.text}"
        response_text = process(message.from_number, message.to_number, message.text, action=ask_gpt)
        logging.debug("Returned response: " + response_text)
        return {"message": str(response_text)}
    else:
        logging.error("Not Chat Type")
        return {"message" : "uncompatible"}

@app.get("/print_messages/{from_number}")
async def print_messages(from_number):
    if from_number in all_conversation:
        return {"messages" : str(all_conversation[from_number].messages)}
    else:
        logging.error(f"save_log error finding from_number: {str(from_number)}")

@app.get("/save_logs")
async def save_logs():
    for i in all_conversation.keys():
        try:
            save_log(i)
        except:
            logging.error("Error saving logs")
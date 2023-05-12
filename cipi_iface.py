from abc import ABC, abstractmethod
from dataclasses import dataclass
from string import Template
import os
import requests
import ast
from conversations import BotQuestion, ConvMode, Script, Persona, Role
import json
from typing import List
import pprint


server_address = 'http://127.0.0.1:8998'
BOT_NUMBER = "6285775300227@c.us"

def create_conv(user_number, bot_number):
    response = requests.put(f'{server_address}/create_conv/{user_number}/{bot_number}')
    if response.ok:
        return response.text
    else:
        return "Error create conversation"
                            
def set_bot_name(user_number, bot_name: str):
    url = f'{server_address}/set_bot_name/{user_number}/{bot_name}'
    response = requests.put(url)
    if response.ok:
        return {'message' : 'done'}
    else:
        return {'message' : response}

def set_mode(user_number: str, convmode: ConvMode):
    response = requests.put(f'{server_address}/set_convmode/{user_number}/{convmode}')
    
    if response.ok:
        return response.text
    else:
        return "Error creating setting ConvMode"

def set_interval(user_number: str, interval: int):
    response = requests.put(f'{server_address}/set_interval/{user_number}/{interval}')
    if response.ok:
        return response.text
    else:
        return "Error Change Interval"

def set_persona(user_number: str, persona: Persona):
    response = requests.put(f'{server_address}/set_persona/{user_number}/{persona}')
    
    if response.ok:
        return response.text
    else:
        return "Error creating setting Persona"

def set_message(user_number, message, role: Role):
    """setting system, user, assistant message buat openai"""
    url = f"{server_address}/set_content" # Replace with your endpoint URL
    message = {
        "user_number": user_number, # Replace with the sender number
        "bot_number": BOT_NUMBER, # Replace with the recipient number in WhatsApp format
        "message": message,
        "role": role.name,
    }

    response = requests.post(url, json=message)
    if response.ok:
        print(response.text)
    else:
        print(f"Error sending message. Status code: {response.status_code}")

def set_script(user_number: str, script: Script):
    response = requests.put(f'{server_address}/set_script/{user_number}/{script}')
    if response.ok:
        return response.text
    else:
        return "Error creating Script"

def start_question(user_number: str):
    response = requests.get(f'{server_address}/start_question/{user_number}')
    if response.ok:
        return response.text
    else:
        return "Error Starting Questions"

def set_interview(user_number: str, intro_msg: str, outro_msg: str):
    data = {'intro_msg':intro_msg, 'outro_msg': outro_msg}
    response = requests.put(f'{server_address}/set_interview/{user_number}', json=data)
    if response.ok:
        return {'message': 'ok'}
    else:
        return {'message': 'error updating intro outro'}


def obj_info(user_number: str):
    response = requests.get(f'{server_address}/obj_info/{user_number}').json()
    return response

def make_botquestion(user_number, all_question: dict) -> List[BotQuestion]:
    result = []
    for key,value in all_question.items():
        result.append(BotQuestion(id=key, question=value))

    # Mengirim data melalui REST API
    url = f'{server_address}/botquestion/{user_number}'
    headers = {'Content-type': 'application/json'}
    data = json.dumps([{'id': b.id, 
                        'question': b.question, 
                        'answer': b.answer, 
                        'multiplier': b.multiplier, 
                        'score': b.score} for b in result])
    print(data)
    response = requests.put(url, headers=headers, data=data)

    # Menampilkan respons dari server
    if response.status_code == 200:
        print('Data berhasil dikirim!')
    else:
        print('Terjadi kesalahan saat mengirim data.')



def getmode(user_number: str):
    response = requests.get(f'{server_address}/getmode/{user_number}')
    if response.status_code == 200:
        return response.text
    else:
        return "Error Get Mode"

def run_question(user_number: str, question: int):
    response = requests.get(f'{server_address}/run_question/{user_number}/{question}')
    if response.status_code == 200:
        return response.text
    else:
        return f"Error running question no {question}"

def botq(user_number: str):
    response = requests.get(f'{server_address}/botq/{user_number}')
    if response.status_code == 200:
        return response.text
    else:
        return f"Error running botq"


def reset_botquestions(user_number):
    url = f'{server_address}/reset_botquestions/{user_number}'
    response = requests.get(url)
    if response.ok:
        print(response.text)
    else:
        print(f'Error resetting botquestions')

def test_send(user_number):
    url = f'{server_address}/test_send/{user_number}'
    response = requests.get(url)
    if response.ok:
        print(response.text)
    else:
        print(f'Error test send')

def save_conversation():
    url = f'{server_address}/save_conversations'
    response = requests.get(url)
    if response.ok:
        print(response.text)
    else:
        print(f'Error Saving conversations')


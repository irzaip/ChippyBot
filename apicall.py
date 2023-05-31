import asyncio
from conversations import Conversation
from colorama import Fore, Back, Style
import reduksi as rd
import openai
import time
import trans_id as trn
import requests
import random

async def ask_gpt(main_obj, conv_obj: Conversation, prompt: str) -> str:
    """
    Akses API ke OpenAI, dari prompt menjadi hasil string        
    input: masuknya list dari Object Conversation.messages
    """
    main_obj.antrian1 += 1
    print(f'sekarang antrian: {main_obj.antrian1}. > put')
    main_obj.queue.put_nowait(main_obj.antrian1)

    while main_obj.queue.qsize() > 0:
        print(f'{Style.DIM}masih ada {main_obj.queue.qsize()} antrian{Style.NORMAL}')
        await asyncio.sleep(1)

    print(f'tiket sudah di proses. mari kita kerjakan {main_obj.antrian1}')

    # cek panjang conversation
    conv_obj.messages = rd.trim_msg(conv_obj.messages)
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
    await asyncio.sleep(random.randint(2,7))

    return message

def ask_dalle(main_obj, conv_obj: Conversation, prompt: str): # type: ignore
    """generate dalle"""

    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512",
    )

    message = response["data"][0]["url"] # type: ignore
    return message


async def ask_ooba(main_obj, conv_obj: Conversation, prompt: str):

    main_obj.antrian2 += 1
    print(f'sekarang antrian: {main_obj.antrian2}. > put')
    main_obj.queue2.put_nowait(main_obj.antrian2)

    while main_obj.queue2.qsize() > 0:
        print(f'masih ada {main_obj.queue2.qsize()} antrian')
        await asyncio.sleep(1)

    print(f'tiket sudah di proses. mari kita kerjakan {main_obj.antrian2}')


    intro = build_pre_prompt(conv_obj)
    req = intro + trn.input_modifier(f"Saya:{prompt}\n{conv_obj.bot_name}:")
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
    conv_obj.messages.append({'role': 'user', 'content': trn.output_modifier(prompt)})
    print(f'{Fore.CYAN}{req}{Fore.WHITE}')
    response = requests.post("http://127.0.0.1:5000/api/v1/generate", json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        conv_obj.messages.append({'role': 'assistant', 'content': trn.output_modifier(result)})
        print('\n\nResponse:\n')
        intro = intro + f"\n\nSaya:{prompt}\nMaya:{result}"
        print(f'{Fore.CYAN}{intro}{Fore.WHITE}\n\n')
        return trn.output_modifier(result)
    else:
        return None
    

def build_pre_prompt(conv_obj: Conversation) -> str:
    result = ""
    for i in conv_obj.messages:
        if i['role'] == 'system':
            result = result + trn.input_modifier(f"{i['content']}\n")
        if i['role'] == 'user':
            result = result + trn.input_modifier(f"\nSaya:{i['content']}\n")
        if i['role'] == 'assistant':
            result = result + trn.input_modifier(f"\nMaya:{i['content']}\n")
    return result

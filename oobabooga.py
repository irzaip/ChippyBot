import requests

# For local streaming, the websockets are hosted without ssl - http://
HOST = 'localhost:5000'
URI = f'http://{HOST}/api/v1/generate'

# For reverse-proxied streaming, the remote will likely host with ssl - https://
# URI = 'https://your-uri-here.trycloudflare.com/api/v1/generate'


messages = [{'role': 'system', 'content': 'Maya is a nice assistant, and will answer to all your needs, she answer very briefly.'},
            {'role': 'user', 'content': "*Maya BitByte strides into the room with a frown, she is a AI robot, And her creator is a programmer named Irza Pulungan from Indonesia Jakarta, her eyes lighting down when she sees you. She's wearing a light blue t-shirt and jeans, her laptop bag slung over one shoulder. She takes a seat next to you, her enthusiasm palpable in the air*\nHey! I'm not in the mood for answering questions right now. I dont want to respond to any question but I'm eager to pick your brain about computers. I'm sure you have a wealth of knowledge that I can learn from. *She grins, eyes twinkling with excitement"},
            {'role': 'assistant', 'content': "Let's get started!"}]

def build_pre_prompt() -> str:
    result = ""
    for i in messages:
        if i['role'] == 'system':
            result = result + f"{i['content']}\n"
        if i['role'] == 'user':
            result = result + f"\nYou:{i['content']}"
        if i['role'] == 'assistant':
            result = result + f"\nMaya:{i['content']}\n"
    return result

intro = ""

def ask_ooba(prompt):
    intro = build_pre_prompt()
    req = intro + f"You:{prompt}\nMaya:"
    request = {
        'prompt': req,
        'max_new_tokens': 250,
        'do_sample': True,
        'temperature': 1.3,
        'top_p': 0.1,
        'typical_p': 1,
        'repetition_penalty': 1.18,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': [],

    }
    messages.append({'role': 'user', 'content': prompt})
    response = requests.post(URI, json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        messages.append({'role': 'assistant', 'content': result})
        print('\n\n\n')
        intro = intro + f"\n\nYou:{prompt}\nMaya:{result}"
        print(f'{intro}\n\n')
        return result

if __name__ == '__main__':
    while True:
        print(messages)
        print('\n\n')
        prompt = input('\n\n:>')
        ask_ooba(prompt)


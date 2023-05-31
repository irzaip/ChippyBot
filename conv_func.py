import toml

cfg = toml.load('config.toml')

def toggle_free_gpt(conv_obj):
    if conv_obj.free_gpt:
        conv_obj.free_gpt = False
    else:
        conv_obj.free_gpt = True

def add_system(conv_obj, message: str) -> None:
    reset_system(conv_obj)
    conv_obj.messages.append({"role" : "system", "content": message})

def change_system(conv_obj, message: str) -> None:
    conv_obj.messages[0]['content'] = message

def reset_system(conv_obj) -> None:
    conv_obj.messages = []
    
def add_role_user(conv_obj, message: str) -> None:
    conv_obj.messages.append({"role": "user", "content" : message})
    
def add_role_assistant(conv_obj, message: str) -> None:
    conv_obj.messages.append({"role" : "assistant", "content" : message})

from conversations import Conversation, Persona
import conv_func as cf
import toml

cfg = toml.load('config.toml')

def set_persona(persona: Persona, conv_obj: Conversation) -> None:
    cf.reset_system(conv_obj)
    set_bot_name(conv_obj.bot_name, conv_obj)
    cf.add_system(conv_obj, cfg[persona.name]['M_S'])
    cf.add_role_user(conv_obj, cfg[persona.name]['M_U'])
    cf.add_role_assistant(conv_obj, cfg[persona.name]['M_A'])  


def set_intro_msg(intro_msg: str, conv_obj: Conversation) -> None:
    conv_obj.intro_msg = intro_msg

def set_outro_msg(outro_msg: str, conv_obj: Conversation) -> None:
    conv_obj.outro_msg = outro_msg

def set_bot_name(bot_name: str, conv_obj: Conversation) -> None:
    conv_obj.bot_name = bot_name

def set_temperature(temperature: float, conv_obj: Conversation) -> None:
    conv_obj.temperature = temperature


def set_personality(bot_name: str, conf_section: str,  reply_with: str, conv_obj: Conversation) -> str:
    cf.reset_system(conv_obj)
    set_bot_name(bot_name, conv_obj)
    cf.add_system(conv_obj, cfg[conf_section]['M_S'])
    cf.add_role_user(conv_obj, cfg[conf_section]['M_U'])
    cf.add_role_assistant(conv_obj, cfg[conf_section]['M_A'])  
    return reply_with

def set_lisa_hrd(conv_obj: Conversation) -> None:
    conv_obj.last_question = 0
    conv_obj.botquestions = []
    conv_obj.persona = Persona.HRD

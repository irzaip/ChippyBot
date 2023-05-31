from conversations import Conversation, ConvMode, Message, Script


def add_last_question(conv_obj: Conversation) -> None:
    conv_obj.last_question += 1

def reset_last_question(conv_obj: Conversation) -> None:
    conv_obj.last_question = 0

def reset_botquestions(conv_obj: Conversation) -> None:
    conv_obj.botquestions = []

def reset_interview(conv_obj: Conversation) -> None:
    conv_obj.last_question = 0
    conv_obj.botquestions = []

def get_last_question(conv_obj: Conversation) -> tuple:
    for i, item in enumerate(conv_obj.botquestions):
        if not item.answer:
            print("INDEX QUEST: ", i)
            return (i, len(conv_obj.botquestions))
            break
    return (len(conv_obj.botquestions),len(conv_obj.botquestions))


def set_question_asked(question_asked: str, conv_obj: Conversation) -> None:
    conv_obj.question_asked = question_asked

def get_answer(conv_obj: Conversation, message: Message):
    #mengisi answer yg masih kosong.
    (i,k) = get_last_question(conv_obj)
    if i < (k-1):
        conv_obj.botquestions[i].answer = message.text
        try:
            r_text = conv_obj.botquestions[i+1].question
            set_question_asked(r_text, conv_obj)
            return r_text
        except Exception as e:
            print(e)                 
    conv_obj.convmode = ConvMode.CHITCHAT
    conv_obj.set_script(Script.BRAIN)
    return conv_obj.outro_msg
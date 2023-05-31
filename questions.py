from conversations import Conversation, ConvMode

def set_question_asked(question_asked: str, conv_obj: Conversation) -> None:
    conv_obj.question_asked = question_asked

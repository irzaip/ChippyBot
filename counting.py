from conversations import Conversation

def tambah_free_tries(conv_obj: Conversation, jumlah: int = 5):
    conv_obj.free_tries += jumlah

def kurangi_profanity_counter(conv_obj: Conversation):
    conv_obj.profanity_counter -= 1
    if conv_obj.profanity_counter < 0:
        conv_obj.profanity_counter = 0

def kurangi_funny_counter(conv_obj: Conversation):
    conv_obj.funny_counter -= 1
    if conv_obj.funny_counter < 0:
        conv_obj.funny_counter = 3

def kurangi_promo_counter(conv_obj: Conversation):
    conv_obj.promo_counter -= 1
    if conv_obj.promo_counter < 0:
        conv_obj.promo_counter = 7

def kurangi_free_tries(conv_obj: Conversation):
    conv_obj.free_tries -= 1
    if conv_obj.free_tries < 0:
        conv_obj.free_tries = 0

def tambah_paid_messages(conv_obj: Conversation, jumlah: int = 5):
    conv_obj.paid_messages += jumlah

def kurangi_paid_messages(conv_obj: Conversation) -> None:
    conv_obj.paid_messages -= 1
    if conv_obj.paid_messages < 0:
        conv_obj.paid_messages = 0

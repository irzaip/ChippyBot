from conversations import Conversation, Message
from typing import Protocol
import admin_func as admin 

class ConvType(Protocol):
    def __init__(self, conv_obj: Conversation):
        self.conv_obj = conv_obj
        self.is_group = self.is_this_a_group()

    def is_this_a_group(self):
        if "@g.us" in self.conv_obj.user_number:
            return True
        else:
            return False

    def run(self, message: Message) -> str:
        pass

# tipe prospek, client, platinum, admin
# cek apakah ini group
#    grup awal dapat 5 free gpt
#     personal dapat 5 free



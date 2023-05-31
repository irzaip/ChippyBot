from conversations import Conversation, ConvMode, Message
from colorama import Fore, Style, Back
import toml
import random
import counting as ct
import apicall as api
import datetime
from db_oper import insert_conv
import asyncio
import interview as iv
from typing import Literal

cfg = toml.load('config.toml')


async def run(self, conv_obj: Conversation, message: Message):
    return "NOT HAVING A GOLD USER"
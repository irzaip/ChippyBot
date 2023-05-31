## startup script

import cipi_iface as cp
from conversations import Persona, Script, BotQuestion, Role, ConvMode
import pprint
import json
import toml
import time
from colorama import Fore, Back, Style, just_fix_windows_console

just_fix_windows_console()

cfg = toml.load('config.toml')

irza = "62895352277562@c.us"
mlt = "6287760368781@c.us"
tm = "62895391400811@c.us"
grp = "120363149813038443@g.us"
un = irza

cp.set_bot_name(un, "Maya")
cp.set_message(un, cfg['VOLD']['M_S'], Role.SYSTEM)
cp.set_message(un, cfg['VOLD']['M_U'], Role.USER)
cp.set_message(un, cfg['VOLD']['M_A'], Role.ASSISTANT)


print(f"{Fore.RED}{Back.WHITE}Done RUNNING STARTUP SCRIPT{Fore.RESET}{Back.RESET}")




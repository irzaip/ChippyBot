import db_oper as dbo
import cipi_iface as cp
import random
import toml
import time

#send_to = dbo.get_private_chat_user('cipibot.db')
send_to = dbo.get_all_participant('cipibot.db')
send_to = [i[0] for i in send_to ]
#send_to = ["120363149813038443@g.us"]

cfg = toml.load('config.toml')

message = "Selamat pagi semuanya, semoga hari ini menjadi hari senin yang menyenangkan dan penuh berkah, selamat memulai pekerjaan anda."

begin = time.time()
for i in send_to:
    result = cp.send_to_phone(i, cfg['CONFIG']['BOT_NUMBER'], message=message)
    print(f'send to {i} is {result}')
    time.sleep(random.randint(10,20))
endtime = time.time()

print(f'Blast Pesan selesai dalam {round(endtime-begin)} detik')


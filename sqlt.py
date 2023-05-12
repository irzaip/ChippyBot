from conversations import Conversation
import sqlite3
import json
import pprint

user_number = "62895352277562@c.us"
bot_number = "6285775300227@c.us"


aa = Conversation(user_number=user_number, bot_number=bot_number)

print(aa.get_params())

epep = aa.get_params()

aa.put_params(epep)

result = aa.get_params()

conn = sqlite3.connect('cipibot.db')
cursor = conn.cursor()
#cursor.execute("SELECT * FROM CONNECTION WHERE user_number = ? and bot_number = ? ", (user_number, bot_number))

#cursor.execute('DELETE FROM CONNECTION WHERE user_number=?', (user_number) )
cursor.execute("INSERT INTO CONNECTION (user_number, bot_number, value) VALUES (?,?,?)", (user_number, bot_number, result))
conn.commit()
cursor.close ()


rows = cursor.fetchall()    
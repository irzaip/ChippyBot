import sqlite3
from typing import Literal

SQLITE = 'sqlite'

CONNECTION = 'connection'
CONVERSATIONS = 'conversations'




#db = MyDatabase(SQLITE,username='', password='', dbname='cipibot.db')

def insert_conv(user_number, bot_number, timestamp, content, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO CONVERSATION (user_number, bot_number, timestamp, content) VALUES (?,?,?,?)", (user_number, bot_number, timestamp, content))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return "Done inserting"

def get_db_connection(user_number: str, bot_number: str, db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CONNECTION WHERE user_number = ? and bot_number = ? ", (user_number, bot_number))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def get_db_all_connection(db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CONNECTION")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def new_db_connection(user_number: str, bot_number: str, result: str, db_name: str) -> Literal['new entry created!']:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO CONNECTION (user_number, bot_number, value) VALUES (?,?,?)", (user_number, bot_number, result))
    conn.commit()
    cursor.close()
    conn.close()
    return "new entry created!"

def update_db_connection(user_number: str, bot_number: str, result: str, db_name: str) -> Literal['new entry created!']:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE CONNECTION SET VALUE = ? WHERE user_number = ? AND bot_number = ?", (result, user_number, bot_number ))
    conn.commit()
    cursor.close()
    conn.close()
    return "new entry created!"

def del_db_connection(user_number: str, bot_number: str, db_name: str) -> Literal['data deleted!']:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM CONNECTION WHERE user_number=?', (user_number) )
    cursor.commit() # type: ignore
    cursor.close()
    conn.close()
    return "data deleted!"



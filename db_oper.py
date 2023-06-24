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
    conn.commit()
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

def create_participant(db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE PARTICIPANT (GROUPID TEXT PRIMARY KEY, GROUPNAME TEXT)')
    conn.commit()
    cursor.close()
    conn.close()
    return "done create"

def create_contacts(db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE CONTACTS (CONTACT_ID TEXT PRIMARY KEY, CONTACT_NAME TEXT, PRIVATE_CHAT BOOL)')
    conn.commit()
    cursor.close()
    conn.close()
    return "done create"


def insert_participants(participant: list[tuple], db_name: str):
    count = 0
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    for i in participant:
        check_sql = 'SELECT * FROM PARTICIPANT WHERE GROUPID = ?'
        cursor.execute(check_sql, (i[0],))
        hasil = cursor.fetchone()

        if not hasil:
            count += 1
            cursor.execute('INSERT INTO PARTICIPANT (GROUPID, GROUPNAME) VALUES (?,?)', (i[0], i[1]))
            conn.commit()
    
    cursor.close()
    conn.close()
    return f"Done Insert {count} new groups"

def insert_contacts(contacts: list[tuple], db_name: str):
    count = 0
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    for i in contacts:
        check_sql = 'SELECT * FROM CONTACTS WHERE CONTACT_ID = ?'
        cursor.execute(check_sql, (i[0],))
        hasil = cursor.fetchone()

        if not hasil:
            count += 1
            cursor.execute('INSERT INTO CONTACTS (CONTACT_ID, CONTACT_NAME) VALUES (?,?)', (i[0], i[1]))
            conn.commit()

    cursor.close()
    conn.close()
    return f"Done Insert {count} total new contacts"

def set_private_chat(contacts: list[str], db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    for i in contacts:
        cursor.execute('UPDATE CONTACTS SET PRIVATE_CHAT = ? WHERE CONTACT_ID = ?', (True, i))
    conn.commit()
    cursor.close()
    conn.close()
    return f"Done for {len(contacts)} users using private chat"

def get_all_participant(db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM PARTICIPANT')
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return result

def get_private_chat_user(db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT CONTACT_ID FROM CONTACTS WHERE PRIVATE_CHAT IS TRUE')
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return result

# CREATE TABLE TOKENS (
#     USER_NUMBER       TEXT,
#     TIMESTAMP         INTEGER,
#     PROMPT_TOKENS     INTEGER,
#     COMPLETION_TOKENS INTEGER,
#     TOTAL_TOKENS      INTEGER
# );

def insert_token_usage(user_number: str, timestamp: int, tokens: tuple[int, int, int], db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO TOKENS (USER_NUMBER, TIMESTAMP, PROMPT_TOKENS, COMPLETION_TOKENS, TOTAL_TOKENS) VALUES (?,?,?,?,?)', (user_number, timestamp, tokens[0], tokens[1], tokens[2]))
    conn.commit()
    cursor.close()
    conn.close()
    return "Done insert token usage"

def insert_info_cs(user_number: str, timestamp: int, db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO INFO_CS (USER_NUMBER, TIMESTAMP) VALUES (?,?)', (user_number, timestamp))
    conn.commit()
    cursor.close()
    conn.close()
    return "Done insert INFO_CS Campaign"
import json
import requests
import pprint
import db_oper

response = requests.get(f'http://127.0.0.1:8000/participant')

aa = json.loads(response.text)
# with open('file.txt', 'w') as f:
#     f.write(json.dumps(str(aa)))

participants = []
for i in aa:
    #pprint.pprint((i['group_id'], i['group_name']))
    participants.append((i['group_id'], i['group_name']))

result = db_oper.insert_participants(participants, 'cipibot.db')
print(result)

all_users = []
for i in aa:
    for n in i['participants']:
        all_users.append((n['contact_id'], n['name']))

set_users = list(set(all_users))

result = db_oper.insert_contacts(set_users, 'cipibot.db')
print(result)

connections = db_oper.get_db_all_connection('cipibot.db')

private_chat = []
for i in connections:
    if i[0].endswith('@c.us'):
        private_chat.append(i[0])

result = db_oper.set_private_chat(private_chat, 'cipibot.db')
print(result)

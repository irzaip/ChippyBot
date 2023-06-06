import json
import requests
import pprint
response = requests.get(f'http://127.0.0.1:8000/participant')

aa = json.loads(response.text)
# with open('file.txt', 'w') as f:
#     f.write(json.dumps(str(aa)))

for i in aa:
    pprint.pprint((i['group_id'], i['group_name']))
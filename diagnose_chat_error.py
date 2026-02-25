import requests
import json

BASE='http://127.0.0.1:8000'
login = requests.post(BASE+'/api/auth/login/', json={'username':'testlogin','password':'testpass123'})
print('LOGIN', login.status_code)
access = login.json().get('access')
headers = {'Authorization': f'Bearer {access}'}
r = requests.post(BASE+'/api/ia/chat/', json={'message':'Bonjour'}, headers=headers)
print('CHAT STATUS:', r.status_code)
print('CHAT RESPONSE:')
try:
    print(json.dumps(r.json(), indent=2))
except:
    print(r.text)

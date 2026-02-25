import requests
BASE='http://127.0.0.1:8000'
login = requests.post(BASE+'/api/auth/login/', json={'username':'testlogin','password':'testpass123'})
print('LOGIN', login.status_code)
print(login.json())
access = login.json().get('access')
headers = {'Authorization': f'Bearer {access}'}
r = requests.post(BASE+'/api/ia/chat/', json={'message':'Bonjour'}, headers=headers)
print('CHAT', r.status_code)
try:
    print(r.json())
except Exception:
    print(r.text)

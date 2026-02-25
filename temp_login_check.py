import requests

resp = requests.post('http://127.0.0.1:8000/api/auth/login/', json={'username':'testlogin','password':'testpass123'})
print('STATUS', resp.status_code)
try:
    print(resp.json())
except Exception:
    print(resp.text)

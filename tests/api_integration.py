import sys, subprocess, time, json
try:
    import requests
except Exception:
    print('requests not installed; installing...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
    import requests

base = 'http://127.0.0.1:8000/api/'

# unique username
import datetime
now = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
username = f'testuser_{now}'
password = 'password123'
email = f'{username}@example.com'

print('Registering user', username)
resp = requests.post(base + 'auth/register/', json={
    'username': username,
    'email': email,
    'password': password,
    'password_confirm': password,
    'nom': 'Doe',
    'prenom': 'Test',
    'niveau': 'débutant',
    'telephone': '0000000000'
})
print('register status', resp.status_code, resp.text)
if resp.status_code not in (200, 201):
    print('Registration failed, aborting')
    sys.exit(1)

print('Logging in')
resp = requests.post(base + 'auth/login/', json={'username': username, 'password': password})
print('login status', resp.status_code, resp.text)
if resp.status_code != 200:
    print('Login failed, aborting')
    sys.exit(1)

token = resp.json().get('access')
headers = {'Authorization': f'Bearer {token}'}

# Chat
print('\nCalling chat endpoint')
resp = requests.post(base + 'ia/chat/', json={'message': "Bonjour, peux-tu m'aider?"}, headers=headers)
print('chat status', resp.status_code, resp.text)

# Generer exercices
MATIERE_ID = 1
print('\nCalling generer_exercices for matiere_id=', MATIERE_ID)
resp = requests.post(base + 'ia/generer-exercices/', json={'nombre': 2, 'matiere_id': MATIERE_ID}, headers=headers)
print('generer_exercices status', resp.status_code)
try:
    print(resp.json())
except Exception:
    print(resp.text)

ex_id = None
if resp.status_code in (200,201):
    data = resp.json()
    exercices = data.get('exercices') or []
    if exercices:
        ex_id = exercices[0].get('id')

# analyser_reponse
if ex_id:
    print('\nCalling analyser_reponse for exercice_id=', ex_id)
    resp = requests.post(base + 'ia/analyser-reponse/', json={'exercice_id': ex_id, 'reponse_donnee': 'Ma réponse'}, headers=headers)
    print('analyser_reponse status', resp.status_code)
    try:
        print(resp.json())
    except Exception:
        print(resp.text)
else:
    print('\nNo exercice id to analyse; skipping analyser_reponse')

print('\nIntegration test finished')

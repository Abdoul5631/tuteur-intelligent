import os
import requests
import time

BASE = os.getenv('BASE_URL', 'http://localhost:8000')
API_LOGIN = f"{BASE}/api/auth/login/"
API_CHAT = f"{BASE}/api/ia/chat/"
API_GENERATE = f"{BASE}/api/ia/generer-exercices/"

# Configure these with a working user in the local DB
USERNAME = os.getenv('TEST_USER', 'testlogin')
PASSWORD = os.getenv('TEST_PASS', 'testpass123')


def get_token():
    r = requests.post(API_LOGIN, json={'username': USERNAME, 'password': PASSWORD})
    r.raise_for_status()
    data = r.json()
    # Support different token shapes
    token = data.get('access') or data.get('token') or data.get('access_token')
    if not token:
        raise RuntimeError('No token in login response: ' + str(data))
    return token


def chat(token, message, matiere_id=None, lecon_id=None):
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'message': message}
    if matiere_id:
        payload['matiere_id'] = matiere_id
    if lecon_id:
        payload['lecon_id'] = lecon_id
    r = requests.post(API_CHAT, json=payload, headers=headers)
    r.raise_for_status()
    return r.json()


def generate_exercises(token, nombre=2, matiere_id=1, topics=None):
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'nombre': nombre, 'matiere_id': matiere_id, 'topics': topics or ['general']}
    r = requests.post(API_GENERATE, json=payload, headers=headers)
    r.raise_for_status()
    return r.json()


if __name__ == '__main__':
    print('Running OpenAI integration smoke test')
    token = get_token()
    print('Token acquired')

    # 1) Bonjour -> accueil
    r1 = chat(token, 'Bonjour')
    print('CHAT Bonjour ->', r1.get('response')[:300])

    # 2) formule du volume -> expect explanation
    r2 = chat(token, 'Quelle est la formule du volume d\'une sphère ?')
    print('CHAT Formule ->', r2.get('response')[:600])

    # 3) Générer exercices
    r3 = generate_exercises(token, nombre=2, matiere_id=1, topics=['volume', 'sphère'])
    print('GENERER exercices ->', r3.get('nombre_genere'), 'exercices')
    for ex in r3.get('exercices', []):
        print('-', ex.get('question')[:200])

    print('Test completed')

#!/usr/bin/env python
import requests
import json

base_url = 'http://127.0.0.1:8000/api'

print('🧪 Testing Profile Update with PUT on /api/me/\n' + '='*70)

# Step 1: Login
login_response = requests.post(
    f'{base_url}/auth/login/',
    json={'username': 'testlogin', 'password': 'testpass123'}
)

if login_response.status_code != 200:
    print(f'✗ Login failed')
    exit(1)

access_token = login_response.json()['access']
headers = {'Authorization': f'Bearer {access_token}'}

# Step 2: Try PUT on /api/me/ endpoint
print('\n📝 Trying PUT on /api/me/')

update_data = {
    'nom': 'TOE By Me',
    'prenom': 'Madi By Me',
}

response = requests.put(
    f'{base_url}/me/',
    json=update_data,
    headers=headers
)

print(f'Status: {response.status_code}')
print(f'Response: {response.json() if response.status_code != 405 else response.text[:100]}')

if response.status_code == 200:
    print('\n✓ Profile update SUCCESSFUL on /api/me/')
else:
    print(f'\n✗ Profile update failed on /api/me/')

#!/usr/bin/env python
import requests
import json

base_url = 'http://127.0.0.1:8000/api'

print('🧪 Testing Profile Update with PATCH\n' + '='*70)

# Step 1: Login to get token
print('\n📝 Step 1: Getting access token')
login_response = requests.post(
    f'{base_url}/auth/login/',
    json={'username': 'testlogin', 'password': 'testpass123'}
)

if login_response.status_code != 200:
    print(f'✗ Login failed: {login_response.text}')
    exit(1)

access_token = login_response.json()['access']
headers = {'Authorization': f'Bearer {access_token}'}
print(f'✓ Token obtained')

# Step 2: Try PATCH instead of PUT
print('\n🔧 Step 2: Update with PATCH')

update_data = {
    'nom': 'TOE Updated',
    'prenom': 'Madi Updated',
}

print(f'Sending: {json.dumps(update_data, indent=2)}')

update_response = requests.patch(
    f'{base_url}/me/update/',
    json=update_data,
    headers=headers
)

print(f'\nResponse Status: {update_response.status_code}')

try:
    response_json = update_response.json()
    print(json.dumps(response_json, indent=2, ensure_ascii=False))
    
    if update_response.status_code == 200:
        print(f'\n✓ Update SUCCESSFUL')
    else:
        print(f'\n✗ Update FAILED')
except:
    print(f'Raw: {update_response.text[:300]}')

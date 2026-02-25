#!/usr/bin/env python
import requests
import json

base_url = 'http://127.0.0.1:8000/api'

print('🧪 Testing Profile Update Endpoint\n' + '='*70)

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

# Step 2: Get current profile
print('\n📋 Step 2: Get current profile')
profile_response = requests.get(f'{base_url}/me/', headers=headers)
print(f'Status: {profile_response.status_code}')
if profile_response.status_code == 200:
    current_profile = profile_response.json()
    print(f'Current profile:')
    for key in ['username', 'nom', 'prenom', 'email', 'date_naissance']:
        print(f'  {key}: {current_profile.get(key, "N/A")}')

# Step 3: Try to update profile
print('\n🔧 Step 3: Try to update profile')

update_data = {
    'nom': 'TOE Updated',
    'prenom': 'Madi Updated',
    'email': 'madi.new@gmail.com',
    'date_naissance': '2008-05-15'
}

print(f'Sending data: {json.dumps(update_data, indent=2)}')

update_response = requests.put(
    f'{base_url}/me/update/',
    json=update_data,
    headers=headers
)

print(f'\nResponse Status: {update_response.status_code}')
print(f'Response Headers: Content-Type = {update_response.headers.get("content-type")}')
print(f'\nResponse Body:')

try:
    response_json = update_response.json()
    print(json.dumps(response_json, indent=2, ensure_ascii=False))
except:
    print(f'Raw text: {update_response.text[:500]}')

if update_response.status_code != 200:
    print(f'\n✗ Update FAILED')
else:
    print(f'\n✓ Update SUCCESSFUL')

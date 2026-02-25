#!/usr/bin/env python
import requests
import json

url = 'http://127.0.0.1:8000/api/auth/login/'
data = {'username': 'testlogin', 'password': 'testpass123'}

print('Testing login endpoint...')
print(f'URL: {url}')
print(f'Credentials: {data}')
print()

try:
    r = requests.post(url, json=data)
    print(f'Status Code: {r.status_code}')
    
    if r.status_code == 200:
        result = r.json()
        print('✓ LOGIN SUCCESSFUL')
        print(f'  Access token (first 50 chars): {result.get("access", "N/A")[:50]}')
        print(f'  Refresh token (first 50 chars): {result.get("refresh", "N/A")[:50]}')
        if 'user' in result:
            print(f'  User info: {json.dumps(result["user"], indent=4)}')
    else:
        print(f'✗ LOGIN FAILED')
        print(f'Response: {r.text[:500]}')
        
except Exception as e:
    print(f'ERROR: {e}')
    import traceback
    traceback.print_exc()

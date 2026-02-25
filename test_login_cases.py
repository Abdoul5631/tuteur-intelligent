#!/usr/bin/env python
import requests
import json

url = 'http://127.0.0.1:8000/api/auth/login/'

test_cases = [
    # Test case-insensitive login
    {'username': 'testlogin', 'password': 'testpass123', 'description': 'lowercase exact'},
    {'username': 'TESTLOGIN', 'password': 'testpass123', 'description': 'UPPERCASE'},
    {'username': 'TestLogin', 'password': 'testpass123', 'description': 'MixedCase'},
    {'username': '  testlogin  ', 'password': 'testpass123', 'description': 'with whitespace'},
    {'username': 'testlogin', 'password': 'wrongpassword', 'description': 'wrong password'},
]

print('🔐 Testing Login Endpoint\n' + '='*60)

for test in test_cases:
    username = test['username']
    password = test['password']
    desc = test['description']
    
    data = {'username': username, 'password': password}
    
    try:
        r = requests.post(url, json=data)
        
        if r.status_code == 200:
            result = r.json()
            access = result.get('access', 'N/A')[:30] + '...' if len(result.get('access', '')) > 30 else result.get('access', 'N/A')
            status_icon = '✓'
        else:
            try:
                error_msg = r.json().get('detail', r.text[:50])
            except:
                error_msg = r.text[:70]
            access = f"ERROR: {error_msg}"
            status_icon = '✗'
        
        print(f'{status_icon} [{r.status_code:3d}] {desc:20s} | {access}')
        
    except Exception as e:
        print(f'✗ [ERR] {desc:20s} | Exception: {str(e)[:50]}')

print('\n✅ Case-insensitive login test complete!')

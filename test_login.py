#!/usr/bin/env python
import requests

test_users = [
    ('testlogin', 'testpass123'),
    ('Hamid', 'password_inconnue'),
    ('alice', 'unknownpass'),
]

print("=== Test de connexion ===\n")
for username, password in test_users:
    r = requests.post('http://localhost:8000/api/auth/login/', 
        json={'username': username, 'password': password})
    
    if r.status_code == 200:
        resp = r.json()
        print(f"✓ {username:15s} | Connecté avec succès")
        if 'access' in resp and 'refresh' in resp:
            print(f"  - JWT Tokens reçus")
        print()
    elif r.status_code == 401:
        print(f"✗ {username:15s} | Credentials invalides")
        print()
    else:
        print(f"✗ {username:15s} | Status {r.status_code}")
        try:
            print(f"  - Error: {r.json()}")
        except:
            pass
        print()

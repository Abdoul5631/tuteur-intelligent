#!/usr/bin/env python
"""
Test rapide : utilise le nouvel endpoint /api/ia/chat-test-mock/ 
qui force le mock sans dépendre de IA_PROVIDER
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

import requests

BASE_URL = "http://127.0.0.1:8000/api"

# 1. LOGIN
print("[1] Logging in as testlogin...")
login_resp = requests.post(
    f"{BASE_URL}/auth/login/",
    json={"username": "testlogin", "password": "testpass123"}
)
print(f"    Status: {login_resp.status_code}")
if login_resp.status_code != 200:
    print(f"    Error: {login_resp.text}")
    sys.exit(1)

token = login_resp.json()["access"]
print(f"    ✓ Got token: {token[:20]}...")

# 2. TEST MOCK CHAT (nouvelle route qui force mock)
print("\n[2] Testing /api/ia/chat-test-mock/ (forced mock)...")
headers = {"Authorization": f"Bearer {token}"}
chat_resp = requests.post(
    f"{BASE_URL}/ia/chat-test-mock/",
    json={"message": "Bonjour, comment ça marche?"},
    headers=headers
)
print(f"    Status: {chat_resp.status_code}")
print(f"    Response: {chat_resp.json()}")

if chat_resp.status_code == 200:
    print("    ✓ Mock endpoint works!")
else:
    print("    ✗ Mock endpoint failed")
    sys.exit(1)

# 3. TEST NORMAL CHAT (route originale avec IA_PROVIDER)
print("\n[3] Testing /api/ia/chat/ (with IA_PROVIDER=mock)...")
chat_resp2 = requests.post(
    f"{BASE_URL}/ia/chat/",
    json={"message": "Bonjour!"},
    headers=headers
)
print(f"    Status: {chat_resp2.status_code}")
print(f"    Response: {chat_resp2.json()}")

if chat_resp2.status_code == 200:
    print("    ✓ Normal chat endpoint works!")
else:
    print("    ✗ Normal chat endpoint failed")

print("\nDone!")

#!/usr/bin/env python
"""
Test OpenAI avec des prompts plus spécifiques
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
print("[1] Logging in...")
login_resp = requests.post(
    f"{BASE_URL}/auth/login/",
    json={"username": "testlogin", "password": "testpass123"},
    timeout=5
)
if login_resp.status_code != 200:
    print(f"    ✗ Login failed: {login_resp.text}")
    sys.exit(1)

token = login_resp.json()["access"]
print(f"    ✓ Got token")

headers = {"Authorization": f"Bearer {token}"}

# 2. TEST CHAT avec OpenAI
print("\n[2] Testing chat with OpenAI (asking about volume formula)...")
chat_resp = requests.post(
    f"{BASE_URL}/ia/chat/",
    json={"message": "Peux-tu m'expliquer la formule du volume d'une sphère?"},
    headers=headers,
    timeout=15
)
print(f"    Status: {chat_resp.status_code}")
if chat_resp.status_code == 200:
    response = chat_resp.json()
    print(f"    Response: {response.get('response', '')[:150]}...")
    print(f"    ✓ Chat works with OpenAI!")
else:
    print(f"    ✗ Error: {chat_resp.text}")

# 3. TEST EXERCISE GENERATION
print("\n[3] Testing exercise generation...")
ex_resp = requests.post(
    f"{BASE_URL}/ia/generer-exercices/",
    json={"count": 3, "topic": "volume et géométrie"},
    headers=headers,
    timeout=15
)
print(f"    Status: {ex_resp.status_code}")
if ex_resp.status_code == 200:
    response = ex_resp.json()
    exercises = response.get('exercises', [])
    print(f"    Generated {len(exercises)} exercises:")
    for i, ex in enumerate(exercises[:3], 1):
        print(f"      {i}. {ex.get('question', '')[:80]}")
    if len(exercises) > 0:
        print(f"    ✓ OpenAI exercise generation works!")
else:
    print(f"    ✗ Error: {ex_resp.text}")

print("\n✅ OpenAI integration test completed!")

#!/usr/bin/env python
"""Test profile update endpoint"""
import requests
import json

# First, login to get token
login_url = "http://localhost:8000/api/auth/login/"
login_data = {
    "username": "testlogin",
    "password": "testpass123"
}

print("Testing profile update endpoint...")
print("-" * 60)

# Login
print("1. Logging in...")
resp = requests.post(login_url, json=login_data)
print(f"   Status: {resp.status_code}")

if resp.status_code != 200:
    print(f"   Error: {resp.text}")
    exit(1)

tokens = resp.json()
access_token = tokens['access']
print(f"   ✓ Got token: {access_token[:30]}...")

# Now try GET /api/me/
print("\n2. Testing GET /api/me/...")
headers = {"Authorization": f"Bearer {access_token}"}
me_url = "http://localhost:8000/api/me/"
resp = requests.get(me_url, headers=headers)
print(f"   Status: {resp.status_code}")
print(f"   Response: {resp.text[:200]}...")

# Try PUT /api/me/
print("\n3. Testing PUT /api/me/...")
update_data = {
    "nom": "UpdatedLastName",
    "prenom": "UpdatedFirstName",
    "email": "testlogin+updated@test.com"
}
resp = requests.put(me_url, json=update_data, headers=headers)
print(f"   Status: {resp.status_code}")
print(f"   Response: {resp.text[:400]}")

if resp.status_code == 200:
    print("\n✓ PUT SUCCESSFUL!")
elif resp.status_code == 405:
    print("\n✗ Got 405 - Method not allowed")
else:
    print(f"\n✗ Got {resp.status_code}")

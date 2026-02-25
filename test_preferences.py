#!/usr/bin/env python
"""Test that preferences endpoint works"""
import requests
import json

login_url = "http://localhost:8000/api/auth/login/"
login_data = {
    "username": "testlogin",
    "password": "testpass123"
}

print("Testing preferences endpoint...")
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
print(f"   ✓ Got token")

# Test GET
headers = {"Authorization": f"Bearer {access_token}"}
pref_url = "http://localhost:8000/api/me/preferences/"
print(f"\n2. Testing GET {pref_url}...")
resp = requests.get(pref_url, headers=headers)
print(f"   Status: {resp.status_code}")
print(f"   Response: {resp.json()}")

if resp.status_code == 200:
    print("\n✓ Preferences endpoint works!")
else:
    print(f"\n✗ Got {resp.status_code}")

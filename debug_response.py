#!/usr/bin/env python
import requests

token_resp = requests.post(
    "http://127.0.0.1:8000/api/auth/login/",
    json={"username": "testlogin", "password": "testpass123"}
)
token = token_resp.json()["access"]
headers = {"Authorization": f"Bearer {token}"}

chat_resp = requests.post(
    "http://127.0.0.1:8000/api/ia/chat/",
    json={"message": "Bonjour"},
    headers=headers
)
print("Status:", chat_resp.status_code)
print("Response:", chat_resp.json())

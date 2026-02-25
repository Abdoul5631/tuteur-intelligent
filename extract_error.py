#!/usr/bin/env python
"""Extract error from Django debugpage"""
import requests
import re

login_url = 'http://localhost:8000/api/auth/login/'
login_data = {'username': 'testlogin', 'password': 'testpass123'}
resp = requests.post(login_url, json=login_data)
token = resp.json()['access']
headers = {'Authorization': f'Bearer {token}'}

resp = requests.get('http://localhost:8000/api/me/', headers=headers)

# Extract exception type
match = re.search(r'<title>(\w+)', resp.text)
if match:
    print(f"✗ Exception Type: {match.group(1)}")

# Look for 'exception_value' in the HTML
match = re.search(r'exception_value["\'>]*>([^<]+)', resp.text)
if match:
    print(f"Exception Message: {match.group(1)}")

# Look for the actual traceback - find lineno with filename
matches = re.findall(r'File "([^"]+)", line (\d+),? in (\w+)', resp.text)
print("\nTraceback:")
for filepath, lineno, funcname in matches:
    print(f"  {filepath}:{lineno} in {funcname}")

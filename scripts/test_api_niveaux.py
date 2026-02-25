import requests
import json

url = 'http://localhost:8000/api/niveaux/'
try:
    r = requests.get(url, timeout=5)
    print(f'Status: {r.status_code}')
    print(f'Headers: {dict(r.headers)}')
    try:
        data = r.json()
        print(f'JSON Response: {json.dumps(data, ensure_ascii=False, indent=2)}')
    except Exception as e:
        print(f'Text Response: {r.text}')
except Exception as e:
    print(f'Error: {e}')

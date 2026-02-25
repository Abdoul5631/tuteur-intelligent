import os, json
import django
import requests
os.environ.setdefault('DJANGO_SETTINGS_MODULE','backend.settings')
django.setup()

urls = ['http://localhost:8000/api/auth/register/','http://localhost:8000/api/niveaux/']
for u in urls:
    try:
        r = requests.get(u, timeout=5)
        print('\nURL:', u)
        print('Status:', r.status_code)
        try:
            print('JSON:', json.dumps(r.json(), ensure_ascii=False, indent=2))
        except Exception as e:
            print('Text:', r.text[:1000])
    except Exception as e:
        print('Error connecting to', u, e)

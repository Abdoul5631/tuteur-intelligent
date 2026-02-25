#!/usr/bin/env python
import os, django, json, traceback
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from django.utils.safestring import SafeString

from core.views import ProfilUtilisateurView
from core.models import Utilisateur

factory = RequestFactory()

try:
    user = User.objects.get(username='testlogin')
except User.DoesNotExist:
    print('User testlogin not found')
    raise SystemExit(1)

# ensure Utilisateur exists
try:
    util = Utilisateur.objects.get(user=user)
except Exception as e:
    print('Utilisateur profile missing:', e)
    raise SystemExit(1)

# Build PUT request
data = {
    'nom': 'TOE Debug',
    'prenom': 'Madi Debug',
    'email': 'madi.debug@example.com'
}

req = factory.put('/api/me/update/', data=json.dumps(data), content_type='application/json')
req.user = user

view = ProfilUtilisateurView.as_view()

try:
    response = view(req)
    print('Response status:', response.status_code)
    try:
        print(response.data)
    except Exception:
        print('No response.data')
except Exception as e:
    print('Exception when calling view:')
    traceback.print_exc()

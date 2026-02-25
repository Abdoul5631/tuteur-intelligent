#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Utilisateur

# Supprimer si existe
User.objects.filter(username='testlogin').delete()

# Creer utilisateur
user = User.objects.create_user(
    username='testlogin',
    email='test@test.com',
    password='testpass123',
    is_active=True
)

utilisateur = Utilisateur.objects.create(user=user, niveau_global='intermediaire')

print('✓ Utilisateur testlogin cree')
print(f'  Existe en BD: {User.objects.filter(username="testlogin").exists()}')
print(f'  Mot de passe OK: {user.check_password("testpass123")}')

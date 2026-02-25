#!/usr/bin/env python
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

# Tester les utilisateurs
print("=== Test de logique d'authentification ===\n")

users_to_test = ['testlogin', 'Hamid', 'alice']

for username in users_to_test:
    try:
        user = User.objects.get(username__iexact=username)
        print(f"✓ {username}")
        print(f"  - Existe? Oui")
        print(f"  - Actif? {user.is_active}")
        print(f"  - Email: {user.email}")
        print(f"  - a_usable_password? {user.has_usable_password()}")
        
        # Tester le mot de passe pour testlogin
        if username == 'testlogin':
            test_pwd = 'testpass123'
            result = user.check_password(test_pwd)
            print(f"  - Password '{test_pwd}' correct? {result}")
        
        print()
    except User.DoesNotExist:
        print(f"✗ {username} - Utilisateur non trouvé\n")

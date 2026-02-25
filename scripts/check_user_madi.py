import os
import sys
import django
import requests

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE','backend.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Utilisateur

# Check if user exists
print("=== CHECKING DATABASE ===")
try:
    user = User.objects.get(username='Madi')
    print(f"✓ User 'Madi' found")
    print(f"  - Email: {user.email}")
    print(f"  - Password hash: {user.password[:20]}...")
    print(f"  - Is active: {user.is_active}")
    print(f"  - Check password '12345678': {user.check_password('12345678')}")
    
    try:
        utilisateur = Utilisateur.objects.get(user=user)
        print(f"✓ Utilisateur (profile) found")
        print(f"  - Nom: {utilisateur.nom}")
        print(f"  - Prenom: {utilisateur.prenom}")
        print(f"  - Niveau global: {utilisateur.niveau_global}")
        print(f"  - Niveau scolaire: {utilisateur.niveau_scolaire}")
    except Utilisateur.DoesNotExist:
        print("✗ NO Utilisateur (profile) found for this user")
except User.DoesNotExist:
    print("✗ User 'Madi' NOT found in database")

# Test login API
print("\n=== TESTING LOGIN API ===")
try:
    r = requests.post('http://localhost:8000/api/auth/login/', 
        json={'username': 'Madi', 'password': '12345678'},
        timeout=5)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")
except Exception as e:
    print(f"Error: {e}")

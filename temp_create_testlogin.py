import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from django.contrib.auth.models import User
from core.models import Utilisateur

username = 'testlogin'
email = 'testlogin@test.com'
password = 'testpass123'

User.objects.filter(username=username).delete()
user = User.objects.create_user(username=username, email=email, password=password, first_name='Test', last_name='User')
Utilisateur.objects.create(user=user, nom='User', prenom='Test', niveau_global='débutant')
print('Created', user.username)

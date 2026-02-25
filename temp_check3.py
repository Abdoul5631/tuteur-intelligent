import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','backend.settings')
django.setup()
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
User = get_user_model()
print('DJANGO DB NAME:', settings.DATABASES['default'].get('NAME'))
print('All usernames:', list(User.objects.values_list('username', flat=True)))
username = 'testlogin'
pwd = 'testpass123'
exists = User.objects.filter(username=username).exists()
print('Exists:', exists)
if exists:
    u = User.objects.get(username=username)
    print('User id:', u.id)
    print('is_active:', u.is_active)
    print('check_password(user):', u.check_password(pwd))
    auth = authenticate(username=username, password=pwd)
    print('authenticate() result:', None if auth is None else f'user id={auth.id}, username={auth.username}')
else:
    print('User not found')

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from django.contrib.auth.models import User
u = User.objects.filter(username='testlogin').first()
if u is None:
    print('NO_USER')
else:
    print('FOUND', u.username, 'is_active=', u.is_active)
    print('check_password testpass123 ->', u.check_password('testpass123'))
    print('check_password testpass124 ->', u.check_password('testpass124'))

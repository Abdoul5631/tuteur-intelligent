#!/usr/bin/env python
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.urls import resolve
from django.urls.exceptions import Resolver404
from core.views import login_user

try:
    resolver = resolve('/api/auth/login/')
    print(f'✓ Route resolved')
    print(f'  View function name: {resolver.func.__name__}')
    print(f'  View module: {resolver.func.__module__}')
    
    # Comparer avec notre login_user
    print(f'\nComparaison:')
    print(f'  Our login_user module: {login_user.__module__}')
    print(f'  Our login_user name: {login_user.__name__}')
    
except Resolver404 as e:
    print(f'✗ Route not found: {e}')
except Exception as e:
    print(f'✗ Error: {type(e).__name__}: {e}')
    import traceback
    traceback.print_exc()

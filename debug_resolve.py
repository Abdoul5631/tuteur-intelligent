import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','backend.settings')
django.setup()
from django.urls import resolve
view = resolve('/api/auth/login/')
print('Resolved:', view)
func = view.func
print('Func repr:', func)
print('Has csrf_exempt attr:', getattr(func, 'csrf_exempt', False))
print('Has view_class:', getattr(func, 'view_class', None))

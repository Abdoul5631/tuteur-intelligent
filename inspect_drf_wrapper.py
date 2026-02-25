#!/usr/bin/env python
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.views import profil_utilisateur
from rest_framework.decorators import api_view

# Get the actual view class through DRF's wrapper
print("Inspecting WrappedAPIView class:")
cls = profil_utilisateur.cls
print(f"  Class: {cls}")
print(f"  Methods: {getattr(cls, 'http_method_names', 'N/A')}")
print(f"  Allowed: {getattr(cls, 'allowed_methods', 'N/A')()}")

# Get source info
import inspect
print(f"\nFunction source (first 30 lines):")
try:
    source = inspect.getsource(profil_utilisateur.__wrapped__ or profil_utilisateur)
    for i, line in enumerate(source.split('\n')[:10], 1):
        print(f"  {i:2d}: {line[:70]}")
except:
    print("  (Could not get source)")

# Check actual decorators by checking closure variables
print(f"\nDRF closure info:")
if hasattr(profil_utilisateur, '__closure__') and profil_utilisateur.__closure__:
    print(f"  Closure cells: {len(profil_utilisateur.__closure__)}")
else:
    print(f"  No closure")

#!/usr/bin/env python
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.views import profil_utilisateur

print("profil_utilisateur attributes:")
print(f"  Type: {type(profil_utilisateur)}")
print(f"  Callable: {callable(profil_utilisateur)}")
print(f"  __name__: {getattr(profil_utilisateur, '__name__', 'N/A')}")
print(f"  __doc__: {getattr(profil_utilisateur, '__doc__', 'N/A')[:50]}...")

# Check for DRF-specific attributes  
print(f"\nDRF Attributes:")
print(f"  .cls: {getattr(profil_utilisateur, 'cls', 'N/A')}")
print(f"  .initkwargs: {getattr(profil_utilisateur, 'initkwargs', 'N/A')}")
print(f"  .suffix: {getattr(profil_utilisateur, 'suffix', 'N/A')}")
print(f"  .http_method_names: {getattr(profil_utilisateur, 'http_method_names', 'N/A')}")

# List all attributes  
print(f"\nAll non-private attributes:")
attrs = [x for x in dir(profil_utilisateur) if not x.startswith('_')]
for attr in attrs[:15]:
    val = getattr(profil_utilisateur, attr)
    if not callable(val):
        print(f"  {attr}: {str(val)[:40]}")

#!/usr/bin/env python
"""Debug why @api_view doesn't accept PUT"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.dirname(__file__))

import django
django.setup()

# Import the view
from core.views import profil_utilisateur

print(f"View: {profil_utilisateur}")
print(f"Type: {type(profil_utilisateur)}")
print(f"Attributes:")
for attr in dir(profil_utilisateur):
    if not attr.startswith('_'):
        val = getattr(profil_utilisateur, attr)
        print(f"  {attr}: {type(val).__name__} = {str(val)[:60]}")

# Check the cls attribute
if hasattr(profil_utilisateur, 'cls'):
    print(f"\n  .cls = {profil_utilisateur.cls}")
    if hasattr(profil_utilisateur.cls, 'http_method_names'):
        print(f"  .cls.http_method_names = {profil_utilisateur.cls.http_method_names}")

# Check the handler attribute
if hasattr(profil_utilisateur, 'handler'):
    print(f"\n  .handler = {profil_utilisateur.handler}")

# Check the allowed_methods
if hasattr(profil_utilisateur, 'allowed_methods'):
    print(f"\n  .allowed_methods = {profil_utilisateur.allowed_methods}")

# Check what the decorator set
if hasattr(profil_utilisateur, 'versioning_class'):
    print(f"\n  .versioning_class = {profil_utilisateur.versioning_class}")

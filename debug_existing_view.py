#!/usr/bin/env python
"""Debug the existing mettre_a_jour_profil function"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.dirname(__file__))

import django
django.setup()

# Import the view
from core.views import mettre_a_jour_profil

print(f"View: {mettre_a_jour_profil}")
print(f"Type: {type(mettre_a_jour_profil)}")

# Check the cls attribute
if hasattr(mettre_a_jour_profil, 'cls'):
    print(f"\n  .cls = {mettre_a_jour_profil.cls}")
    if hasattr(mettre_a_jour_profil.cls, 'http_method_names'):
        print(f"  .cls.http_method_names = {mettre_a_jour_profil.cls.http_method_names}")

#!/usr/bin/env python
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.views import profil_utilisateur
from rest_framework.decorators import api_view

# Get the actual view class through DRF's wrapper
print("profil_utilisateur inspection:")
cls = profil_utilisateur.cls
print(f"  cls: {cls}")
print(f"  cls.http_method_names: {cls.http_method_names}")

# Check the view_initkwargs
print(f"\nview_initkwargs: {profil_utilisateur.view_initkwargs}")
print(f"initkwargs: {profil_utilisateur.initkwargs}")

# Check for suffix_pattern
print(f"\nsuffix_pattern: {getattr(profil_utilisateur, 'suffix_pattern', 'N/A')}")

# Try to get the actual API view closure
print(f"\nDRF closure analysis:")
closure = profil_utilisateur.__closure__
if closure:
    for i, cell in enumerate(closure):
        try:
            val = cell.cell_contents
            if isinstance(val, list) and len(val) < 10:
                print(f"  Cell {i}: {val}")
            elif isinstance(val, dict):
                print(f"  Cell {i} (dict): {list(val.keys())[:5]}")
        except:
            pass

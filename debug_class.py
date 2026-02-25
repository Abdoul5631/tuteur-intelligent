#!/usr/bin/env python
"""Directly try to execute the class from views.py"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.dirname(__file__))

import django
django.setup()

# Try to import the entire module content and execute it step by step
import importlib
import traceback

try:
    # First, import the module normally
    import core.views
    print(f"✓ Module imported, has {len([x for x in dir(core.views) if not x.startswith('_')])} public items")
    
    # Now let's manually walk through the file looking for the class definition
    with open('core/views.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the class line
    for i, line in enumerate(lines):
        if 'class ProfilUtilisateurView' in line:
            print(f"\n✓ Found class definition at line {i+1}")
            print(f"  Context:")
            for j in range(max(0, i-2), min(len(lines), i+10)):
                print(f"  {j+1}: {lines[j].rstrip()}")
            break
    
    # Try to get the class by name using getattr
    if hasattr(core.views, 'ProfilUtilisateurView'):
        print("\n✓ Class IS in core.views!")
        cls = getattr(core.views, 'ProfilUtilisateurView')
        print(f"  Class: {cls}")
    else:
        print("\n✗ Class NOT found with hasattr")
        
        # Check if maybe it got compiled but with a different name
        all_items = dir(core.views)
        print(f"\n  Looking for 'Profil' in module:")
        matches = [x for x in all_items if 'Profil' in x]
        print(f"  Found: {matches}")
        
        # Check if any of the wrapper functions are there
        if 'profil_utilisateur' in all_items:
            print(f"\n  ✓ profil_utilisateur function IS there")
            func = getattr(core.views, 'profil_utilisateur')
            print(f"  Type: {type(func)}")
            
except Exception as e:
    print(f"\n✗ Error: {e}")
    traceback.print_exc()

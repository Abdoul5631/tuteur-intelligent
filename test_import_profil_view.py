#!/usr/bin/env python
import sys
import os
import traceback

# Set up Django before importing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

try:
    import django
    print("✓ Django imported")
    django.setup()
    print("✓ Django setup complete")
    
    print("\nAttempting to import ProfilUtilisateurView...")
    from core.views import ProfilUtilisateurView
    print("✓ ProfilUtilisateurView imported successfully")
    
    print(f"  Type: {type(ProfilUtilisateurView)}")
    print(f"  Has as_view: {hasattr(ProfilUtilisateurView, 'as_view')}")
    
except Exception as e:
    print(f"\n✗ IMPORT FAILED:")
    print(f"\nException type: {type(e).__name__}")
    print(f"Exception message: {e}")
    print(f"\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)

print("\n✓ All imports successful!")

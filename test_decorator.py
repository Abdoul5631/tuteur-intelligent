#!/usr/bin/env python
"""Test if the decorator works"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.dirname(__file__))

import django
django.setup()

# Import what we need
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

print("✓ All imports successful")

# Try to create a simple class with the same decorator
try:
    @method_decorator(csrf_exempt, name='dispatch')
    class TestView(APIView):
        permission_classes = [IsAuthenticated]
        
        def get(self, request):
            return Response({'test': 'ok'})
    
    print("✓ Test class created successfully")
    print(f"✓ Has get method: {hasattr(TestView, 'get')}")
    print(f"✓ Has as_view: {hasattr(TestView, 'as_view')}")
    
except Exception as e:
    print(f"✗ Error creating test class: {e}")
    import traceback
    traceback.print_exc()

# Now try to do what should be in views.py
print("\nNow testing the actual views.py location...")
try:
    # Read the section of views.py where the class is defined
    import importlib.util
    spec = importlib.util.spec_from_file_location("test_views", "core/views.py")
    test_module = importlib.util.module_from_spec(spec)
    
    print("Attempting to execute module...")
    spec.loader.exec_module(test_module)
    print("✓ Module executed")
    
    if hasattr(test_module, 'ProfilUtilisateurView'):
        print("✓ ProfilUtilisateurView found!")
    else:
        print("✗ ProfilUtilisateurView not found")
        print(f"  Available: {[x for x in dir(test_module) if 'Profil' in x]}")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

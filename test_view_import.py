#!/usr/bin/env python
"""Debug import issues with full traceback"""
import os
import sys

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.dirname(__file__))

def main():
    try:
        # Setup Django first
        import django
        django.setup()
        
        # Now try to import
        print("Attempting to import core.views...")
        import core.views as views_module
        print(f"✓ Module imported, has {len(dir(views_module))} items")
        
        # Try to access the class directly
        print("\nTrying direct attribute access...")
        cls = getattr(views_module, 'ProfilUtilisateurView', None)
        if cls:
            print(f"✓ Found via getattr: {cls}")
        else:
            print("✗ Not found via getattr")
            
            # List all classes
            import inspect
            classes = [name for name, obj in inspect.getmembers(views_module) if inspect.isclass(obj)]
            print(f"\nAll classes in module: {classes}")
        
    except Exception as e:
        print(f"✗ Exception during import: {e}")
        print(f"   Type: {type(e).__name__}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        
        # Try to determine where error occurred
        import sys
        exc_info = sys.exc_info()
        if exc_info[2]:
            print(f"\nError in file: {exc_info[2].tb_frame.f_code.co_filename}")
            print(f"Line: {exc_info[2].tb_lineno}")

if __name__ == '__main__':
    main()

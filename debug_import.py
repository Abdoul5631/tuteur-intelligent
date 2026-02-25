import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

try:
    import core.views as views
    print("✓ Module imported successfully")
    print(f"  Module file: {views.__file__}")
    
    print("\n📋 All functions in module:")
    funcs = [x for x in dir(views) if not x.startswith('_') and callable(getattr(views, x))]
    for func in sorted(funcs)[:30]:
        obj = getattr(views, func)
        print(f"  - {func:30s} ({type(obj).__name__})")
    
    print("\n🔍 Looking for login_view specifically:")
    if hasattr(views, 'login_view'):
        print("  ✓ login_view FOUND")
        login_func = getattr(views, 'login_view')
        print(f"    Type: {type(login_func)}")
        print(f"    Callable: {callable(login_func)}")
    else:
        print("  ✗ login_view NOT FOUND")
        
except Exception as e:
    print(f"✗ IMPORT ERROR: {e}")
    import traceback
    traceback.print_exc()

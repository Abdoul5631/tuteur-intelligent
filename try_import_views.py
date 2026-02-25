import os, traceback
os.environ.setdefault('DJANGO_SETTINGS_MODULE','backend.settings')
try:
    import django
    django.setup()
    import importlib
    views = importlib.import_module('core.views')
    print('Imported core.views, has ProfilUtilisateurView:', hasattr(views,'ProfilUtilisateurView'))
except Exception:
    print('IMPORT ERROR:')
    traceback.print_exc()
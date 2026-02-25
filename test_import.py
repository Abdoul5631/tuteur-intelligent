#!/usr/bin/env python
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

try:
    import core.views as views_module
    print('✓ core.views importé')
    
    # Lister les classes/fonctions
    attrs = [x for x in dir(views_module) if not x.startswith('_')]
    print(f'\n Attributs (premier 30):')
    for attr in attrs[:30]:
        print(f'    - {attr}')
    
    print(f'\n✓ CustomTokenObtainPairView présente? {"CustomTokenObtainPairView" in attrs}')
    print(f'✓ CustomTokenObtainPairSerializer présente? {"CustomTokenObtainPairSerializer" in attrs}')
    
    # Essayer d'accéder directement
    try:
        cls = getattr(views_module, 'CustomTokenObtainPairView')
        print(f'\n✓ Classe trouvée: {cls}')
    except AttributeError as e:
        print(f'\n✗ Classe non trouvée: {e}')
        
except Exception as e:
    print(f'✗ Erreur: {type(e).__name__}: {e}')
    import traceback
    traceback.print_exc()

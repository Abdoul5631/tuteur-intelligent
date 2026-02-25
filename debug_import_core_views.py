import sys
import importlib
import traceback

sys.path.insert(0, r'D:\Documents\Tuteur intelligent')
try:
    importlib.invalidate_caches()
    m = importlib.import_module('core.views')
    print('Imported core.views OK')
    for name in ['mettre_a_jour_profil', 'preferences_utilisateur', 'changer_mot_de_passe']:
        print(f"{name}:", hasattr(m, name))
    print('Some defs:', [n for n in dir(m) if n.startswith('mettre') or n.startswith('preferences') or n.startswith('changer')][:20])
except Exception:
    traceback.print_exc()

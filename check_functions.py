#!/usr/bin/env python
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core import views

funcs = [
    'preferences_utilisateur',
    'changer_mot_de_passe',
    'lecon_detail',
    'exercices_par_lecon',  
    'recommandations_exercices',
    'leaderboard',
    'resultats_detailles',
    'statistiques_lecons',
]

print("Checking functions in core.views:")
for func in funcs:
    exists = hasattr(views, func)
    status = "OK" if exists else "MISSING"
    print(f"  {status:10s} | {func}")

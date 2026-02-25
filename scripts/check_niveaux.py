import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','backend.settings')
import django
django.setup()
from core.services.curriculum_complet import NIVEAUX
print('NIVEAUX count:', len(NIVEAUX))
print(NIVEAUX)

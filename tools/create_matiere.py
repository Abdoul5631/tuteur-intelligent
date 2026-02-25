import os
import sys
# Ensure project root is on sys.path so Django can import the settings module
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
from django import setup
setup()
from core.models import Matiere

m, created = Matiere.objects.get_or_create(
	nom='mathematiques',
	defaults={'description': 'Seed', 'couleur_hex': '#3B82F6', 'icone': '📚'}
)
print(m.id)

#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db import connection

cursor = connection.cursor()
cursor.execute("PRAGMA table_info(core_matiere)")
columns = cursor.fetchall()

print('Colonnes de core_matiere:')
for col in columns:
    print(f'  {col[1]} ({col[2]})')

print('\n---')
print('Test import Matiere:')
from core.models import Matiere
print(f'Fields: {[f.name for f in Matiere._meta.get_fields()]}')

#!/usr/bin/env python
"""
Script de test du workflow complet (login, lecons, chat IA, exercices)
"""

import os
import django
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Utilisateur

# ==== STEP 1: CREER UTILISATEUR TEST ====
username = 'demouser'
password = 'demo123456'
email = 'demo@tuteur.test'

# Supprimer s'il existe
User.objects.filter(username=username).delete()

# Creer
user = User.objects.create_user(username=username, email=email, password=password, first_name='Demo', last_name='User')
utilisateur = Utilisateur.objects.create(user=user, niveau_global='intermediaire')

print(f"✓ Utilisateur cree: {username} / {password}\n")

# ==== STEP 2: LOGIN ====
BASE_URL = 'http://localhost:8000/api'

print("=== WORKFLOW TEST (Requetes HTTP) ===\n")
print("1. LOGIN:")

resp = requests.post(f'{BASE_URL}/auth/login/', json={
    'username': username,
    'password': password
})

if resp.status_code == 200:
    tokens = resp.json()
    access_token = tokens['access']
    print(f"   ✓ Login OK (status 200)")
    print(f"   - Access token: {access_token[:50]}...\n")
else:
    print(f"   X Login FAILED (status {resp.status_code})")
    print(f"   - Error: {resp.text}\n")
    exit(1)

headers = {'Authorization': f'Bearer {access_token}'}

# ==== STEP 3: VOIR LES MATIERES ====
print("2. VOIR LES MATIERES (GET /lecons/):")

resp = requests.get(f'{BASE_URL}/lecons/', headers=headers)

if resp.status_code == 200:
    lecons = resp.json()
    print(f"   ✓ Recu {len(lecons)} lecons")
    if lecons:
        lecon = lecons[0]
        print(f"   - Premiere lecon: {lecon.get('titre', 'N/A')}")
        lecon_id = lecon.get('id')
        matiere_name = lecon.get('matiere', {}).get('nom', 'N/A') if isinstance(lecon.get('matiere'), dict) else 'N/A'
        print(f"     - Matiere: {matiere_name}")
        print(f"     - ID: {lecon_id}\n")
else:
    print(f"   X FAILED (status {resp.status_code})\n")
    lecon_id = None

# ==== STEP 4: CHATTER AVEC L'IA ====
if lecon_id:
    print("3. CHAT AVEC L'IA (POST /ia/chat/):")
    
    resp = requests.post(f'{BASE_URL}/ia/chat/', 
        headers=headers,
        json={
            'message': 'Bonjour! Peux-tu m\'expliquer les fractions?',
            'matiere': 'mathematiques',
            'niveau': '6eme'
        }
    )
    
    if resp.status_code == 200:
        result = resp.json()
        reponse = result.get('reponse', 'N/A')
        print(f"   ✓ Chat OK (status 200)")
        print(f"   - Reponse IA: {reponse[:100]}...\n")
    else:
        print(f"   X FAILED (status {resp.status_code})")
        print(f"   - Response: {resp.text[:200]}\n")
else:
    print("3. CHAT AVEC L'IA: Non teste (pas de lecon)\n")

# ==== STEP 5: GENERER EXERCICES ====
print("4. GENERER EXERCICES (POST /ia/generer-exercices/):")

resp = requests.post(f'{BASE_URL}/ia/generer-exercices/',
    headers=headers,
    json={
        'nombre': 2,
        'matiere': 'mathematiques',
        'niveau': '6eme',
        'topics': ['fractions', 'operations']
    }
)

if resp.status_code in [200, 201]:
    result = resp.json()
    exercices = result.get('exercices', [])
    print(f"   ✓ Genere {len(exercices)} exercices")
    if exercices:
        ex = exercices[0]
        print(f"   - Question 1: {ex.get('question', 'N/A')[:70]}...\n")
else:
    print(f"   X FAILED (status {resp.status_code})")
    print(f"   - Response: {resp.text[:200]}\n")

# ==== STEP 6: VOIR LE PROFIL ====
print("5. VER LE PROFIL (GET /profil/):")

resp = requests.get(f'{BASE_URL}/profil/', headers=headers)

if resp.status_code == 200:
    profil = resp.json()
    print(f"   ✓ Profil OK")
    print(f"   - Utilisateur: {profil.get('prenom', 'N/A')} {profil.get('nom', 'N/A')}")
    print(f"   - Niveau global: {profil.get('niveau_global', 'N/A')}\n")
else:
    print(f"   X FAILED (status {resp.status_code})\n")

print("="*60)
print("WORKFLOW TEST COMPLETE!")
print("="*60)

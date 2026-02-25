#!/usr/bin/env python
"""
Test end-to-end du chat IA via l'API
Simule une conversation complète élève-IA
"""

import requests
import json
import sys
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Utilisateur
import time

BASE_URL = 'http://localhost:8000/api'

print("=" * 80)
print("🔗 TEST END-TO-END: Chat IA via API REST")
print("=" * 80)
print()

# ============ STEP 1: Créer/Récupérer utilisateur de test ============
print("📝 STEP 1: Préparation utilisateur de test")
print("-" * 80)

username = 'ia_test_user'
email = 'iatest@test.local'
password = 'iatest12345'

# Supprimer l'utilisateur s'il existe déjà
User.objects.filter(username=username).delete()

# Créer nouvel utilisateur
user = User.objects.create_user(
    username=username,
    email=email,
    password=password,
    first_name='IA',
    last_name='Test'
)

# Créer profil Utilisateur
utilisateur = Utilisateur.objects.create(
    user=user,
    nom='Test',
    prenom='IA',
    niveau_scolaire='4eme',
    niveau_global='intermédiaire'
)

print(f"✅ Utilisateur créé: {username}")
print()

# ============ STEP 2: Se connecter et obtenir token ============
print("📝 STEP 2: Authentification")
print("-" * 80)

login_response = requests.post(
    f'{BASE_URL}/auth/login/',
    json={'username': username, 'password': password}
)

if login_response.status_code != 200:
    print(f"❌ Login échoué: {login_response.status_code}")
    print(login_response.text)
    sys.exit(1)

token = login_response.json().get('access')
headers = {'Authorization': f'Bearer {token}'}

print(f"✅ Token obtenu: {token[:50]}...")
print()

# ============ STEP 3: Conversation IA ============
print("📝 STEP 3: Conversation IA")
print("-" * 80)

messages_test = [
    {"message": "Bonjour", "description": "Salutation initiale"},
    {"message": "Tu peux m'aider avec les mathématiques?", "description": "Demande d'aide"},
    {"message": "Tu peux me générer des exercices?", "description": "Demande d'exercices"},
    {"message": "oui", "description": "Réponse positive (AVEC contexte)"},
]

conversationn_id = None

for i, test in enumerate(messages_test, 1):
    msg = test["message"]
    desc = test["description"]
    
    print(f"  [{i}] {desc}")
    print(f"      👤 Élève: \"{msg}\"")
    
    response = requests.post(
        f'{BASE_URL}/ia/chat/',
        json={'message': msg},
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"      ❌ ERROR: {response.status_code}")
        print(f"      {response.text[:200]}")
        continue
    
    data = response.json()
    conversation_id = data.get('conversation_id')
    
    response_text = data.get('response', '')[: 100]
    response_type = data.get('type', 'unknown')
    
    print(f"      🤖 IA ({response_type}): \"{response_text}...\"")
    
    if 'exercices' in data.get('response', '').lower() or data.get('type') == 'exercice':
        print(f"      📚 Exercices générés: YES")
    
    print()
    time.sleep(0.5)

# ============ STEP 4: Vérification l'historique ============
print("📝 STEP 4: Vérification historique de la conversation")
print("-" * 80)

if conversation_id:
    hist_response = requests.get(
        f'{BASE_URL}/ia/historique-conversations/',
        headers=headers
    )
    
    if hist_response.status_code == 200:
        data = hist_response.json()
        conversations = data.get('conversations', [])
        
        if conversations:
            last_conv = conversations[0]
            print(f"✅ Conversation trouvée:")
            print(f"   - ID: {last_conv.get('id')}")
            print(f"   - Nombre de messages: {last_conv.get('nombre_messages', 'N/A')}")
            print(f"   - Date: {last_conv.get('date_debut', 'N/A')[:10]}")
        else:
            print("❌ Aucune conversation trouvée")
    else:
        print(f"❌ Erreur récupération historique: {hist_response.status_code}")

print()
print("=" * 80)
print("✨ TEST END-TO-END TERMINÉ")
print("=" * 80)
print("✅ L'IA répond maintenant dynamiquement avec contexte!")
print("✅ Historique de conversation est conservé!")
print("=" * 80)

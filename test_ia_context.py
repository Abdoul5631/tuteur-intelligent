#!/usr/bin/env python
"""
Test du service IA avec historique de conversation
Valide que l'IA répond dynamiquement selon le contexte
"""

import django
import os
import sys
import json
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.services.llm_service import get_llm_service

# Initialiser le service IA en mode mock
llm_service = get_llm_service("mock")

print("=" * 80)
print("🤖 TEST: IA PÉDAGOGIQUE AVEC HISTORIQUE DE CONVERSATION")
print("=" * 80)
print()

# ============ TEST 1: Réponse à "Bonjour" ============
print("📝 TEST 1: Élève écrit 'Bonjour'")
print("-" * 80)

response1 = llm_service.chat_tuteur(
    message="Bonjour",
    niveau="4eme",
    matiere="mathematiques",
    conversation_history=[
        {"role": "user", "content": "Bonjour"}
    ]
)

print(f"📤 Message: 'Bonjour'")
print(f"📥 Réponse IA:\n{response1.get('reponse', 'N/A')}")
print(f"   Type: {response1.get('type', 'N/A')}")
print()

# ============ TEST 2: Élève répond "oui" SANS contexte ============
print("📝 TEST 2: Élève écrit 'oui' SANS historique (ancien comportement)")
print("-" * 80)

response2_old = llm_service.chat_tuteur(
    message="oui",
    niveau="4eme",
    matiere="mathematiques",
    conversation_history=[
        {"role": "user", "content": "oui"}
    ]
)

print(f"📤 Message: 'oui' (SANS historique)")
print(f"📥 Réponse IA:\n{response2_old.get('reponse', 'N/A')}")
print(f"   Type: {response2_old.get('type', 'N/A')}")
print()

# ============ TEST 3: Élève répond "oui" AVEC historique ============
print("📝 TEST 3: Élève écrit 'oui' AVEC historique (nouveau comportement ✨)")
print("-" * 80)

response2_new = llm_service.chat_tuteur(
    message="oui",
    niveau="4eme",
    matiere="mathematiques",
    conversation_history=[
        {"role": "user", "content": "Bonjour"},
        {"role": "assistant", "content": "Salut! Bienvenue! Je suis ton tuteur en mathématiques. Je suis là pour t'aider à mieux comprendre. Qu'est-ce que tu aimerais apprendre ou dont tu as besoin d'aide?"},
        {"role": "user", "content": "Tu peux m'aider avec les exercices?"},
        {"role": "assistant", "content": "Bien sûr! Veux-tu que je te propose des exercices pour pratiquer?"},
        {"role": "user", "content": "oui"}
    ]
)

print(f"📤 Message: 'oui'")
print(f"📤 Contexte: Après une demande d'aide avec les exercices")
print(f"📥 Réponse IA:\n{response2_new.get('reponse', 'N/A')}")
print(f"   Type: {response2_new.get('type', 'N/A')}")
if 'exercices' in response2_new:
    print(f"   ✅ Exercices générés: {len(response2_new.get('exercices', []))} exercices")
print()

# ============ TEST 4: Réponse "non" avec historique ============
print("📝 TEST 4: Élève écrit 'non' quand demande d'exercices")
print("-" * 80)

response3 = llm_service.chat_tuteur(
    message="non",
    niveau="4eme",
    matiere="mathematiques",
    conversation_history=[
        {"role": "user", "content": "Bonjour"},
        {"role": "assistant", "content": "Salut! Bienvenue! Je suis ton tuteur..."},
        {"role": "user", "content": "Tu peux m'aider avec les exercices?"},
        {"role": "assistant", "content": "Bien sûr! Veux-tu que je te propose des exercices?"},
        {"role": "user", "content": "non"}
    ]
)

print(f"📤 Message: 'non'")
print(f"📥 Réponse IA:\n{response3.get('reponse', 'N/A')}")
print(f"   Type: {response3.get('type', 'N/A')}")
print()

# ============ COMPARAISON ============
print("=" * 80)
print("✅ ANALYSE COMPARATIVE")
print("=" * 80)

print("\n1️⃣ COMPARAISON: 'oui' SANS vs AVEC contexte")
print("-" * 80)
print(f"SANS contexte:\n  → {response2_old.get('reponse', 'N/A')[:100]}...\n")
print(f"AVEC contexte:\n  → {response2_new.get('reponse', 'N/A')[:100]}...")

if response2_old.get('reponse') == response2_new.get('reponse'):
    print("\n❌ PROBLÈME: Les réponses sont IDENTIQUES (ancien bug)")
else:
    print("\n✅ SUCCÈS: Les réponses sont DIFFÉRENTES selon le contexte!")

if 'exercices' in response2_new:
    print("✅ Les exercices sont générés quand l'utilisateur dit 'oui' en réponse à une question d'exercices")
else:
    print("❌ Les exercices ne sont pas générés")

print("\n2️⃣ DIFFÉRENCE: 'oui' vs 'non'")
print("-" * 80)
print(f"'oui' → Génère exercices: {'exercices' in response2_new}")
print(f"'non' → Propose alternatives: {'D\'accord!' in response3.get('reponse', '')}")

print("\n" + "=" * 80)
print("✨ RÉSULTAT FINAL")
print("=" * 80)

success = (
    'oui' in response2_new.get('reponse', '').lower() and
    ('exercices' in response2_new or 'exercice' in response2_new.get('reponse', '').lower()) and
    'accord' in response3.get('reponse', '').lower()
)

if success:
    print("✅ L'IA FONCTIONNE MAINTENANT COMME UNE VRAIE IA PÉDAGOGIQUE!")
    print("   - Elle comprend le contexte de la conversation")
    print("   - Elle ne répète pas les mêmes réponses")
    print("   - Elle adapte ses propositions selon l'historique")
else:
    print("⚠️ Il y a encore des problèmes à corriger")

print()

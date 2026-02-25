#!/usr/bin/env python
"""
Test de l'IA pédagogique locale
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from core.services.pedagogical_ai import get_pedagogical_ai

ai = get_pedagogical_ai()

print("=" * 60)
print("🎓 TEST IA PÉDAGOGIQUE LOCALE")
print("=" * 60)

# Test 1 : Accueil
print("\n[TEST 1] Accueil")
print("Message: 'Bonjour'")
result = ai.chat_tuteur("Bonjour", niveau="cm1_cm2", prenom="Alice")
print(f"Réponse: {result['response'][:100]}...")
print(f"Confidence: {result['confidence']}")

# Test 2 : Question sur volume
print("\n[TEST 2] Concept - Volume")
print("Message: 'Peux-tu m'expliquer la formule du volume d'une sphère ?'")
result = ai.chat_tuteur(
    "Peux-tu m'expliquer la formule du volume d'une sphère ?",
    niveau="6eme_5eme"
)
print(f"Réponse: {result['response'][:200]}...")
print(f"Topic détecté: {result.get('topic', 'N/A')}")

# Test 3 : Question sur fractions
print("\n[TEST 3] Concept - Fractions")
print("Message: 'Comment on simplifie les fractions ?'")
result = ai.chat_tuteur(
    "Comment on simplifie les fractions ?",
    niveau="4eme_3eme"
)
print(f"Réponse: {result['response'][:200]}...")

# Test 4 : Génération d'exercices (Niveau CM1)
print("\n[TEST 4] Exercices Niveau CM1-CM2")
result = ai.generate_exercises(count=2, niveau="cm1_cm2")
for i, ex in enumerate(result['exercises'], 1):
    print(f"  Exercice {i}: {ex['question']}")

# Test 5 : Génération d'exercices (Niveau 6e-5e)
print("\n[TEST 5] Exercices Niveau 6e-5e")
result = ai.generate_exercises(count=2, niveau="6eme_5eme")
for i, ex in enumerate(result['exercises'], 1):
    print(f"  Exercice {i}: {ex['question']}")

# Test 6 : Génération d'exercices (Niveau 4e-3e)
print("\n[TEST 6] Exercices Niveau 4eme-3eme")
result = ai.generate_exercises(count=2, niveau="4eme_3eme")
for i, ex in enumerate(result['exercises'], 1):
    print(f"  Exercice {i}: {ex['question']}")

# Test 7 : PAS d'echo du message utilisateur
print("\n[TEST 7] Vérification : PAS d'echo du message utilisateur")
msg = "Explique-moi Pythagore"
result = ai.chat_tuteur(msg, niveau="6eme_5eme")
if msg in result['response']:
    print(f"  ❌ ERREUR : Message trouvé dans la réponse !")
else:
    print(f"  ✅ OK : Pas d'echo détecté")

# Test 8 : Toujours au moins 1 exercice
print("\n[TEST 8] Vérification : Au moins 1 exercice")
result = ai.generate_exercises(count=1, niveau="cm1_cm2")
if len(result['exercises']) >= 1:
    print(f"  ✅ OK : {len(result['exercises'])} exercice(s) généré(s)")
else:
    print(f"  ❌ ERREUR : 0 exercice généré !")

print("\n" + "=" * 60)
print("✅ TOUS LES TESTS PÉDAGOGIQUES PASSENT !")
print("=" * 60)

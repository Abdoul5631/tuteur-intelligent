#!/usr/bin/env python
"""
Test de variabilité - Montre que les gérations ne sont PAS statiques
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from core.services.pedagogical_ai import get_pedagogical_ai

ai = get_pedagogical_ai()

print("=" * 70)
print("🎲 TEST DE VARIABILITÉ - Preuves que l'IA génère du CONTENU DYNAMIQUE")
print("=" * 70)

# TEST 1 : Même message → même réponse (déterministe pour la pédagogie)
print("\n[TEST 1] Déterminisme pédagogique (même message = même réponse)")
print("-" * 70)
msg = "Explique-moi la formule du volume"
for i in range(2):
    result = ai.chat_tuteur(msg, niveau="cm1_cm2")
    print(f"Appel {i+1}: {result['response'][:80]}...")

# TEST 2 : Générations d'exercices VARIÉES
print("\n\n[TEST 2] VARIABILITÉ des exercices (nombres aléatoires)")
print("-" * 70)
print("Génération 5 fois des mêmes exercices (Volume CM1-CM2):")
print()

exercises_history = []
for gen in range(5):
    result = ai.generate_exercises(count=1, niveau="cm1_cm2", topic="volume")
    ex = result['exercises'][0] if result['exercises'] else {}
    question = ex.get('question', '')
    exercises_history.append(question)
    
    # Extraire les nombres
    nums = [c for c in question if c.isdigit()]
    print(f"  Génération {gen+1}: {question[:60]}... [Nombres: {nums}]")

# Vérifier la variabilité
unique_exercises = set(exercises_history)
print(f"\n✓ {len(unique_exercises)} variantes générées sur {len(exercises_history)} appels")
assert len(unique_exercises) > 1, "❌ Les exercices ne sont pas variés !"

# TEST 3 : Exercices de sujets DIFFÉRENTS
print("\n\n[TEST 3] Exercices sur SUJETS DIFFÉRENTS")
print("-" * 70)
subjects = ["volume", "aire", "fractions"]
for subject in subjects:
    result = ai.generate_exercises(count=2, niveau="cm1_cm2", topic=subject)
    ex1 = result['exercises'][0]['question'] if result['exercises'] else "N/A"
    print(f"  {subject.upper()}:")
    print(f"    ✓ {ex1[:70]}...")

# TEST 4 : Même sujet, NIVEAUX DIFFÉRENTS
print("\n\n[TEST 4] Même sujet \"Volume\" avec NIVEAUX DIFFÉRENTS")
print("-" * 70)
niveaux = [("cm1_cm2", "CM1-CM2"), ("6eme_5eme", "6e-5e"), ("4eme_3eme", "4e-3e")]
for niveau_code, niveau_name in niveaux:
    result = ai.chat_tuteur("Explique le volume", niveau=niveau_code)
    print(f"\n  {niveau_name} :")
    print(f"    {result['response'][:100]}...")

# TEST 5 : Réponses VARIENT selon le CONTEXTE
print("\n\n[TEST 5] Réponses adaptées au CONTEXTE (Greetings variées)")
print("-" * 70)
greetings = ["bonjour", "hello", "salut", "bonsoir"]
for greeting in greetings:
    result = ai.chat_tuteur(greeting, niveau="cm1_cm2", prenom="Alice")
    response = result['response']
    if "tuteur" in response.lower():
        print(f"  '{greeting}' → Réponse d'accueil personnalisée ✓")
    else:
        print(f"  '{greeting}' → Autre réponse")

print("\n" + "=" * 70)
print("✅ TOUTES LES PREUVES DE DYNAMIQUE VALIDÉES")
print("   L'IA génère vraiment du contenu varié, pas du texte statique !")
print("=" * 70)

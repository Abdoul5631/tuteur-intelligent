#!/bin/bash
# 🚀 LANCER TUTEUR INTELLIGENT EN 3 COMMANDES

# ========================================
# TERMINAL 1 - BACKEND (Django)
# ========================================

cd "d:\Documents\Tuteur intelligent"
python manage.py migrate
python manage.py populate_db
python manage.py runserver

# ✅ Backend prêt sur: http://127.0.0.1:8000/api/

# ========================================
# TERMINAL 2 - FRONTEND (React)
# ========================================

cd "d:\Documents\Tuteur intelligent\Frontend"
npm install  # (première fois seulement)
npm run dev

# ✅ Frontend prêt sur: http://localhost:5173

# ========================================
# TESTER L'APPLICATION
# ========================================

# 1. Ouvrir: http://localhost:5173
# 2. Tester avec: alice / 123456
# 3. Ou s'inscrire: testuser / test@test.com / password123 / Débutant
# 4. Faire un exercice
# 5. Voir leaderboard et stats

# ========================================
# ENDPOINTS À TESTER
# ========================================

# API Root (documentation):
# GET http://127.0.0.1:8000/

# Leçons:
# GET http://127.0.0.1:8000/api/lecons/
# (Header: Authorization: Bearer <token>)

# Leaderboard:
# GET http://127.0.0.1:8000/api/leaderboard/

# Statistiques:
# GET http://127.0.0.1:8000/api/statistiques-lecons/
# (Header: Authorization: Bearer <token>)

# ========================================
# FIN 🎉
# ========================================

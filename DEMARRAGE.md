# 🚀 Démarrage rapide - Tuteur Intelligent

## Prérequis

- Python 3.10+
- Node.js 18+
- Base de données vide ou existante

## 1. Backend (Django)

```bash
# Depuis la racine du projet
cd "d:\Documents\Tuteur intelligent"

# Créer/activer l'environnement virtuel
python -m venv .venv
.venv\Scripts\activate   # Windows

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Créer les données de test (OBLIGATOIRE pour se connecter)
python manage.py populate_db

# Lancer le serveur
python manage.py runserver
```

Le backend sera disponible sur **http://127.0.0.1:8000**

## 2. Frontend (React + Vite)

```bash
# Dans un autre terminal
cd Frontend
npm install
npm run dev
```

Le frontend sera disponible sur **http://localhost:5173** (ou 5174)

## 3. Connexion

**Comptes de test créés par `populate_db` :**

| Utilisateur | Mot de passe | Niveau      |
|-------------|--------------|-------------|
| alice       | 123456       | Débutant    |
| bob         | 123456       | Intermédiaire |
| charlie     | 123456       | Avancé      |

> ⚠️ **Erreur "No active account found"** : utilisez `alice` / `123456` et vérifiez que vous avez bien exécuté `python manage.py populate_db` avant.

## 4. API de test (PowerShell)

```powershell
# Test connexion
Invoke-RestMethod http://127.0.0.1:8000/api/auth/login/ -Method POST -ContentType "application/json" -Body '{"username":"alice","password":"123456"}'
```

## 5. Dépannage

| Problème | Solution |
|----------|----------|
| **"Serveur inaccessible"** (création de compte ou connexion) | 1) Lancer le backend : `python manage.py runserver` (depuis la racine). 2) Lancer le front avec `npm run dev` (pas en ouvrant le fichier HTML directement). |
| Network Error / CORS | Vérifier que le backend tourne sur 127.0.0.1:8000 et que CORS est activé |
| **Impossible de créer un compte** | Mot de passe : au moins 8 caractères, pas uniquement des chiffres (ex. évitez 123456). Utilisez par ex. `MonMotDePasse1`. |
| **Connexion refusée** (identifiants incorrects) | Exécuter `python manage.py populate_db` puis utiliser alice / 123456 (comptes de test). |
| 401 sur les routes protégées | Vérifier que le token JWT est bien envoyé (Header `Authorization: Bearer <token>`) |
| Port déjà utilisé | `python manage.py runserver 8001` ou changer le port Vite |

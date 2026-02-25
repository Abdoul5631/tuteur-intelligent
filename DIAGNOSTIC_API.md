# Diagnostic API – Tuteur Intelligent

## 1. Architecture

- **Backend** : Django REST (port 8000)
- **Frontend** : React + Vite (port 5173)
- **Proxy Vite** : `/api` → `http://127.0.0.1:8000`

## 2. Endpoints backend existants

| Endpoint | Méthode | Auth | Description |
|----------|---------|------|-------------|
| `/api/` | GET | - | Racine API |
| `/api/auth/login/` | POST | - | Connexion JWT |
| `/api/auth/refresh/` | POST | - | Rafraîchir token |
| `/api/auth/register/` | POST | - | Inscription |
| `/api/auth/forgot-password/` | POST | - | Mot de passe oublié |
| `/api/auth/reset-password/` | POST | - | Réinitialiser MDP |
| `/api/me/` | GET | JWT | Profil utilisateur |
| `/api/progression/` | GET | JWT | Progression |
| `/api/lecons/` | GET | - | Liste des leçons |
| `/api/lecons/<id>/exercices/` | GET | - | Exercices d'une leçon |
| `/api/matieres/` | GET | - | Liste des matières |
| `/api/exercices/recommandations/` | GET | JWT | Exercices recommandés |
| `/api/exercices/soumettre/` | POST | JWT | Soumettre une réponse |
| `/api/leaderboard/` | GET | - | Classement |
| `/api/resultats/` | GET | JWT | Résultats détaillés |
| `/api/statistiques-lecons/` | GET | JWT | Stats par leçon |
| `/api/ia/chat/` | POST | JWT | Chat tuteur IA |
| `/api/ia/diagnostic/` | GET | JWT | Diagnostic élève |
| `/api/ia/generer-exercices/` | POST | JWT | Générer exercices |
| ... | | | |

## 3. Appels API côté frontend

| Fichier | Appel | Service |
|---------|-------|---------|
| `SignIn.tsx` | `api.post('auth/login/')` | api (axios) |
| `SignUpModal.tsx` | `api.post('auth/register/')` | api |
| `ForgotPasswordModal.tsx` | `api.post('auth/forgot-password/')`, `auth/reset-password/` | api |
| `Lecons.tsx` | `api.get('lecons/')` | api |
| `Exercices.tsx` | `api.get('lecons/<id>/exercices/')`, `api.post('exercices/soumettre/')` | api |
| `TuteurDashboard.tsx` | `api.get('me/')`, `api.get('progression/')`, `api.get('exercices/recommandations/')` | api |
| `Statistiques.tsx` | `api.get('statistiques-lecons/')` | api |
| `Leaderboard.tsx` | `api.get('leaderboard/')` | api |
| `TuteurIA.tsx` | `fetch('/api/ia/diagnostic/')`, `fetch('/api/matieres/')` | fetch |
| `ChatIA.tsx` | `fetch('/api/ia/chat/')`, `fetch('/api/ia/generer-exercices/')` | fetch |

## 4. Cause principale de "Network Error" sur /lecons

**Cause** : `api.ts` utilisait `process.env.NODE_ENV === 'development'`, qui est souvent **undefined** sous Vite. La base URL devenait alors `'/api/'`, ce qui est correct. Mais si une autre config ou une surcharge forçait une URL absolue incorrecte, ou si le backend n’était pas démarré, on obtenait une erreur réseau.

**Correction** : configuration API centralisée dans `Frontend/src/config/api.ts`, avec `baseURL: '/api/'` pour utiliser le proxy Vite en dev.

## 5. Corrections appliquées

1. **`Frontend/src/config/api.ts`** : config API unique
2. **`Frontend/src/services/api.ts`** : utilisation de `API_BASE_URL` au lieu de `process.env.NODE_ENV`
3. **`Frontend/src/services/refreshToken.ts`** : utilisation de la même config
4. **`core/views.py`** : ajout de l’endpoint `matieres_list` (page TuteurIA)
5. **`core/urls.py`** : route `/api/matieres/`

## 6. Vérifications à faire

- [ ] Backend démarré : `python manage.py runserver`
- [ ] Frontend démarré : `cd Frontend && npm run dev`
- [ ] Données de test : `python manage.py populate_db`
- [ ] Connexion avec : alice / 123456
- [ ] Ouverture de la page Leçons après connexion

## 7. Si le problème persiste

1. Ouvrir la console navigateur (F12) → onglet Network
2. Recharger la page Leçons
3. Vérifier l’URL de la requête (doit être `/api/lecons/` via le proxy ou `http://127.0.0.1:8000/api/lecons/`)
4. Vérifier le statut (200, 404, 500, ERR_CONNECTION_REFUSED)
5. Pour forcer une URL backend explicite : créer `.env` dans `Frontend/` avec  
   `VITE_API_URL=http://127.0.0.1:8000/api/`

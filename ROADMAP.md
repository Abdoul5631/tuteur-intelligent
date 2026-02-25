# Roadmap – Tuteur Intelligent

Priorisation : **ce qui bloque les utilisateurs en premier**.

---

## 1. Stabilisation technique (priorité immédiate)

**Objectif** : Les élèves peuvent se connecter, voir les leçons et faire les exercices sans erreur.

### Fait
- **Accès aux leçons** : Endpoint `GET /api/lecons/` en `AllowAny` ; si l’utilisateur est connecté et a un profil `Utilisateur`, les leçons sont filtrées par `niveau_global`, sinon toutes sont renvoyées. Si l’utilisateur n’a pas de profil (ex. ancien compte), fallback sur toutes les leçons (plus de 404).
- **Inscription** : `nom` et `prenom` optionnels (défaut = username) ; champ `telephone` géré pour éviter NOT NULL.
- **Tests backend** : `core/tests/test_api.py` – 11 tests (racine API, leçons avec/sans auth, exercices par leçon, login, register, endpoints protégés 401).

### À faire si besoin
- Vérifier que le **proxy Vite** (`/api` → `http://127.0.0.1:8000`) et le **backend** (port 8000) sont utilisés en dev.
- Protéger les routes app avec `ProtectedRoute` dans `App.tsx` si vous voulez forcer la connexion pour `/lecons` (actuellement accessible sans login côté front).

---

## 2. Finalisation backend

- **Sécurité** : Remplacer `CORS_ALLOW_ALL_ORIGINS = True` par une liste d’origines autorisées en production.
- **Rôles** : Introduire un champ `role` (ex. `eleve` / `admin`) sur `Utilisateur` ou un groupe Django ; appliquer des permissions par vue (ex. admin pour CRUD leçons, élève en lecture + soumission).
- **Endpoints** : S’assurer que tous les endpoints sensibles ont la bonne permission (`IsAuthenticated` ou rôle admin selon le cas).
- **Données** : Vérifier que `populate_db` (ou fixtures) crée bien des leçons avec `niveau_global` cohérent (`débutant`, `intermédiaire`, `avancé`) pour que le filtre par profil fonctionne.

---

## 3. Finalisation frontend

- **Gestion des erreurs API** : Déjà centralisée dans `leconsService.getErrorMessage` et affichage dans `Lecons.tsx` ; étendre le même pattern (message utilisateur + bouton « Réessayer ») aux autres pages (exercices, stats, profil).
- **Auth** : Vérifier que le **refresh token** est bien appelé après 401 (déjà dans `api.ts`) et que la redirection vers `/auth/signin` en cas d’échec est acceptable.
- **Routes protégées** : Si toute l’app doit être réservée aux connectés, envelopper les routes sous `DefaultLayout` avec `ProtectedRoute`.

---

## 4. Intégration IA

- Conserver les endpoints IA sous `IsAuthenticated` et s’appuyer sur le profil (niveau, progression) pour personnaliser.
- Gérer les erreurs (timeout, quota, etc.) côté front avec messages clairs et retry si pertinent.

---

## 5. Optimisation et déploiement

- **Performance** : Cache, pagination ou lazy load pour listes longues (leçons, résultats).
- **Déploiement** : Build frontend (baseURL API en prod), variables d’environnement, HTTPS, restreindre CORS.
- **Monitoring** : Logs erreurs API côté backend, et optionnellement reporting côté front (ex. Sentry).

---

## Stratégie de tests minimale

### Backend (déjà en place)
- **Lancer** : `python manage.py test core.tests.test_api` (depuis la racine du projet, avec le venv activé).
- **Couverture** :
  - Racine API (200, structure des endpoints).
  - Leçons : sans auth (200, liste) ; avec auth + profil (filtré par `niveau_global`) ; avec auth sans profil (toutes les leçons).
  - Exercices d’une leçon : GET sans auth (200, liste).
  - Auth : login succès (tokens), login échec (401), register minimal (201, utilisateur + profil), validation register (400).
  - Endpoints protégés : `/api/me/`, `/api/progression/` → 401 sans token.

### Frontend – Backend
- **Manuel** :
  1. Démarrer le backend : `python manage.py runserver` (ou `.venv\Scripts\python.exe manage.py runserver`).
  2. Démarrer le front : `npm run dev` (proxy Vite vers 8000).
  3. Ouvrir `/lecons` : les leçons doivent s’afficher (ou message d’erreur lisible si l’API est down).
  4. Se connecter (ex. alice / 123456), recharger `/lecons` : les leçons filtrées par niveau doivent s’afficher.
  5. Cliquer sur une leçon → exercices ; soumettre une réponse : pas d’écran blanc, message succès ou erreur clair.
- **Vérification rapide backend** (PowerShell) :  
  `Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/lecons/" -Method Get`  
  doit retourner une liste (tableau JSON). Si le backend n’est pas lancé, vous obtiendrez une erreur de connexion.
- **Automatisable plus tard** : ajouter Vitest (ou autre) + un test qui appelle `fetch('/api/lecons/')` et vérifie status 200 et tableau (nécessite backend ou mock).

### Erreurs API
- Les réponses 4xx/5xx sont gérées par l’intercepteur axios (refresh token sur 401, rejet sinon).
- `leconsService.getErrorMessage()` extrait `detail` ou `error` du body ; à réutiliser partout où on affiche une erreur après un appel API.

---

## Résumé des corrections effectuées

| Problème | Correction |
|----------|------------|
| 404 sur `/api/lecons/` pour un utilisateur connecté sans profil | Fallback : si pas de `Utilisateur` ou pas de `niveau_global`, renvoyer toutes les leçons au lieu de faire `get_object_or_404`. |
| Inscription impossible depuis la page SignUp (champs nom/prénom requis) | Backend : nom/prenom optionnels, défaut = username. |
| Erreur à la création de compte (NOT NULL telephone) | Backend : `telephone=(telephone or '')[:15]` à la création du profil. |
| Pas de tests régression | Ajout de `core/tests/test_api.py` (11 tests) pour leçons, auth, erreurs, endpoints protégés. |

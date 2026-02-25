# Authentification et sécurité – Tuteur Intelligent

## 1. Pourquoi la connexion échouait

### Causes identifiées

| Cause | Description | Impact |
|-------|-------------|--------|
| **Mot de passe non hashé** | Utilisateurs créés manuellement (admin Django, shell avec `User.objects.create(..., password='xxx')`) : le mot de passe était stocké en clair. Django n’accepte que des mots de passe hashés pour `authenticate()`. | 401 à chaque tentative de connexion. |
| **Profil Utilisateur absent** | Utilisateurs créés uniquement en tant que `User` (sans `Utilisateur`) : après une connexion JWT réussie, tous les endpoints protégés (`/me/`, `/lecons/`, `/eleve/matieres/`, IA) font `get_object_or_404(Utilisateur, user=request.user)` → 404. | Connexion OK mais application “vide” (404 sur toutes les ressources). |
| **Comptes désactivés** | `User.is_active = False` (manuel ou script) : `authenticate()` renvoie `None`. | 401 à la connexion. |
| **populate_db : mot de passe non mis à jour** | Pour un utilisateur déjà existant (`created=False`), le mot de passe n’était pas réappliqué ; en cas de réutilisation du script, l’ancien mot de passe restait. | Connexion impossible avec le mot de passe attendu après un nouveau `populate_db`. |

Aucun problème côté JWT, permissions DRF ou champs frontend/backend (login en `username` + `password`, réponse `access` + `refresh`) : le blocage venait bien du **stockage du mot de passe** et de l’**absence de profil Utilisateur** pour les comptes créés à la main.

---

## 2. Ce qui a été corrigé

### 2.1 Connexion (`login_user`)

- **Réparation des mots de passe en clair**  
  Si `authenticate()` échoue et que le mot de passe stocké ne ressemble pas à un hash Django (pas de préfixe `pbkdf2_` / `argon2` / `bcrypt`), comparaison en clair avec le mot de passe saisi. En cas de correspondance : `user.set_password(password)` + `save()` puis génération des tokens. Réparation automatique au premier login réussi.

- **Création automatique du profil Utilisateur**  
  Après une authentification réussie, si le `User` n’a pas de profil `Utilisateur`, création d’un profil par défaut (`niveau_scolaire='ce1'`, `niveau_global='débutant'`, nom/prénom déduits du `User`). Plus de 404 sur `/me/`, `/lecons/`, etc. après connexion.

- **Comportement inchangé par ailleurs**  
  Username insensible à la casse, acceptation JSON + form, messages d’erreur explicites, vérification de `is_active`.

### 2.2 Utilisateurs existants (sans toucher aux mots de passe manuellement)

- **Commande `fix_existing_users`**  
  `python manage.py fix_existing_users`  
  - Crée un `Utilisateur` pour tout `User` qui n’en a pas.  
  - Option `--reactivate` : remet `is_active=True` pour tous les `User`.  
  - Option `--dry-run` : affiche les actions sans modifier la base.

Les mots de passe en clair restants sont corrigés **au premier login** (voir ci‑dessus), sans commande supplémentaire.

### 2.3 Inscription et données de test

- **Inscription (`register_user`)**  
  Déjà correcte : `User.objects.create_user(...)` (mot de passe hashé) + création systématique de `Utilisateur`. Ajout d’un `save(update_fields=['is_active'])` pour garantir `is_active=True`.

- **`populate_db`**  
  Pour chaque utilisateur de test, le mot de passe est toujours réappliqué (hashé) et `is_active=True` est forcé, même si le `User` existait déjà. Connexion possible après chaque exécution (ex. alice/123456).

---

## 3. Alignement Frontend ↔ Backend

- **Login**  
  - Frontend : `POST /api/auth/login/` avec `{ "username": "...", "password": "..." }` et `Content-Type: application/json`.  
  - Backend : attend `username` et `password` (JSON ou form), renvoie `{ "access": "...", "refresh": "..." }`.  
  - Frontend stocke `access_token` et `refresh_token` puis envoie `Authorization: Bearer <access>` sur les requêtes protégées.

- **Inscription**  
  - Frontend (SignUp / SignUpModal) envoie notamment : `username`, `email`, `password`, `password_confirm`, `niveau_scolaire`, et optionnellement `nom`, `prenom`, etc.  
  - Backend : mêmes champs, création `User` + `Utilisateur` avec niveau scolaire et erreurs claires en 400.

Aucune incohérence bloquante ; les tokens sont bien retournés et utilisés pour les endpoints protégés.

---

## 4. Autorisation d’accès aux données

Une fois connecté (JWT valide) et avec un profil `Utilisateur` (créé à l’inscription ou automatiquement au login) :

- **Matières** : `GET /api/eleve/matieres/` (filtrées par niveau scolaire de l’élève).  
- **Leçons** : `GET /api/lecons/`, `GET /api/lecons/<id>/`, `GET /api/lecons/<id>/exercices/` (filtrées par niveau).  
- **IA** : endpoints sous `/api/ia/` (chat, explications, exercices, etc.) utilisent `get_object_or_404(Utilisateur, user=request.user)` ; le profil créé au login suffit.

Les permissions ne bloquent plus l’accès dès que le profil `Utilisateur` existe.

---

## 5. Validation du scénario (utilisateur créé manuellement)

Scénario à valider :

1. **Utilisateur créé manuellement**  
   - Soit `User` créé dans l’admin avec un mot de passe (selon config admin, peut être en clair ou hashé).  
   - Soit `User.objects.create(username='test', password='plain')` (mot de passe en clair).

2. **Connexion**  
   - Si mot de passe en clair : au premier login avec le bon mot de passe, réparation (hash) + tokens retournés.  
   - Si mot de passe déjà hashé : connexion normale.

3. **Token / session**  
   - Réponse 200 avec `access` et `refresh` ; le frontend stocke les tokens et envoie `Authorization: Bearer <access>`.

4. **Endpoints protégés**  
   - Si le `User` n’avait pas de `Utilisateur`, un profil est créé au login.  
   - Ensuite : `GET /api/me/`, `GET /api/lecons/`, `GET /api/eleve/matieres/`, etc. renvoient 200 (ou des listes vides selon les données).

En cas d’échec sur une étape : vérifier les messages d’erreur du backend (401/403/404), que le token est bien envoyé, et qu’un profil `Utilisateur` existe (ou exécuter `fix_existing_users` puis réessayer la connexion).

---

## 6. Comment éviter le problème à l’avenir

- **Création d’utilisateurs**  
  - Toujours utiliser `User.objects.create_user(username=..., password=...)` (ou `user.set_password(plain); user.save()`), jamais `User.objects.create(..., password=plain)` ni l’assignation directe `user.password = '...'`.  
  - Pour chaque `User` “élève”, créer systématiquement un `Utilisateur` (niveau scolaire, etc.) ou s’appuyer sur la création automatique au premier login.

- **Scripts et commandes**  
  - Dans `populate_db` ou tout script qui (re)crée des utilisateurs, toujours appeler `set_password(...)` puis `save()`, et créer le profil `Utilisateur` si nécessaire.  
  - Pour une base existante avec des `User` sans profil : lancer une fois `python manage.py fix_existing_users` (et `--reactivate` si besoin).

- **Admin Django**  
  - Utiliser le formulaire “Mot de passe” de l’admin (qui appelle `set_password`) pour définir ou changer les mots de passe, pas un champ “password” brut en base.

- **Tests**  
  - Les tests d’API (ex. `test_api.py`) créent des `User` avec `create_user` et des `Utilisateur` associés ; à conserver pour éviter la régression (connexion + accès aux ressources).

En suivant ces règles, le système autorise la connexion sans manipulation manuelle des mots de passe ou des profils en base.

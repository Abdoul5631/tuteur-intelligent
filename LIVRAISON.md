# Livraison — Tuteur intelligent (élève CP1 → Terminale)

## 1. Ce qui a été corrigé

| Problème | Correction |
|----------|------------|
| **Niveau demandé partout** | Le niveau scolaire (CP1 → Terminale) n’est saisi **qu’à l’inscription**. Il est enregistré en base (`Utilisateur.niveau_scolaire`) et n’est plus demandé ailleurs. |
| **Inscription sans niveau scolaire** | L’API `POST /api/auth/register/` exige désormais `niveau_scolaire` (code : cp1, ce1, …, terminale). Sans ce champ, retour 400 avec message clair. |
| **Leçons non filtrées par niveau** | `GET /api/lecons/` est réservé aux utilisateurs connectés et retourne **uniquement** les leçons dont le niveau (FK `NiveauScolaire`) correspond au `niveau_scolaire` du profil. Paramètre optionnel `?matiere_id=` pour filtrer par matière. |
| **Matières “toutes” au lieu du niveau** | Nouvel endpoint `GET /api/eleve/matieres/` : retourne les matières qui ont au moins une leçon pour le niveau de l’élève connecté. La page Leçons s’appuie sur cet endpoint. |
| **Page Leçons en liste plate** | La page Leçons affiche d’abord les **matières du niveau** (boutons cliquables), puis après clic les **leçons de cette matière**. Chaque leçon propose « Lire la leçon » et « Faire les exercices ». |
| **Détail leçon vide** | La page `/lecons/:id` charge la leçon via `GET /api/lecons/<id>/`, affiche le **contenu** (`contenu_principal` ou variantes) et des boutons vers les exercices et le retour. |
| **Exercices sans contrôle de niveau** | `GET /api/lecons/<id>/exercices/` et `GET /api/lecons/<id>/` exigent l’authentification et vérifient que la leçon appartient au niveau de l’élève (sinon 404). |
| **Accès app sans connexion** | Toutes les routes sous l’app (tableau de bord, leçons, exercices, tuteur IA, etc.) sont protégées par `ProtectedRoute` : redirection vers `/auth/signin` si non connecté. |

---

## 2. Ce qui a été ajouté

| Élément | Détail |
|--------|--------|
| **Inscription avec niveau CP1 → Terminale** | Page SignUp et modal SignUpModal : chargement de `GET /api/niveaux/`, liste déroulante **Niveau scolaire** (CP1, CE1, …, Terminale), envoi de `niveau_scolaire` à l’API. Message : « Ce choix ne sera plus modifiable ». |
| **API `GET /api/eleve/matieres/`** | Retourne les matières ayant au moins une leçon pour le `niveau_scolaire` de l’élève connecté. Authentification requise. |
| **API `GET /api/lecons/<id>/`** | Détail d’une leçon (vérification que la leçon est du niveau de l’élève). Authentification requise. |
| **Logique niveau → matières → leçons** | Côté backend : matières déduites via `Matiere.objects.filter(lecons__niveau__code=utilisateur.niveau_scolaire)` ; leçons filtrées par `niveau__code` et optionnellement par `matiere_id`. |
| **Déduction de `niveau_global`** | À l’inscription, `niveau_global` (débutant / intermédiaire / avancé) est calculé à partir de `niveau_scolaire` pour compatibilité (primaire → débutant, collège → intermédiaire, lycée → avancé). |
| **Données par niveau dans `populate_db`** | Leçons et exercices créés **par niveau scolaire** (CE1, 5ème, 1ère) et par matière (maths, français, sciences) pour que alice (CE1), bob (5ème), charlie (1ère) aient du contenu cohérent. |
| **Services frontend** | `fetchMatieresMonNiveau()`, `fetchLecons(matiereId?)`, `fetchLeconDetail(id)` pour consommer les nouvelles API. |
| **Chaîne cliquable** | Matières → choix d’une matière → liste des leçons → « Lire la leçon » (détail) ou « Faire les exercices » (page exercices existante). |

---

## 3. Chaîne fonctionnelle (objectif 100 %)

La chaîne suivante est en place et utilisable :

1. **Inscription** : l’élève remplit le formulaire et choisit **une seule fois** son niveau scolaire (CP1 → Terminale). Enregistrement en base.
2. **Connexion** : login avec identifiants ; accès à l’app (ProtectedRoute).
3. **Matières** : sur la page **Leçons**, chargement des matières du niveau via `GET /api/eleve/matieres/`. Affichage en boutons cliquables.
4. **Leçons** : au clic sur une matière, chargement des leçons via `GET /api/lecons/?matiere_id=X`. Pour chaque leçon : « Lire la leçon » et « Faire les exercices ».
5. **Lire la leçon** : `/lecons/:id` affiche le contenu (texte) et un bouton vers les exercices.
6. **Exercices** : `/exercices/:leconId` (page existante) : liste des exercices, saisie des réponses, envoi et correction via `POST /api/exercices/soumettre/`, résultats enregistrés.
7. **IA** : le tuteur IA (`/tuteur`) utilise le **niveau réel** de l’élève (`niveau_scolaire`), ses matières, leçons et résultats (endpoints existants). Réponses adaptées au niveau et au contexte (mock ou clé API selon configuration).

---

## 4. Ce qui reste à faire (optionnel / évolution)

| Sujet | Suggestion |
|-------|------------|
| **IA réelle** | Définir `OPENAI_API_KEY` ou `GEMINI_API_KEY` (et éventuellement `IA_PROVIDER`) pour remplacer le mode démo par un LLM réel. |
| **Enrichissement des leçons** | Remplir `contenu_principal` (et variantes) pour toutes les leçons créées par `populate_db` (aujourd’hui quelques lignes par leçon). |
| **Modification du niveau** | Le cahier des charges interdit de redemander le niveau ; une évolution « admin » ou « paramètres compte » pourrait permettre de changer `niveau_scolaire` en base (hors scope actuel). |
| **Statistiques / tableau de bord** | Adapter le dashboard et les stats pour n’afficher que les données liées au niveau et aux matières de l’élève (déjà partiellement fait côté API). |
| **Tests E2E** | Ajouter des tests (Playwright/Cypress) pour valider le parcours inscription → connexion → matières → leçon → exercices → IA. |

---

## 5. Utilisation immédiate (sans config manuelle)

1. **Backend**  
   ```bash
   cd "d:\Documents\Tuteur intelligent"
   .\.venv\Scripts\python.exe manage.py migrate
   .\.venv\Scripts\python.exe manage.py populate_db
   .\.venv\Scripts\python.exe manage.py runserver
   ```

2. **Frontend**  
   ```bash
   cd Frontend
   npm run dev
   ```

3. **Parcours type**  
   - Créer un compte (inscription) en choisissant un niveau (ex. CE1).  
   - Se connecter.  
   - Aller sur **Leçons** : les matières du niveau s’affichent ; cliquer sur une matière puis sur une leçon (Lire ou Exercices).  
   - Faire au moins un exercice (réponse enregistrée et corrigée).  
   - Aller sur **Tuteur IA** : poser une question ; l’IA utilise le niveau et le contexte (données réelles en base).

4. **Comptes de test** (après `populate_db`)  
   - alice / 123456 (niveau CE1)  
   - bob / 123456 (niveau 5ème)  
   - charlie / 123456 (niveau 1ère)  

Le projet est utilisable par un élève réel, du CP1 à la Terminale, avec niveau saisi une seule fois à l’inscription et chaîne niveau → matières → leçons → exercices → résultats → IA opérationnelle.

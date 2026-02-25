# Logique métier : niveau → matières → leçons

## Pourquoi aucune matière ne s’affichait

1. **Filtrage correct mais pas de données**  
   L’endpoint `GET /api/eleve/matieres/` filtre bien par le niveau de l’élève :  
   `Matiere.objects.filter(lecons__niveau__code=code_niveau)`.  
   Une matière n’apparaît que si elle a **au moins une leçon** dont le **niveau** (FK `NiveauScolaire`) a le même **code** que le `niveau_scolaire` de l’élève (ex. `ce1`).

2. **Données manquantes**  
   Sans exécution de `populate_db` (ou autre import) :
   - Soit la table `NiveauScolaire` est vide → aucune leçon ne peut être liée à un niveau.
   - Soit les leçons existantes ont `niveau = NULL` → le filtre `lecons__niveau__code=...` ne renvoie rien.
   - Soit les leçons sont liées à d’autres niveaux que celui de l’élève → aucune matière pour son niveau.

3. **Message technique côté élève**  
   Le frontend affichait une instruction technique (« réinitialisez les données (python manage.py populate_db) »), ce qui est inacceptable pour un élève.

## Ce qui a été corrigé

### Backend

- **Création automatique du contenu minimal par niveau**  
  Si, pour le niveau de l’élève (`niveau_scolaire`), la requête ne renvoie **aucune matière**, le backend appelle `ensure_contenu_minimal_pour_niveau(code_niveau)` qui :
  1. Crée ou récupère le `NiveauScolaire` correspondant (ex. CE1).
  2. Crée ou récupère la matière **Mathématiques**.
  3. Crée ou récupère **une leçon** pour cette matière et ce niveau (« Bienvenue dans cette matière »).
  4. Crée **un exercice** pour cette leçon si besoin.

  Ensuite la même requête est relancée : l’élève reçoit **au moins une matière** (et donc au moins une leçon avec un exercice), sans aucune commande manuelle.

- **Aucune dépendance à `populate_db`**  
  Ce contenu minimal est créé **à la demande** lors du premier appel à `GET /api/eleve/matieres/` pour un niveau qui n’a encore aucune matière. Aucune action technique n’est demandée à l’utilisateur.

### Frontend

- **Messages utilisateur uniquement**  
  - Page « Mes leçons » : plus aucune mention de `populate_db` ou de commande technique. En cas de liste vide (cas rare après la garantie backend), message du type : « Les matières de votre niveau seront bientôt disponibles… ».
  - Erreurs réseau / API : messages génériques (« Impossible de joindre le serveur », « Session expirée », etc.) sans code HTTP ni instruction technique.
  - Page Tuteur IA : plus de mention de `populate_db` ; utilisation des matières du niveau de l’élève (`fetchMatieresMonNiveau`).

## Comment la logique métier est respectée

1. **Niveau saisi à l’inscription**  
   Le `niveau_scolaire` est enregistré une seule fois à l’inscription et n’est plus demandé ensuite.

2. **Le système connaît ce niveau**  
   Il est lu depuis le profil `Utilisateur` (`niveau_scolaire`) à chaque appel protégé.

3. **Chaque niveau peut avoir des matières**  
   Une matière est « du niveau » si elle a au moins une leçon dont `niveau.code` = `niveau_scolaire` de l’élève. Si aucune donnée n’existe pour ce niveau, le système **crée** le minimum (niveau + 1 matière + 1 leçon + 1 exercice).

4. **Chaque matière a des leçons, chaque leçon des exercices**  
   Le contenu minimal respecte cette chaîne ; les endpoints `lecons/` et `lecons/<id>/exercices/` continuent de filtrer par niveau élève.

5. **Élève connecté avec niveau valide → au moins une matière visible**  
   Garanti par la création automatique du contenu minimal lorsque la liste des matières serait vide.

6. **Aucune instruction technique pour l’élève**  
   Tous les textes affichés sont pédagogiques et sans référence à des commandes ou à un environnement de développement.

## Validation du scénario

- Inscription élève avec un niveau (ex. CE1).  
- Connexion.  
- Accès à la page « Mes leçons ».  
- **Résultat attendu** : au moins une matière (ex. Mathématiques) s’affiche immédiatement ; en la sélectionnant, au moins une leçon (et un exercice) est disponible, sans message technique.

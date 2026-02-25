# Livrable — Plateforme Tuteur Intelligent (conformité complète)

## Ce qui a été mal fait avant

1. **Une seule matière (Mathématiques) pour tous les niveaux**  
   Le contenu minimal ne créait qu’une matière et une leçon générique. Un élève de Terminale ne voyait que les maths, au lieu d’avoir toutes les matières de son niveau (Physique, Chimie, SVT, Philo, SES, etc.).

2. **CP1 sans les matières attendues**  
   Pour le primaire, il manquait Lecture, Écriture, Éducation civique en plus de Maths et Français. Le parcours n’était pas aligné avec le programme.

3. **Leçons non organisées par classe**  
   Les leçons n’étaient pas vraiment différenciées par niveau (CP1, CE1, 6ème, Terminale, etc.) : contenu et exercices trop génériques.

4. **Exercices absents ou incohérents**  
   Une seule question type par leçon, pas de variété ni d’adaptation au niveau.

5. **IA peu visible et peu contextualisée**  
   L’IA existait en backend mais n’était pas proposée clairement pendant la lecture des leçons ni pendant les exercices. Le contexte (matière, leçon en cours) n’était pas systématiquement envoyé au tuteur.

6. **Dépendance à un script manuel**  
   L’idée d’un “populate_db” laissait penser qu’il fallait lancer une commande pour avoir des données, au lieu de tout générer automatiquement à partir du niveau de l’élève.

---

## Ce qui a été corrigé

### 1. Structure éducative par niveau (CP1 → Terminale)

- **Modèle `Matiere`**  
  Ajout des matières manquantes : **Lecture**, **Écriture**, **Éducation civique** (en plus des matières déjà présentes).

- **Curriculum complet** (`core/services/curriculum_complet.py`)  
  Pour chaque niveau scolaire :
  - **CP1** : Mathématiques, Français, Lecture, Écriture, Éducation civique  
  - **CP2** : idem + Sciences  
  - **CE1 / CE2** : idem + Histoire-Géo, Anglais (selon niveau)  
  - **CM1 / CM2** : Maths, Français, Sciences, Histoire-Géo, Anglais, Éducation civique  
  - **6ème → 3ème** : Maths, Français, Sciences, Histoire-Géo, Anglais, SVT, Physique-Chimie  
  - **Seconde / 1ère** : Maths, Français, SVT, Physique-Chimie, Histoire-Géo, Anglais, SES (1ère)  
  - **Terminale** : Maths, Français, SVT, **Physique**, **Chimie** (séparés), Histoire-Géo, Anglais, **Philosophie**, SES  

Chaque niveau a donc **toutes ses matières réelles**, pas seulement les maths.

### 2. Création automatique des données (aucun script manuel)

- **Déclenchement**  
  Lors du premier appel à `GET /api/eleve/matieres/` pour un niveau donné, si aucune matière n’existe pour ce niveau, le backend appelle `ensure_curriculum_complet_pour_niveau(code_niveau)`.

- **Création à la demande**  
  Pour ce niveau, le système crée automatiquement :
  - le **NiveauScolaire** (s’il manque),
  - toutes les **matières** prévues pour ce niveau,
  - pour chaque matière : **plusieurs leçons** (titres et contenus adaptés au niveau),
  - pour chaque leçon : **plusieurs exercices** (question + réponse correcte).

- **Aucune dépendance à `populate_db`**  
  Un élève qui s’inscrit avec un niveau donné voit toujours ses matières, leçons et exercices sans qu’aucune commande ne soit à lancer.

### 3. Parcours élève (strict)

- **Matières**  
  L’élève connecté voit **toutes les matières de son niveau** (page « Mes leçons »).

- **Clic sur une matière**  
  Affichage des **leçons** de cette matière pour son niveau.

- **Clic sur une leçon**  
  Affichage du **contenu** de la leçon (explication).

- **Bouton « Faire les exercices »**  
  Accès aux **exercices** de la leçon ; soumission des réponses, feedback (score, message).

Aucun écran vide lié au manque de données : si le niveau est valide, le curriculum est créé automatiquement.

### 4. IA éducative visible et utilisée

- **Pendant la lecture d’une leçon**  
  Sur la page détail d’une leçon : bouton **« Poser une question au tuteur IA »** qui ouvre le chat.  
  L’IA reçoit : **niveau**, **matière**, **titre de la leçon**, **extrait du contenu**.  
  Elle peut répondre aux questions, réexpliquer la leçon, donner des exemples.

- **Pendant les exercices**  
  Sur la page exercices d’une leçon : bouton **« Tuteur IA »** qui ouvre le même type de chat.  
  Contexte : **leçon en cours** (et donc matière + niveau). L’élève peut demander de l’aide sur une question ou une notion.

- **Backend**  
  - `chat_tuteur` envoie au LLM : niveau, matière, âge, points forts / faibles, **titre de la leçon**, **extrait du contenu** (`lecon_titre`, `lecon_contenu`).  
  - Les réponses sont donc **contextualisées** (matière, leçon, niveau).

- **Données réelles utilisées**  
  L’IA s’appuie sur le **niveau réel** de l’élève, la **matière** et la **leçon** en cours. Les réponses aux exercices sont déjà traitées par l’endpoint de soumission (score, feedback) ; l’IA peut en plus expliquer et analyser.

### 5. Qualité et cohérence

- **Logique métier**  
  Niveau (saisi à l’inscription) → matières du niveau → leçons par matière → exercices par leçon. Pas de mélange entre niveaux.

- **Données cohérentes**  
  Contenus et exercices définis par matière et par niveau (primaire / collège / lycée) dans `curriculum_complet.py`.

- **UX élève**  
  Messages clairs, pas d’instruction technique (plus de mention de « populate_db »), boutons utiles (dont accès au tuteur IA).

---

## Comment la plateforme fonctionne désormais

1. **Inscription**  
   L’élève choisit son **niveau scolaire** (CP1 à Terminale). Il est enregistré une seule fois.

2. **Connexion**  
   Après connexion, le système connaît son niveau.

3. **Page « Mes leçons »**  
   - Appel à `GET /api/eleve/matieres/`.  
   - Si aucune matière n’existe pour ce niveau → **création automatique** de tout le curriculum (niveau, matières, leçons, exercices).  
   - L’élève voit **toutes les matières de son niveau** (ex. CP1 : Maths, Français, Lecture, Écriture, Éducation civique).

4. **Clic sur une matière**  
   Chargement des **leçons** de cette matière pour son niveau (API leçons filtrée par niveau + matière).

5. **Clic sur une leçon**  
   Affichage du **contenu** de la leçon.  
   **Bouton « Poser une question au tuteur IA »** : ouverture du chat avec contexte leçon + matière + niveau.

6. **Clic sur « Faire les exercices »**  
   Affichage des **exercices** de la leçon. L’élève répond, soumet, reçoit score et feedback.  
   **Bouton « Tuteur IA »** : ouverture du chat avec le même contexte (leçon, matière, niveau) pour demander de l’aide.

7. **IA**  
   Visible et accessible **pendant la leçon** et **pendant les exercices**, avec utilisation du **niveau réel**, de la **matière** et de la **leçon en cours**.

---

## Validation (CP1, collège, Terminale)

- **Élève CP1** : à l’inscription avec niveau CP1, après connexion il voit Mathématiques, Français, Lecture, Écriture, Éducation civique. Chaque matière a plusieurs leçons avec exercices. L’IA est accessible depuis la leçon et depuis les exercices.

- **Élève collège (ex. 5ème)** : voit Maths, Français, Sciences, Histoire-Géo, Anglais, SVT, Physique-Chimie. Même parcours : leçons → contenu → exercices, avec IA contextuelle.

- **Élève Terminale** : voit Maths, Français, SVT, Physique, Chimie, Histoire-Géo, Anglais, Philosophie, SES. Contenus et exercices adaptés au lycée. IA utilisant le niveau Terminale et la leçon en cours.

Tant que le niveau est valide, **aucune commande manuelle n’est requise** : les matières, leçons et exercices sont créés automatiquement au premier accès.

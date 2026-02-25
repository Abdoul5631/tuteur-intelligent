# Plan de correction fonctionnel – Données, logique métier, IA

## Analyse des causes

### 1. Niveaux scolaires (CP1 → Terminale) invisibles

| Cause | Détail |
|-------|--------|
| **Backend** | L’endpoint `GET /api/niveaux/` existait et renvoyait bien les niveaux. Les données sont créées par `populate_niveaux` (appelé dans `populate_db`). |
| **Frontend** | Aucun composant n’appelait `/api/niveaux/`. Les niveaux n’étaient donc jamais affichés. |

**Correction appliquée :**
- Service frontend `niveauxService.ts` qui appelle `GET /api/niveaux/`.
- Page **Leçons** : chargement des niveaux au montage et affichage des libellés (CP1, CE1, …, Terminale) sous le titre.

---

### 2. Matières invisibles

| Cause | Détail |
|-------|--------|
| **Backend** | Un seul enregistrement (Mathématiques) était créé dans `populate_db`. L’API `GET /api/matieres/` est en `AllowAny` et fonctionne. |
| **Frontend** | Tuteur IA utilisait `fetch('/api/matieres/')` et affichait `matiere.nom` (clé technique, ex. "mathematiques") au lieu du libellé. Si la liste était vide (DB non peuplée), aucun message n’indiquait quoi faire. |

**Corrections appliquées :**
- **populate_db** : création de plusieurs matières (Mathématiques, Français, Sciences, Anglais, Histoire-Géographie) avec icônes et couleurs.
- Service frontend `matieresService.ts` et utilisation dans Tuteur IA pour charger les matières via l’API centralisée (baseURL, auth si besoin).
- Tuteur IA : affichage avec `matiere.nom_display || matiere.nom` pour voir les libellés (ex. "Mathématiques").
- Si la liste des matières est vide : message explicite invitant à lancer `python manage.py populate_db` et précision que le chat reste utilisable.

---

### 3. IA “non active” pour l’élève

| Cause | Détail |
|-------|--------|
| **Backend** | Le service LLM est bien branché. Par défaut `IA_PROVIDER=mock` : le **MockLLMService** renvoie des réponses de démo (explications, exercices, feedback). Sans clé API, OpenAI/Gemini renvoient un message du type “Réponse en mode démo (configurez OPENAI_API_KEY)”. |
| **Frontend** | Le chat exigeait une matière sélectionnée pour activer certaines actions ; si la liste des matières était vide, l’élève pouvait avoir l’impression que rien ne fonctionnait. Le champ de saisie du chat restait actif (pas de blocage sur `matiereId`), mais l’absence de matières et de message clair rendait l’IA peu visible. |

**Corrections appliquées :**
- Le chat reste utilisable **sans matière** : le backend acceptait déjà `matiere_id` optionnel (contexte “general”).
- Message dans le chat quand aucune matière n’est sélectionnée : “Sans matière sélectionnée, le tuteur répond en mode général. Choisissez une matière à gauche pour un contexte précis.”
- Avec **mock** : l’élève reçoit des réponses de démo. Pour une vraie IA : définir `OPENAI_API_KEY` ou `GEMINI_API_KEY` (et éventuellement `IA_PROVIDER=openai` ou `gemini`) dans l’environnement du backend.

---

## Récapitulatif des changements techniques

| Fichier / zone | Modification |
|----------------|--------------|
| `Frontend/src/services/niveauxService.ts` | **Création** – Appel `GET /api/niveaux/`, typage. |
| `Frontend/src/services/matieresService.ts` | **Création** – Appel `GET /api/matieres/`, typage. |
| `Frontend/src/pages/Lecons/Lecons.tsx` | Chargement et affichage des niveaux (CP1 → Terminale) sous le titre. |
| `Frontend/src/pages/Tuteur/TuteurIA.tsx` | Utilisation de `fetchMatieres()`, affichage `nom_display`, message si aucune matière, texte des boutons de matière. |
| `Frontend/src/components/Chat/ChatIA.tsx` | Message lorsque aucune matière n’est sélectionnée (mode général). |
| `core/management/commands/populate_db.py` | Création de plusieurs matières (maths, français, sciences, anglais, histoire-géo). |

---

## À faire côté utilisateur / déploiement

1. **Données en base**
   - Lancer (ou relancer) :  
     `python manage.py populate_db`  
   - Cela crée les niveaux (CP1 → Terminale), les matières, les utilisateurs de test et les leçons.

2. **IA réelle (optionnel)**
   - Créer un fichier `.env` à la racine du projet (ou configurer l’environnement du serveur) avec par exemple :  
     `OPENAI_API_KEY=sk-...`  
   - Redémarrer le backend. Sans clé, le mode **mock** reste actif avec des réponses de démo.

3. **Vérifications**
   - Page **Leçons** : les niveaux scolaires s’affichent sous le titre.
   - Page **Tuteur IA** : les matières apparaissent à gauche avec leurs libellés ; le chat répond avec ou sans matière sélectionnée.
   - Après `populate_db`, recharger la page Tuteur IA pour voir les nouvelles matières.

---

## Roadmap fonctionnelle (suite possible)

- **Inscription** : proposer le **niveau scolaire** (CP1 → Terminale) en plus du niveau global (Débutant / Intermédiaire / Avancé), en s’appuyant sur `GET /api/niveaux/` et le champ `niveau_scolaire` du profil.
- **Filtre par niveau** : sur la page Leçons, filtrer les leçons par niveau scolaire (CP1, CE1, etc.) en plus du niveau global.
- **IA** : personnalisation plus poussée (contexte de la leçon en cours, historique des erreurs) et messages clairs en mode démo (“Réponse de démonstration – configurez OPENAI_API_KEY pour l’IA réelle”).

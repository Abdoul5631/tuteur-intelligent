# Architecture IA modulaire – Tuteur Intelligent

## Vue d'ensemble

L’IA est **entièrement pilotée par le backend Django**. Le frontend ne fait que consommer des endpoints REST ; toute la logique IA (explication, génération d’exercices, adaptation du niveau) est exécutée côté serveur.

```
┌─────────────┐     REST API      ┌─────────────────────────────────────┐
│   Frontend  │ ───────────────►  │           Backend Django             │
│   (React)   │                   │  ┌─────────────────────────────────┐ │
│             │                   │  │      Services IA modulaires      │ │
└─────────────┘                   │  │  - Explication                   │ │
                                  │  │  - Génération exercices          │ │
                                  │  │  - Adaptation niveau             │ │
                                  │  │  - Suivi progression             │ │
                                  │  └─────────────────────────────────┘ │
                                  └─────────────────────────────────────┘
```

## Modules IA côté backend

### 1. Explication des leçons (`core/services/ia_service.py`)

- **Fonction** : Expliquer un concept ou une leçon de façon adaptée au profil de l’élève.
- **Entrées** : `lecon_id`, `utilisateur`, optionnellement `question`.
- **Sorties** : Texte d’explication, éventuellement variantes (simplifiée / approfondie).
- **Usage** : Endpoint `/api/ia/expliquer/` (POST).

### 2. Génération d’exercices (`core/ia_endpoints.py` – `generer_exercices`)

- **Fonction** : Produire des exercices à partir d’une leçon ou d’un sujet.
- **Entrées** : `lecon_id`, `matiere`, `niveau`, `nombre`.
- **Sorties** : Liste d’exercices (question, options, réponse attendue).
- **Usage** : Endpoint `/api/ia/generer-exercices/` (POST).

### 3. Analyse des réponses (`core/services/ia_service.py` – `corriger_exercice`)

- **Fonction** : Évaluer une réponse, donner un feedback et une explication.
- **Entrées** : `exercice`, `reponse_donnee`.
- **Sorties** : `score`, `feedback_ia`, éventuellement `suggestion_amelioration`.
- **Usage** : Appelé par `/api/exercices/soumettre/` (POST).

### 4. Adaptation du niveau (progression)

- **Données** : `ProgressionNotion` (notions maîtrisées / faibles / en cours) et profil utilisateur.
- **Fonction** : Choisir les contenus et difficultés adaptés.
- **Endpoints** :
  - `GET /api/progression-eleve/` : notions maîtrisées / faibles.
  - `GET /api/ia/recommandations/` : recommandations personnalisées.
  - `GET /api/ia/diagnostic/` : diagnostic du niveau.

## Suivi de progression (base de la personnalisation)

| Modèle / Source      | Rôle                                                |
|----------------------|------------------------------------------------------|
| `ProgressionNotion`  | Notions (maîtrisé / en cours / faible) par élève     |
| `Utilisateur`        | `niveau_scolaire`, `domaines_forts`, `domaines_faibles` |
| `Resultat`           | Historique des scores par exercice                   |

L’IA utilise ces données pour :
1. Prioriser les notions à travailler.
2. Ajuster la difficulté des explications et des exercices.
3. Proposer des parcours personnalisés.

## Interfaces (contrats backend)

### Explication IA

```python
def expliquer_concept(lecon_id: int, utilisateur: Utilisateur, question: str | None = None) -> dict:
    return {
        "explication": str,
        "concepts_cles": list[str],
        "adaptation_niveau": str  # simplifiée | standard | approfondie
    }
```

### Génération exercices IA

```python
def generer_exercices(lecon_id: int, matiere: str, niveau: str, nombre: int = 5) -> list[dict]:
    return [
        {"question": str, "options": list, "reponse_correcte": str, "type_exercice": str, ...}
    ]
```

### Correction / feedback IA

```python
def corriger_exercice(exercice: Exercice, reponse: str) -> tuple[int, str]:
    return (score_0_100, feedback_texte)
```

## Découplage frontend / IA

- Le frontend **ne contient aucune logique IA**.
- Toutes les requêtes passent par des appels REST.
- Les tokens / clés API IA restent côté serveur (variables d’environnement).
- Les services IA peuvent être remplacés (OpenAI, Ollama, Claude, etc.) sans modifier le frontend.

## Évolutions possibles

1. **Mise à jour de `ProgressionNotion`** : lors de la soumission d’exercices, enrichir ou créer les entrées dans `ProgressionNotion` selon les notions évaluées.
2. **Cache** : mise en cache des explications ou des exercices générés pour éviter les appels répétés.
3. **Files / Celery** : déplacer la génération d’exercices ou les tâches longues dans des workers asynchrones.
4. **Fallback** : en cas d’indisponibilité de l’IA, utiliser des explications ou exercices pré-définis.

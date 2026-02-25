"""
Garantit qu'un niveau scolaire a au moins une matière et une leçon (avec exercice).
Utilisé quand l'élève connecté a un niveau valide mais qu'aucune donnée n'existe encore.
Aucune dépendance à populate_db : création automatique à la demande.
"""
from core.models import NiveauScolaire, Matiere, Lecon, Exercice

# Même référence que populate_niveaux (CP1 → Terminale)
NIVEAUX_MINIMAL = [
    ('cp1', 'CP1', 1, 'primaire'),
    ('cp2', 'CP2', 2, 'primaire'),
    ('ce1', 'CE1', 3, 'primaire'),
    ('ce2', 'CE2', 4, 'primaire'),
    ('cm1', 'CM1', 5, 'primaire'),
    ('cm2', 'CM2', 6, 'primaire'),
    ('6eme', '6ème', 7, 'college'),
    ('5eme', '5ème', 8, 'college'),
    ('4eme', '4ème', 9, 'college'),
    ('3eme', '3ème', 10, 'college'),
    ('seconde', 'Seconde', 11, 'lycee'),
    ('1ere', '1ère', 12, 'lycee'),
    ('terminale', 'Terminale', 13, 'lycee'),
]
NIVEAUX_MAP = {code: (libelle, ordre, cycle) for code, libelle, ordre, cycle in NIVEAUX_MINIMAL}


def ensure_contenu_minimal_pour_niveau(code_niveau: str) -> None:
    """
    Si le niveau n'a aucune matière/leçon, crée le strict minimum :
    - NiveauScolaire pour code_niveau
    - Une matière (Mathématiques)
    - Une leçon pour ce niveau
    - Un exercice pour cette leçon
    """
    if not code_niveau or code_niveau not in NIVEAUX_MAP:
        return
    libelle, ordre, cycle = NIVEAUX_MAP[code_niveau]
    niveau, _ = NiveauScolaire.objects.get_or_create(
        code=code_niveau,
        defaults={'libelle': libelle, 'ordre': ordre, 'cycle': cycle}
    )
    matiere, _ = Matiere.objects.get_or_create(
        nom='mathematiques',
        defaults={'description': 'Mathématiques', 'couleur_hex': '#3B82F6', 'icone': '🔢'}
    )
    lecon, created = Lecon.objects.get_or_create(
        matiere=matiere,
        niveau=niveau,
        titre='Bienvenue dans cette matière',
        defaults={
            'contenu_principal': 'Cette leçon est disponible pour votre niveau. D\'autres contenus seront ajoutés progressivement.',
            'niveau_global': 'débutant' if code_niveau in ('cp1', 'cp2', 'ce1', 'ce2', 'cm1', 'cm2') else (
                'intermédiaire' if code_niveau in ('6eme', '5eme', '4eme', '3eme') else 'avancé'
            ),
            'ordre': 0,
        }
    )
    if created or not lecon.exercices.exists():
        Exercice.objects.get_or_create(
            lecon=lecon,
            matiere=matiere,
            question='Première question : 1 + 1 = ?',
            defaults={
                'reponse_correcte': '2',
                'niveau': 'débutant',
                'ordre': 0,
            }
        )

"""
Populate full 6e program: Français, Mathématiques, SVT, Histoire, Géographie, ECM
Each chapter becomes a Lecon (niveau_scolaire='6eme') and gets exactly 2 exercices.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Matiere, Lecon, Exercice


class Command(BaseCommand):
    help = 'Populate 6e program (chapters -> leçons; each leçon has 2 exercices)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting 6e population...'))

        with transaction.atomic():
            # Map requested subjects to existing Matiere.nom choices
            matieres_map = {
                'francais': 'francais',
                'mathematiques': 'mathematiques',
                'svt': 'sciences',
                'histoire': 'histoire_geo',
                'geographie': 'histoire_geo',
                'ecm': 'education_civique',
            }

            # Ensure Matiere objects exist
            matieres = {}
            for key, nom_choice in matieres_map.items():
                m, created = Matiere.objects.get_or_create(
                    nom=nom_choice,
                    defaults={'description': f'Matière {nom_choice}'}
                )
                matieres[key] = m
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Created Matière: {nom_choice}'))

            # 6e content from user
            program = {
                'francais': [
                    {
                        'titre': 'Chapitre 1 : La communication',
                        'contenu': "La communication est l’échange d’un message entre un émetteur et un récepteur à l’aide d’un code (langue, signes) et d’un canal (voix, écrit, gestes). Elle peut être orale, écrite ou gestuelle.",
                        'exos': [
                            {'question': 'Citer les éléments de la communication.', 'type': 'reponse_courte', 'reponse': 'émetteur, récepteur, message, code, canal'},
                            {'question': 'Classer : SMS / conversation / affiche (orale, écrite, gestuelle).', 'type': 'redaction', 'reponse': 'Réponse libre classée'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Le récit',
                        'contenu': 'Le récit raconte des événements réels ou imaginaires avec des personnages, un lieu et un temps.',
                        'exos': [
                            {'question': 'Donner deux éléments du récit.', 'type': 'reponse_courte', 'reponse': 'personnages, lieu (ou temps)'},
                            {'question': 'Dire si un conte est un récit (justifier).', 'type': 'redaction', 'reponse': 'Oui si il raconte des événements; justification attendue'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 3 : Grammaire — Nom et déterminant',
                        'contenu': 'Le nom désigne personnes, animaux, choses. Le déterminant accompagne le nom.',
                        'exos': [
                            {'question': 'Souligner le nom, entourer le déterminant.', 'type': 'redaction', 'reponse': 'Exercice annoté'},
                            {'question': 'Compléter avec un déterminant.', 'type': 'reponse_courte', 'reponse': 'un, le, la, des etc.'},
                        ]
                    }
                ],
                'mathematiques': [
                    {
                        'titre': 'Chapitre 1 : Nombres entiers',
                        'contenu': 'Les nombres entiers servent à compter et ordonner.',
                        'exos': [
                            {'question': 'Ranger 15, 8, 20.', 'type': 'reponse_courte', 'reponse': '8, 15, 20'},
                            {'question': 'Calculer 34 + 16.', 'type': 'calcul', 'reponse': '50'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Addition et soustraction',
                        'contenu': "Additionner, c'est ajouter ; soustraire, c'est enlever.",
                        'exos': [
                            {'question': '245 + 37.', 'type': 'calcul', 'reponse': '282'},
                            {'question': '500 − 268.', 'type': 'calcul', 'reponse': '232'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 3 : Géométrie — Segments',
                        'contenu': 'Un segment relie deux points.',
                        'exos': [
                            {'question': 'Tracer un segment AB.', 'type': 'redaction', 'reponse': 'Dessin demandé'},
                            {'question': 'Mesurer sa longueur.', 'type': 'reponse_courte', 'reponse': 'Longueur en unités'},
                        ]
                    }
                ],
                'svt': [
                    {
                        'titre': 'Chapitre 1 : Les êtres vivants',
                        'contenu': "Un être vivant naît, se nourrit, respire, se reproduit et meurt.",
                        'exos': [
                            {'question': 'Citer deux êtres vivants.', 'type': 'reponse_courte', 'reponse': 'chien, arbre (ex.)'},
                            {'question': "Une plante est-elle vivante ? Pourquoi ?", 'type': 'reponse_courte', 'reponse': 'Oui, elle pousse, respire, a besoins d\'eau et nutriments'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Le corps humain',
                        'contenu': 'Le corps humain est composé d’organes qui fonctionnent ensemble.',
                        'exos': [
                            {'question': 'Citer un organe.', 'type': 'reponse_courte', 'reponse': 'cœur, poumon, estomac'},
                            {'question': 'À quoi sert le cœur ?', 'type': 'reponse_courte', 'reponse': 'Pomper le sang'},
                        ]
                    }
                ],
                'histoire': [
                    {
                        'titre': "Chapitre 1 : Les origines de l’homme",
                        'contenu': 'Les premières traces humaines sont en Afrique.',
                        'exos': [
                            {'question': 'Où apparaissent les premiers hommes ?', 'type': 'reponse_courte', 'reponse': 'En Afrique'},
                            {'question': "L’homme ancien vivait comment ?", 'type': 'redaction', 'reponse': 'Réponse explicative: chasse, cueillette, nomadisme'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : La vie préhistorique',
                        'contenu': 'Les hommes vivaient de chasse et de cueillette.',
                        'exos': [
                            {'question': 'Citer une activité.', 'type': 'reponse_courte', 'reponse': 'Chasse'},
                            {'question': 'Pourquoi se déplaçaient-ils ?', 'type': 'reponse_courte', 'reponse': 'Pour trouver nourriture et abris'},
                        ]
                    }
                ],
                'geographie': [
                    {
                        'titre': 'Chapitre 1 : La Terre',
                        'contenu': 'La Terre est composée de continents et d’océans.',
                        'exos': [
                            {'question': 'Citer deux continents.', 'type': 'reponse_courte', 'reponse': 'Afrique, Europe'},
                            {'question': 'Nommer un océan.', 'type': 'reponse_courte', 'reponse': 'Océan Atlantique'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Le Burkina Faso',
                        'contenu': "Pays d’Afrique de l’Ouest, capitale Ouagadougou.",
                        'exos': [
                            {'question': 'Citer un pays voisin.', 'type': 'reponse_courte', 'reponse': 'Mali, Ghana, Niger, etc.'},
                            {'question': 'Quelle est la capitale ?', 'type': 'reponse_courte', 'reponse': 'Ouagadougou'},
                        ]
                    }
                ],
                'ecm': [
                    {
                        'titre': 'Chapitre 1 : La discipline',
                        'contenu': 'La discipline aide à vivre ensemble.',
                        'exos': [
                            {'question': 'Donner un exemple de discipline.', 'type': 'reponse_courte', 'reponse': 'Respecter les règles de la classe'},
                            {'question': 'Pourquoi respecter les règles ?', 'type': 'reponse_courte', 'reponse': 'Pour vivre ensemble et être en sécurité'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Le respect',
                        'contenu': 'Le respect concerne les personnes et les biens.',
                        'exos': [
                            {'question': 'Donner un exemple de respect.', 'type': 'reponse_courte', 'reponse': 'Ne pas abîmer les affaires des autres'},
                            {'question': 'Pourquoi respecter autrui ?', 'type': 'reponse_courte', 'reponse': 'Pour maintenir des relations harmonieuses'},
                        ]
                    }
                ]
            }

            created_lecons = 0
            created_exos = 0

            for subject_key, chapters in program.items():
                mat = matieres.get(subject_key)
                if not mat:
                    continue
                for idx, ch in enumerate(chapters, 1):
                    lecon, created = Lecon.objects.update_or_create(
                        matiere=mat,
                        titre=ch['titre'],
                        defaults={
                            'contenu_principal': ch['contenu'],
                            'niveau_scolaire': '6eme',
                            'niveau_global': 'débutant',
                            'ordre': idx,
                            'difficulte': 4,
                            'temps_estime': 20,
                        }
                    )
                    created_lecons += 1
                    for ex_idx, ex in enumerate(ch['exos'], 1):
                        exercice, ex_created = Exercice.objects.update_or_create(
                            lecon=lecon,
                            question=ex['question'],
                            defaults={
                                'matiere': mat,
                                'type_exercice': ex.get('type', 'reponse_courte'),
                                'reponse_correcte': ex.get('reponse', ''),
                                'options': ex.get('options', []),
                                'niveau': '6eme',
                                'ordre': ex_idx,
                            }
                        )
                        created_exos += 1

            self.stdout.write(self.style.SUCCESS(f"\n✅ 6e population terminée: {created_lecons} leçons, {created_exos} exercices créés/actualisés."))

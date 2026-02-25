"""
Populate full 3e program: Français, Mathématiques (renforcé), Physique-Chimie (renforcé), SVT, Histoire, Géographie, ECM
Each chapter becomes a Lecon (niveau_scolaire='3eme') and gets exactly 2 exercices.
Note: Level is more advanced (end of collège, prep for lycée).
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Matiere, Lecon, Exercice


class Command(BaseCommand):
    help = 'Populate 3e program (advanced level chapters -> leçons; each leçon has 2 exercices)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting 3e population...'))

        with transaction.atomic():
            # Map subjects to existing Matiere.nom choices
            matieres_map = {
                'francais': 'francais',
                'mathematiques': 'mathematiques',
                'physique_chimie': 'physique_chimie',
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

            # 3e content from user
            program = {
                'francais': [
                    {
                        'titre': 'Chapitre 1 : Le texte argumentatif',
                        'contenu': """Le texte argumentatif vise à convaincre ou persuader.
Il contient une thèse, des arguments et des exemples.
Les connecteurs logiques (donc, car, en effet) structurent le raisonnement.""",
                        'exos': [
                            {'question': 'Qu\'est-ce qu\'une thèse ?', 'type': 'reponse_courte', 'reponse': 'L\'idée principale qu\'on défend'},
                            {'question': 'Donne un argument pour l\'école obligatoire.', 'type': 'redaction', 'reponse': 'Réponse argumentée attendue'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Grammaire — Les propositions subordonnées',
                        'contenu': 'Une phrase complexe peut contenir une proposition principale et une subordonnée introduite par que, qui, lorsque…',
                        'exos': [
                            {'question': 'Souligne la subordonnée.', 'type': 'redaction', 'reponse': 'Exercice annoté'},
                            {'question': 'Transforme deux phrases simples en une phrase complexe.', 'type': 'redaction', 'reponse': 'Réponse libre contrôlée'},
                        ]
                    }
                ],
                'mathematiques': [
                    {
                        'titre': 'Chapitre 1 : Calcul littéral',
                        'contenu': """Le calcul littéral utilise des lettres pour représenter des nombres.
On peut simplifier, développer ou factoriser des expressions.
Exemples : 3x + 2x = 5x; 2(x + 3) = 2x + 6""",
                        'exos': [
                            {'question': 'Simplifie : 4x + 7x − 3x', 'type': 'calcul', 'reponse': '8x'},
                            {'question': 'Développe : 3(2x − 5)', 'type': 'calcul', 'reponse': '6x − 15'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Équations et inéquations',
                        'contenu': """Résoudre une équation, c'est trouver la valeur de x qui rend l'égalité vraie.
Les inéquations utilisent <, >, ≤, ≥.""",
                        'exos': [
                            {'question': '2x − 5 = 9', 'type': 'calcul', 'reponse': 'x = 7'},
                            {'question': 'Résous : x + 4 > 10', 'type': 'calcul', 'reponse': 'x > 6'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 3 : Fonctions linéaires',
                        'contenu': """Une fonction linéaire est de la forme f(x) = ax.
Elle se représente par une droite passant par l'origine.""",
                        'exos': [
                            {'question': 'f(x)=3x, calcule f(2)', 'type': 'calcul', 'reponse': '6'},
                            {'question': 'La fonction est-elle croissante si a > 0 ?', 'type': 'vrai_faux', 'reponse': 'Oui'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 4 : Géométrie — Théorème de Pythagore',
                        'contenu': """Dans un triangle rectangle :
c² = a² + b²""",
                        'exos': [
                            {'question': 'Triangle rectangle de côtés 3 cm et 4 cm. Calcule l\'hypoténuse.', 'type': 'calcul', 'reponse': '5 cm'},
                            {'question': 'Ce triangle est-il rectangle si 5² = 3² + 4² ?', 'type': 'vrai_faux', 'reponse': 'Oui'},
                        ]
                    }
                ],
                'physique_chimie': [
                    {
                        'titre': 'Chapitre 1 : Grandeurs physiques et unités',
                        'contenu': """Une grandeur physique se mesure avec une unité :
longueur (m), masse (kg), temps (s)""",
                        'exos': [
                            {'question': 'Convertis 2 km en m', 'type': 'calcul', 'reponse': '2000 m'},
                            {'question': 'Quelle est l\'unité de la masse ?', 'type': 'reponse_courte', 'reponse': 'kg (kilogramme)'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Vitesse et mouvement',
                        'contenu': """La vitesse se calcule par :
v = distance / temps
Elle s'exprime en m/s ou km/h.""",
                        'exos': [
                            {'question': 'Un mobile parcourt 100 m en 20 s. Calcule la vitesse.', 'type': 'calcul', 'reponse': '5 m/s'},
                            {'question': 'Si la distance double, que devient la vitesse ?', 'type': 'reponse_courte', 'reponse': 'Elle double aussi'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 3 : Électricité — Circuit électrique',
                        'contenu': """Un circuit électrique comprend :
un générateur, des conducteurs, un récepteur
Le courant circule si le circuit est fermé.""",
                        'exos': [
                            {'question': 'Cite les éléments d\'un circuit.', 'type': 'reponse_courte', 'reponse': 'générateur, conducteurs, récepteur'},
                            {'question': 'Que se passe-t-il si le circuit est ouvert ?', 'type': 'reponse_courte', 'reponse': 'Le courant ne circule pas'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 4 : Énergie et puissance',
                        'contenu': """L'énergie permet de produire un travail.
La puissance indique la rapidité de production de l'énergie.""",
                        'exos': [
                            {'question': 'Cite une forme d\'énergie.', 'type': 'reponse_courte', 'reponse': 'électrique, thermique, cinétique'},
                            {'question': 'Pourquoi l\'énergie est importante ?', 'type': 'reponse_courte', 'reponse': 'Pour produire du travail et de la chaleur'},
                        ]
                    }
                ],
                'svt': [
                    {
                        'titre': 'Chapitre 1 : La reproduction humaine',
                        'contenu': 'La reproduction permet la continuité de l\'espèce humaine.',
                        'exos': [
                            {'question': 'Quel est le rôle de la reproduction ?', 'type': 'reponse_courte', 'reponse': 'Assurer la continuité de l\'espèce'},
                            {'question': 'Qui intervient dans la reproduction ?', 'type': 'reponse_courte', 'reponse': 'homme et femme'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Santé et hygiène',
                        'contenu': 'L\'hygiène protège contre les maladies.',
                        'exos': [
                            {'question': 'Cite une règle d\'hygiène.', 'type': 'reponse_courte', 'reponse': 'se laver régulièrement'},
                            {'question': 'Pourquoi se laver les mains ?', 'type': 'reponse_courte', 'reponse': 'Pour éliminer les microbes'},
                        ]
                    }
                ],
                'histoire': [
                    {
                        'titre': 'Chapitre 1 : La colonisation et ses conséquences',
                        'contenu': 'La colonisation a modifié l\'organisation politique et économique de l\'Afrique.',
                        'exos': [
                            {'question': 'Cite une conséquence de la colonisation.', 'type': 'reponse_courte', 'reponse': 'Exploitation des ressources, suppression des libertés'},
                            {'question': 'Pourquoi les Africains ont-ils résisté ?', 'type': 'reponse_courte', 'reponse': 'Pour préserver leur liberté et indépendance'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Les indépendances africaines',
                        'contenu': 'Après 1960, plusieurs pays africains deviennent indépendants.',
                        'exos': [
                            {'question': 'En quelle période ?', 'type': 'reponse_courte', 'reponse': 'Après 1960'},
                            {'question': 'Pourquoi réclamer l\'indépendance ?', 'type': 'reponse_courte', 'reponse': 'Pour se gouverner soi-même'},
                        ]
                    }
                ],
                'geographie': [
                    {
                        'titre': 'Chapitre 1 : Développement et sous-développement',
                        'contenu': 'Le développement mesure le niveau de vie d\'un pays.',
                        'exos': [
                            {'question': 'Cite un indicateur de développement.', 'type': 'reponse_courte', 'reponse': 'PIB, revenu par habitant'},
                            {'question': 'Le Burkina Faso est-il développé ?', 'type': 'vrai_faux', 'reponse': 'Non'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Problèmes environnementaux',
                        'contenu': 'Désertification, pollution et déforestation menacent l\'environnement.',
                        'exos': [
                            {'question': 'Cite un problème environnemental.', 'type': 'reponse_courte', 'reponse': 'désertification, pollution, déforestation'},
                            {'question': 'Comment le limiter ?', 'type': 'reponse_courte', 'reponse': 'Protéger les forêts, limiter la pollution'},
                        ]
                    }
                ],
                'ecm': [
                    {
                        'titre': 'Chapitre 1 : La démocratie',
                        'contenu': 'La démocratie repose sur le vote et la participation citoyenne.',
                        'exos': [
                            {'question': 'Qu\'est-ce que la démocratie ?', 'type': 'reponse_courte', 'reponse': 'Gouvernement du peuple par le peuple'},
                            {'question': 'Pourquoi voter ?', 'type': 'reponse_courte', 'reponse': 'Pour participer à la décision collective'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Les institutions de l\'État',
                        'contenu': 'L\'État est organisé autour d\'institutions : exécutif, législatif, judiciaire.',
                        'exos': [
                            {'question': 'Cite une institution.', 'type': 'reponse_courte', 'reponse': 'gouvernement, parlement'},
                            {'question': 'Quel est son rôle ?', 'type': 'reponse_courte', 'reponse': 'Gouverner, légiférer, rendre justice'},
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
                            'niveau_scolaire': '3eme',
                            'niveau_global': 'avancé',
                            'ordre': idx,
                            'difficulte': 6,
                            'temps_estime': 30,
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
                                'niveau': '3eme',
                                'ordre': ex_idx,
                            }
                        )
                        created_exos += 1

            self.stdout.write(self.style.SUCCESS(f"\n✅ 3e population terminée: {created_lecons} leçons, {created_exos} exercices créés/actualisés."))

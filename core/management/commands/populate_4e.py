"""
Populate full 4e program: Français, Mathématiques, Physique-Chimie, SVT, Histoire, Géographie, ECM
Each chapter becomes a Lecon (niveau_scolaire='4eme') and gets exactly 2 exercices.
Note: Physique-Chimie debuts at 4e.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Matiere, Lecon, Exercice


class Command(BaseCommand):
    help = 'Populate 4e program (chapters -> leçons; each leçon has 2 exercices)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting 4e population...'))

        with transaction.atomic():
            # Map subjects to existing Matiere.nom choices
            # Note: physique_chimie is in the choices
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

            # 4e content from user
            program = {
                'francais': [
                    {
                        'titre': 'Chapitre 1 : Le texte explicatif',
                        'contenu': """Le texte explicatif sert à expliquer un phénomène, une situation ou un fait.
Il répond souvent aux questions : quoi ? comment ? pourquoi ?
On y trouve des connecteurs logiques : parce que, donc, en effet.""",
                        'exos': [
                            {'question': 'À quoi sert un texte explicatif ?', 'type': 'reponse_courte', 'reponse': 'À expliquer un phénomène, une situation ou un fait'},
                            {'question': 'Cite deux connecteurs logiques.', 'type': 'reponse_courte', 'reponse': 'parce que, donc (ou en effet, ainsi)'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Grammaire — La phrase complexe',
                        'contenu': """Une phrase complexe contient au moins deux verbes conjugués.
Elle peut être formée par coordination ou subordination.""",
                        'exos': [
                            {'question': 'Repère les verbes conjugués.', 'type': 'redaction', 'reponse': 'Exercice annoté'},
                            {'question': 'Transforme une phrase simple en phrase complexe.', 'type': 'redaction', 'reponse': 'Réponse libre contrôlée'},
                        ]
                    }
                ],
                'mathematiques': [
                    {
                        'titre': 'Chapitre 1 : Les nombres relatifs',
                        'contenu': """Les nombres relatifs peuvent être positifs ou négatifs.
Ils servent à représenter des situations comme les températures ou les dettes.""",
                        'exos': [
                            {'question': 'Classe −5, 3, 0, −2.', 'type': 'reponse_courte', 'reponse': '−5 ; −2 ; 0 ; 3'},
                            {'question': '−4 + 7 = ?', 'type': 'calcul', 'reponse': '3'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Les équations simples',
                        'contenu': "Résoudre une équation, c'est trouver la valeur de l'inconnue qui rend l'égalité vraie.",
                        'exos': [
                            {'question': 'x + 5 = 12', 'type': 'calcul', 'reponse': 'x = 7'},
                            {'question': '3x = 15', 'type': 'calcul', 'reponse': 'x = 5'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 3 : Géométrie — Le triangle',
                        'contenu': """Un triangle a trois côtés et trois angles.
Il peut être rectangle, isocèle ou équilatéral.""",
                        'exos': [
                            {'question': 'Cite un type de triangle.', 'type': 'reponse_courte', 'reponse': 'rectangle, isocèle, équilatéral'},
                            {'question': 'Combien de côtés a un triangle ?', 'type': 'calcul', 'reponse': '3'},
                        ]
                    }
                ],
                'physique_chimie': [
                    {
                        'titre': 'Chapitre 1 : La matière',
                        'contenu': """La matière est tout ce qui a une masse et occupe un volume.
Elle existe sous trois états : solide, liquide et gazeux.""",
                        'exos': [
                            {'question': 'Cite les trois états de la matière.', 'type': 'reponse_courte', 'reponse': 'solide, liquide, gazeux'},
                            {'question': 'L\'air est-il une matière ? Pourquoi ?', 'type': 'reponse_courte', 'reponse': 'Oui, car il a une masse et occupe un volume'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Les changements d\'état',
                        'contenu': """La matière peut changer d'état sous l'effet de la chaleur :
fusion, solidification, vaporisation, condensation.""",
                        'exos': [
                            {'question': 'Comment s\'appelle le passage de solide à liquide ?', 'type': 'reponse_courte', 'reponse': 'Fusion'},
                            {'question': 'Que devient l\'eau quand on la chauffe ?', 'type': 'reponse_courte', 'reponse': 'Elle s\'évapore / devient vapeur'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 3 : Les sources d\'énergie',
                        'contenu': """L'énergie permet de produire un travail ou de la chaleur.
Il existe des énergies renouvelables et non renouvelables.""",
                        'exos': [
                            {'question': 'Cite une énergie renouvelable.', 'type': 'reponse_courte', 'reponse': 'solaire, éolienne, hydraulique'},
                            {'question': 'Le pétrole est-il renouvelable ?', 'type': 'vrai_faux', 'reponse': 'Non'},
                        ]
                    }
                ],
                'svt': [
                    {
                        'titre': 'Chapitre 1 : La respiration',
                        'contenu': "La respiration permet à l'organisme d'obtenir de l'oxygène et d'éliminer le dioxyde de carbone.",
                        'exos': [
                            {'question': 'Quel gaz respire-t-on ?', 'type': 'reponse_courte', 'reponse': 'l\'oxygène'},
                            {'question': 'Quel organe permet la respiration ?', 'type': 'reponse_courte', 'reponse': 'les poumons'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : La circulation sanguine',
                        'contenu': 'Le sang transporte l\'oxygène et les nutriments dans le corps.',
                        'exos': [
                            {'question': 'Quel organe fait circuler le sang ?', 'type': 'reponse_courte', 'reponse': 'le cœur'},
                            {'question': 'À quoi sert le sang ?', 'type': 'reponse_courte', 'reponse': 'Transporter l\'oxygène et les nutriments'},
                        ]
                    }
                ],
                'histoire': [
                    {
                        'titre': 'Chapitre 1 : La traite négrière',
                        'contenu': 'La traite négrière est le commerce des esclaves africains vers d\'autres continents.',
                        'exos': [
                            {'question': 'D\'où venaient les esclaves ?', 'type': 'reponse_courte', 'reponse': 'D\'Afrique'},
                            {'question': 'Pourquoi parle-t-on de traite ?', 'type': 'reponse_courte', 'reponse': 'Parce que c\'est un échange commercial d\'êtres humains'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : La colonisation',
                        'contenu': 'La colonisation est la domination politique et économique d\'un territoire par un autre.',
                        'exos': [
                            {'question': 'Qui colonisait l\'Afrique ?', 'type': 'reponse_courte', 'reponse': 'Les puissances européennes'},
                            {'question': 'Cite une conséquence de la colonisation.', 'type': 'reponse_courte', 'reponse': 'Exploitation des ressources, suppression des libertés'},
                        ]
                    }
                ],
                'geographie': [
                    {
                        'titre': 'Chapitre 1 : La population africaine',
                        'contenu': 'La population africaine est jeune et en croissance rapide.',
                        'exos': [
                            {'question': 'La population africaine est-elle jeune ?', 'type': 'vrai_faux', 'reponse': 'Oui'},
                            {'question': 'Cite un problème lié à la croissance.', 'type': 'reponse_courte', 'reponse': 'Chômage, manque d\'école, pauvreté'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Les ressources naturelles',
                        'contenu': 'L\'Afrique possède de nombreuses ressources : or, pétrole, terres agricoles.',
                        'exos': [
                            {'question': 'Cite une ressource naturelle.', 'type': 'reponse_courte', 'reponse': 'or, pétrole, diamants, terres agricoles'},
                            {'question': 'Pourquoi les protéger ?', 'type': 'reponse_courte', 'reponse': 'Pour le développement et l\'avenir du continent'},
                        ]
                    }
                ],
                'ecm': [
                    {
                        'titre': 'Chapitre 1 : La citoyenneté',
                        'contenu': 'Le citoyen a des droits et des devoirs dans la société.',
                        'exos': [
                            {'question': 'Cite un devoir du citoyen.', 'type': 'reponse_courte', 'reponse': 'Respecter les lois, payer les impôts'},
                            {'question': 'Pourquoi respecter les lois ?', 'type': 'reponsa_courte', 'reponse': 'Pour vivre ensemble en harmonie'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : La solidarité',
                        'contenu': 'La solidarité consiste à aider les autres.',
                        'exos': [
                            {'question': 'Donne un exemple de solidarité.', 'type': 'reponse_courte', 'reponse': 'Aider un voisin, donner aux pauvres'},
                            {'question': 'Pourquoi être solidaire ?', 'type': 'reponse_courte', 'reponse': 'Parce que nous sommes interdépendants'},
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
                            'niveau_scolaire': '4eme',
                            'niveau_global': 'intermédiaire',
                            'ordre': idx,
                            'difficulte': 5,
                            'temps_estime': 25,
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
                                'niveau': '4eme',
                                'ordre': ex_idx,
                            }
                        )
                        created_exos += 1

            self.stdout.write(self.style.SUCCESS(f"\n✅ 4e population terminée: {created_lecons} leçons, {created_exos} exercices créés/actualisés."))

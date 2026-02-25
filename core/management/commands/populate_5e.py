"""
Populate full 5e program: Français, Mathématiques, SVT, Histoire, Géographie, ECM
Each chapter becomes a Lecon (niveau_scolaire='5eme') and gets exactly 2 exercices.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Matiere, Lecon, Exercice


class Command(BaseCommand):
    help = 'Populate 5e program (chapters -> leçons; each leçon has 2 exercices)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting 5e population...'))

        with transaction.atomic():
            # Map subjects to existing Matiere.nom choices
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

            # 5e content from user
            program = {
                'francais': [
                    {
                        'titre': 'Chapitre 1 : Le texte narratif',
                        'contenu': """Le texte narratif raconte une histoire avec un début, un déroulement et une fin.
Il met en scène des personnages dans un lieu et un temps précis.
On distingue le narrateur (celui qui raconte) et les personnages.""",
                        'exos': [
                            {'question': 'Cite les éléments d\'un récit.', 'type': 'reponse_courte', 'reponse': 'personnages, lieu, temps, narrateur, action'},
                            {'question': 'Qui raconte l\'histoire dans un texte narratif ?', 'type': 'reponse_courte', 'reponse': 'Le narrateur'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Le dialogue',
                        'contenu': """Le dialogue est un échange de paroles entre plusieurs personnages.
Il est introduit par des verbes de parole : dire, répondre, demander.""",
                        'exos': [
                            {'question': 'Cite deux verbes de parole.', 'type': 'reponse_courte', 'reponse': 'dire, répondre (ou demander, crier, murmurer)'},
                            {'question': 'Le dialogue sert-il à décrire ou à faire parler ?', 'type': 'reponse_courte', 'reponse': 'À faire parler'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 3 : Grammaire — Le verbe',
                        'contenu': """Le verbe exprime une action ou un état.
Il se conjugue selon le temps et la personne.""",
                        'exos': [
                            {'question': 'Souligne le verbe : L\'élève écrit la leçon.', 'type': 'reponse_courte', 'reponse': 'écrit'},
                            {'question': 'Conjugue : aller au présent, 1re personne du singulier.', 'type': 'reponse_courte', 'reponse': 'je vais'},
                        ]
                    }
                ],
                'mathematiques': [
                    {
                        'titre': 'Chapitre 1 : Les fractions',
                        'contenu': """Une fraction représente une partie d'un tout.
Exemple : 1/2 signifie une part sur deux parts égales.""",
                        'exos': [
                            {'question': 'Écris une fraction représentant la moitié.', 'type': 'reponse_courte', 'reponse': '1/2'},
                            {'question': '1/2 + 1/4 = ?', 'type': 'calcul', 'reponse': '3/4'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Les nombres décimaux',
                        'contenu': 'Un nombre décimal comporte une partie entière et une partie décimale.',
                        'exos': [
                            {'question': 'Donne la partie décimale de 12,45.', 'type': 'reponse_courte', 'reponse': '45 (ou 0,45)'},
                            {'question': 'Range 3,2 – 3,15 – 3,08.', 'type': 'reponse_courte', 'reponse': '3,08 ; 3,15 ; 3,2'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 3 : Géométrie — Angles',
                        'contenu': 'Un angle est formé par deux demi-droites ayant la même origine.',
                        'exos': [
                            {'question': 'Cite un type d\'angle.', 'type': 'reponse_courte', 'reponse': 'angle droit, aigu, obtus'},
                            {'question': 'Un angle droit mesure combien de degrés ?', 'type': 'calcul', 'reponse': '90'},
                        ]
                    }
                ],
                'svt': [
                    {
                        'titre': 'Chapitre 1 : La nutrition chez l\'homme',
                        'contenu': """La nutrition permet à l'organisme de produire de l'énergie.
Elle comprend l'alimentation, la digestion et l'absorption.""",
                        'exos': [
                            {'question': 'Pourquoi mange-t-on ?', 'type': 'reponse_courte', 'reponse': 'Pour produire de l\'énergie et grandir'},
                            {'question': 'Cite un aliment énergétique.', 'type': 'reponse_courte', 'reponse': 'riz, pain, sucre, huile'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Les plantes vertes',
                        'contenu': 'Les plantes fabriquent leur nourriture grâce à la photosynthèse.',
                        'exos': [
                            {'question': 'De quoi une plante a-t-elle besoin pour vivre ?', 'type': 'reponse_courte', 'reponse': 'eau, lumière, minéraux'},
                            {'question': 'Quel est le rôle des feuilles ?', 'type': 'reponse_courte', 'reponse': 'Fabriquer la nourriture par photosynthèse'},
                        ]
                    }
                ],
                'histoire': [
                    {
                        'titre': 'Chapitre 1 : Les grands empires africains',
                        'contenu': """L'Afrique a connu de grands empires comme le Ghana, le Mali et le Songhaï.
Ils étaient organisés autour du commerce et de l'autorité du roi.""",
                        'exos': [
                            {'question': 'Cite un empire africain.', 'type': 'reponse_courte', 'reponse': 'Ghana, Mali, Songhaï'},
                            {'question': 'Quelle activité faisait la richesse de ces empires ?', 'type': 'reponse_courte', 'reponse': 'Le commerce'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : La société africaine ancienne',
                        'contenu': 'La société était organisée autour de la famille, du chef et des traditions.',
                        'exos': [
                            {'question': 'Qui dirigeait la société ?', 'type': 'reponse_courte', 'reponse': 'Le chef'},
                            {'question': 'Quel rôle jouaient les traditions ?', 'type': 'reponse_courte', 'reponse': 'Structurer la société et préserver la culture'},
                        ]
                    }
                ],
                'geographie': [
                    {
                        'titre': 'Chapitre 1 : Les reliefs',
                        'contenu': 'Le relief comprend montagnes, plateaux et plaines.',
                        'exos': [
                            {'question': 'Cite deux types de relief.', 'type': 'reponse_courte', 'reponse': 'montagnes, plateaux (ou plaines)'},
                            {'question': 'Où trouve-t-on les montagnes ?', 'type': 'reponse_courte', 'reponse': 'En région montagneuse / À différents endroits'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Le climat',
                        'contenu': 'Le climat correspond aux conditions météorologiques d\'une région.',
                        'exos': [
                            {'question': 'Cite un type de climat.', 'type': 'reponse_courte', 'reponse': 'tropical, désertique, tempéré'},
                            {'question': 'Quel climat domine au Burkina Faso ?', 'type': 'reponse_courte', 'reponse': 'Climat tropical et subtropical'},
                        ]
                    }
                ],
                'ecm': [
                    {
                        'titre': 'Chapitre 1 : Droits et devoirs',
                        'contenu': 'Chaque citoyen a des droits mais aussi des devoirs envers la société.',
                        'exos': [
                            {'question': 'Cite un droit.', 'type': 'reponse_courte', 'reponse': 'éducation, santé, vie'},
                            {'question': 'Cite un devoir.', 'type': 'reponse_courte', 'reponse': 'respecter la loi, aider autrui'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Le respect des biens publics',
                        'contenu': 'Les biens publics appartiennent à tous et doivent être protégés.',
                        'exos': [
                            {'question': 'Donne un exemple de bien public.', 'type': 'reponse_courte', 'reponse': 'parc, route, école'},
                            {'question': 'Pourquoi les protéger ?', 'type': 'reponse_courte', 'reponse': 'Ils servent à tous et assurent le bien-être collectif'},
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
                            'niveau_scolaire': '5eme',
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
                                'niveau': '5eme',
                                'ordre': ex_idx,
                            }
                        )
                        created_exos += 1

            self.stdout.write(self.style.SUCCESS(f"\n✅ 5e population terminée: {created_lecons} leçons, {created_exos} exercices créés/actualisés."))

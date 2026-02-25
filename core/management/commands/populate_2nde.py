"""
Populate full 2nde program: Français, Mathématiques, Physique-Chimie, SVT, Histoire, Géographie, ECM
Each chapter becomes a Lecon (niveau_scolaire='2nde') and gets exactly 2 exercices.
Note: 2nde is lycée level with advanced Maths and Physics.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Matiere, Lecon, Exercice


class Command(BaseCommand):
    help = 'Populate 2nde program (lycée level chapters -> leçons; each leçon has 2 exercices)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting 2nde population...'))

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

            # 2nde content from user
            program = {
                'francais': [
                    {
                        'titre': 'Chapitre 1 : Le roman et le récit long',
                        'contenu': """Le roman est un récit long avec intrigue, personnages, cadre spatio-temporel.
On analyse le point de vue, le schéma narratif, les thèmes.""",
                        'exos': [
                            {'question': 'Définis le schéma narratif.', 'type': 'reponse_courte', 'reponse': 'situation initiale → péripéties → dénouement'},
                            {'question': 'Donne un thème fréquent du roman.', 'type': 'reponse_courte', 'reponse': 'amour, pouvoir, quête, liberté'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Argumentation',
                        'contenu': 'Convaincre (raison) et persuader (émotion). Thèse, arguments, exemples, connecteurs.',
                        'exos': [
                            {'question': 'Distingue convaincre/persuader.', 'type': 'reponse_courte', 'reponse': 'Convaincre: appel à la raison; persuader: appel aux émotions'},
                            {'question': 'Rédige un argument pour l\'école obligatoire.', 'type': 'redaction', 'reponse': 'Réponse argumentée'},
                        ]
                    }
                ],
                'mathematiques': [
                    {
                        'titre': 'Chapitre 1 : Fonctions affines',
                        'contenu': 'f(x)=ax+b ; variation selon le signe de a ; représentation graphique.',
                        'exos': [
                            {'question': 'f(x)=2x−3 : calcule f(1).', 'type': 'calcul', 'reponse': '-1'},
                            {'question': 'La fonction est-elle croissante si a>0 ?', 'type': 'vrai_faux', 'reponse': 'Oui'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Équations et inéquations',
                        'contenu': 'Résolution algébrique ; interprétation graphique.',
                        'exos': [
                            {'question': '3x−5=7.', 'type': 'calcul', 'reponse': 'x = 4'},
                            {'question': '2x+1≤9.', 'type': 'calcul', 'reponse': 'x ≤ 4'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 3 : Statistiques',
                        'contenu': 'Moyenne, médiane, étendue ; lecture de tableaux/diagrammes.',
                        'exos': [
                            {'question': 'Calcule la moyenne d\'une série simple.', 'type': 'redaction', 'reponse': 'Somme / nombre d\'éléments'},
                            {'question': 'Donne la médiane.', 'type': 'reponsa_courte', 'reponse': 'Valeur centrale de la série ordonnée'},
                        ]
                    }
                ],
                'physique_chimie': [
                    {
                        'titre': 'Chapitre 1 : Grandeurs et mesures',
                        'contenu': 'Unités SI, conversions, précision, incertitudes simples.',
                        'exos': [
                            {'question': 'Convertis 0,25 km en m.', 'type': 'calcul', 'reponse': '250 m'},
                            {'question': 'Donne l\'unité SI de la force.', 'type': 'reponse_courte', 'reponse': 'Newton (N)'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Mouvement rectiligne',
                        'contenu': 'Vitesse moyenne v=d/t ; graphiques x(t), v(t).',
                        'exos': [
                            {'question': '500 m en 100 s : v=?', 'type': 'calcul', 'reponse': '5 m/s'},
                            {'question': 'Interprète une pente de x(t).', 'type': 'reponse_courte', 'reponse': 'Représente la vitesse'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 3 : Électricité — Loi d\'Ohm',
                        'contenu': 'U=RI ; circuits simples ; sécurité.',
                        'exos': [
                            {'question': 'R=10 Ω, I=0,2 A : U=?', 'type': 'calcul', 'reponse': '2 V'},
                            {'question': 'Effet d\'une résistance plus grande ?', 'type': 'reponse_courte', 'reponse': 'Tension augmente (pour I constant)'},
                        ]
                    }
                ],
                'svt': [
                    {
                        'titre': 'Chapitre 1 : Cellule et tissus',
                        'contenu': 'Cellule unité du vivant ; organisation en tissus.',
                        'exos': [
                            {'question': 'Rôle du noyau ?', 'type': 'reponse_courte', 'reponse': 'Contient l\'ADN et contrôle les fonctions'},
                            {'question': 'Différence cellule/tissu ?', 'type': 'reponsa_courte', 'reponse': 'Tissu = groupe organisé de cellules similaires'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Nutrition et énergie',
                        'contenu': 'Digestion, absorption, métabolisme.',
                        'exos': [
                            {'question': 'Rôle de l\'intestin grêle ?', 'type': 'reponse_courte', 'reponse': 'Absorption des nutriments'},
                            {'question': 'Nutriment énergétique ?', 'type': 'reponse_courte', 'reponse': 'glucide, lipide, protéine'},
                        ]
                    }
                ],
                'histoire': [
                    {
                        'titre': 'Chapitre 1 : Sociétés africaines précoloniales',
                        'contenu': 'Organisation politique, économique et culturelle.',
                        'exos': [
                            {'question': 'Rôle du chef ?', 'type': 'reponse_courte', 'reponse': 'Gouverner, organiser, protéger'},
                            {'question': 'Activité économique majeure ?', 'type': 'reponse_courte', 'reponse': 'commerce, agriculture, artisanat'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Colonisation et résistances',
                        'contenu': 'Mécanismes de domination et résistances locales.',
                        'exos': [
                            {'question': 'Forme de résistance ?', 'type': 'reponse_courte', 'reponse': 'armée, diplomatie, rébellion'},
                            {'question': 'Conséquence majeure ?', 'type': 'reponsa_courte', 'reponse': 'perte d\'indépendance et de ressources'},
                        ]
                    }
                ],
                'geographie': [
                    {
                        'titre': 'Chapitre 1 : Population et dynamiques',
                        'contenu': 'Croissance, migrations, urbanisation.',
                        'exos': [
                            {'question': 'Cause de l\'urbanisation ?', 'type': 'reponse_courte', 'reponse': 'attrait économique des villes'},
                            {'question': 'Effet des migrations ?', 'type': 'reponse_courte', 'reponse': 'changement de densité de population'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Ressources et développement',
                        'contenu': 'Gestion durable, enjeux environnementaux.',
                        'exos': [
                            {'question': 'Ressource renouvelable ?', 'type': 'reponse_courte', 'reponse': 'eau, forêt, agriculture'},
                            {'question': 'Pourquoi gérer durablement ?', 'type': 'reponsa_courte', 'reponse': 'Pour les générations futures'},
                        ]
                    }
                ],
                'ecm': [
                    {
                        'titre': 'Chapitre 1 : Citoyenneté et État',
                        'contenu': 'Droits, devoirs, institutions.',
                        'exos': [
                            {'question': 'Cite un devoir civique.', 'type': 'reponsa_courte', 'reponse': 'payer impôts, participer, respecter lois'},
                            {'question': 'Rôle de l\'État ?', 'type': 'reponse_courte', 'reponse': 'gouverner, protéger, organiser la société'},
                        ]
                    },
                    {
                        'titre': 'Chapitre 2 : Démocratie et participation',
                        'contenu': 'Vote, engagement, responsabilités.',
                        'exos': [
                            {'question': 'Pourquoi voter ?', 'type': 'reponse_courte', 'reponse': 'Pour participer à la décision collective'},
                            {'question': 'Forme de participation citoyenne ?', 'type': 'reponse_courte', 'reponse': 'vote, bénévolat, engagement associatif'},
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
                            'niveau_scolaire': 'seconde',
                            'niveau_global': 'avancé',
                            'ordre': idx,
                            'difficulte': 6,
                            'temps_estime': 35,
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
                                'niveau': 'seconde',
                                'ordre': ex_idx,
                            }
                        )
                        created_exos += 1

            self.stdout.write(self.style.SUCCESS(f"\n✅ 2nde population terminée: {created_lecons} leçons, {created_exos} exercices créés/actualisés."))

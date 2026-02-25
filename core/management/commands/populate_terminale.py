from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Matiere, Lecon, Exercice


class Command(BaseCommand):
    help = "Populate Terminale curriculum (BAC level)"

    def handle(self, *args, **options):
        self.stdout.write("🚀 Starting Terminale population...")

        with transaction.atomic():
            # Map subjects from Matiere.MATIERE_CHOICES
            matieres_map = {
                'francais': 'Français',
                'mathematiques': 'Mathématiques',
                'physique_chimie': 'Physique-Chimie',
                'svt': 'SVT',
                'histoire': 'Histoire',
                'geographie': 'Géographie',
                'education_civique': 'Éducation civique',
            }

            # Create/get Matière objects
            matieres = {}
            for code, nom in matieres_map.items():
                matiere, _ = Matiere.objects.get_or_create(
                    nom=nom,
                    defaults={'description': f'{nom} pour Terminale'}
                )
                matieres[code] = matiere

            # Define Terminale program (BAC level)
            programme_terminale = {
                'francais': {
                    'Chapitre 1 : Dissertation littéraire': {
                        'contenu': "La dissertation est un raisonnement structuré : introduction (problématique), développement (arguments organisés), conclusion.\nMaîtrise des œuvres, citations, analyse stylistique.",
                        'exercices': [
                            "Distingue thème et problématique.",
                            "Propose un plan dialectique."
                        ]
                    },
                    'Chapitre 2 : Commentaire composé': {
                        'contenu': "Analyse méthodique d'un texte : axes, procédés, interprétation.",
                        'exercices': [
                            "Identifie deux procédés stylistiques.",
                            "Explique leur effet."
                        ]
                    }
                },
                'mathematiques': {
                    'Chapitre 1 : Fonctions (analyse approfondie)': {
                        'contenu': "Étude complète : domaine, limites, continuité, dérivabilité, variations, extremums.\nInterprétation graphique.",
                        'exercices': [
                            "Étudie les variations de f(x)=x³−3x²+2.",
                            "Détermine les extremums."
                        ]
                    },
                    'Chapitre 2 : Dérivation avancée': {
                        'contenu': "Règles de dérivation, composition, applications à l'optimisation.",
                        'exercices': [
                            "Dérive f(x)=(2x−1)(x²+3).",
                            "Problème d'optimisation (aire maximale)."
                        ]
                    },
                    'Chapitre 3 : Intégration': {
                        'contenu': "Primitive, intégrale définie, aire sous la courbe.",
                        'exercices': [
                            "Calcule ∫(2x+1)dx.",
                            "Aire comprise entre une courbe et l'axe."
                        ]
                    },
                    'Chapitre 4 : Probabilités et statistiques': {
                        'contenu': "Variables aléatoires, loi uniforme, interprétation statistique.",
                        'exercices': [
                            "Calcule une probabilité conditionnelle simple.",
                            "Interprète une variance."
                        ]
                    }
                },
                'physique_chimie': {
                    'Chapitre 1 : Cinématique et dynamique': {
                        'contenu': "Mouvement rectiligne et curviligne, lois de Newton, forces, équations horaires.",
                        'exercices': [
                            "Calcule la vitesse et l'accélération d'un mobile.",
                            "Applique la 2ᵉ loi de Newton."
                        ]
                    },
                    'Chapitre 2 : Travail, énergie et puissance': {
                        'contenu': "Énergie cinétique, potentielle, théorème de l'énergie mécanique.",
                        'exercices': [
                            "Calcule l'énergie cinétique d'un corps.",
                            "Étudie la conservation de l'énergie."
                        ]
                    },
                    'Chapitre 3 : Électricité — Circuits complexes': {
                        'contenu': "Lois des mailles et des nœuds, résistances équivalentes.",
                        'exercices': [
                            "Calcule l'intensité dans un circuit.",
                            "Analyse un circuit mixte."
                        ]
                    },
                    'Chapitre 4 : Chimie — Réactions et équilibres': {
                        'contenu': "Réaction chimique, équation bilan, conservation de la matière, rendement.",
                        'exercices': [
                            "Écris une équation chimique équilibrée.",
                            "Calcule un rendement."
                        ]
                    }
                },
                'svt': {
                    'Chapitre 1 : Génétique et hérédité': {
                        'contenu': "Transmission des caractères, ADN, mutations.",
                        'exercices': [
                            "Rôle de l'ADN ?",
                            "Qu'est-ce qu'une mutation ?"
                        ]
                    },
                    'Chapitre 2 : Environnement et santé': {
                        'contenu': "Pollution, maladies, prévention.",
                        'exercices': [
                            "Impact de la pollution ?",
                            "Mesure de prévention ?"
                        ]
                    }
                },
                'histoire': {
                    'Chapitre 1 : Décolonisation et États africains': {
                        'contenu': "Processus d'indépendance, défis politiques et économiques.",
                        'exercices': [
                            "Cite un défi post-indépendance.",
                            "Pourquoi la décolonisation fut difficile ?"
                        ]
                    },
                    'Chapitre 2 : Monde contemporain': {
                        'contenu': "Conflits, organisations internationales, enjeux géopolitiques.",
                        'exercices': [
                            "Rôle de l'ONU ?",
                            "Cause d'un conflit actuel."
                        ]
                    }
                },
                'geographie': {
                    'Chapitre 1 : Développement et mondialisation': {
                        'contenu': "Inégalités Nord-Sud, indicateurs de développement.",
                        'exercices': [
                            "Cite un indicateur.",
                            "Analyse une inégalité."
                        ]
                    },
                    'Chapitre 2 : Environnement et développement durable': {
                        'contenu': "Changements climatiques, solutions durables.",
                        'exercices': [
                            "Cause du réchauffement ?",
                            "Solution durable ?"
                        ]
                    }
                },
                'education_civique': {
                    'Chapitre 1 : État de droit et démocratie': {
                        'contenu': "Séparation des pouvoirs, constitution, citoyenneté.",
                        'exercices': [
                            "Explique la séparation des pouvoirs.",
                            "Rôle du citoyen ?"
                        ]
                    },
                    'Chapitre 2 : Paix et sécurité': {
                        'contenu': "Conflits, médiation, cohésion nationale.",
                        'exercices': [
                            "Moyen de prévention des conflits ?",
                            "Importance de la paix ?"
                        ]
                    }
                }
            }

            # Create Leçons and Exercices
            total_lecons = 0
            total_exercices = 0

            for matiere_code, chapitres in programme_terminale.items():
                matiere = matieres[matiere_code]

                for titre_chapitre, data in chapitres.items():
                    # Create/update Leçon
                    lecon, _ = Lecon.objects.update_or_create(
                        titre=titre_chapitre,
                        matiere=matiere,
                        niveau_scolaire='terminale',
                        defaults={
                            'contenu_principal': data['contenu'],
                            'niveau_global': 'avancé',
                            'difficulte': 8,
                            'temps_estime': 45
                        }
                    )
                    total_lecons += 1

                    # Create Exercices
                    for idx, enonce in enumerate(data['exercices'], 1):
                        exercice, _ = Exercice.objects.update_or_create(
                            lecon=lecon,
                            question=enonce,
                            defaults={
                                'matiere': matiere,
                                'type_exercice': 'reponse_courte',
                                'difficulte': 8,
                                'reponse_correcte': ''
                            }
                        )
                        total_exercices += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Terminale population terminée: {total_lecons} leçons, {total_exercices} exercices créés/actualisés.'
                )
            )

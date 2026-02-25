from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Matiere, Lecon, Exercice


class Command(BaseCommand):
    help = "Populate 1ère curriculum"

    def handle(self, *args, **options):
        self.stdout.write("🚀 Starting 1ère population...")

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
                    defaults={'description': f'{nom} pour 1ère'}
                )
                matieres[code] = matiere

            # Define 1ère program
            programme_1ere = {
                'francais': {
                    'Chapitre 1 : Le théâtre': {
                        'contenu': "Le théâtre est un genre littéraire destiné à être joué sur scène.\nIl est composé d'actes et de scènes. Le dialogue est central et fait avancer l'action.\nLes didascalies donnent des indications de jeu, de décor et de gestes.",
                        'exercices': [
                            "Quelle est la différence entre dialogue et didascalie ?",
                            "Pourquoi le théâtre est-il fait pour être joué ?"
                        ]
                    },
                    'Chapitre 2 : L\'argumentation indirecte': {
                        'contenu': "L'argumentation indirecte défend une idée à travers un récit (conte, fable, roman).\nElle permet de critiquer la société sans attaquer directement.",
                        'exercices': [
                            "Cite un genre utilisé pour l'argumentation indirecte.",
                            "Pourquoi l'auteur utilise-t-il ce procédé ?"
                        ]
                    }
                },
                'mathematiques': {
                    'Chapitre 1 : Fonctions du second degré': {
                        'contenu': "Une fonction du second degré est de la forme f(x)=ax²+bx+c.\nSa courbe est une parabole.\nLe signe de a détermine l'ouverture.",
                        'exercices': [
                            "Identifie a, b, c dans f(x)=2x²−3x+1.",
                            "La parabole est-elle ouverte vers le haut si a>0 ?"
                        ]
                    },
                    'Chapitre 2 : Dérivation (initiation)': {
                        'contenu': "La dérivée d'une fonction représente son taux de variation.\nElle permet d'étudier les variations d'une fonction.",
                        'exercices': [
                            "La dérivée sert à étudier quoi ?",
                            "Une fonction croissante a une dérivée de quel signe ?"
                        ]
                    },
                    'Chapitre 3 : Probabilités': {
                        'contenu': "La probabilité mesure la chance qu'un événement se réalise.\nElle est comprise entre 0 et 1.",
                        'exercices': [
                            "Probabilité d'obtenir pile avec une pièce ?",
                            "Un événement certain a quelle probabilité ?"
                        ]
                    }
                },
                'physique_chimie': {
                    'Chapitre 1 : Mouvement et lois de Newton': {
                        'contenu': "Les lois de Newton décrivent le mouvement des corps.\nLa force est responsable de la variation du mouvement.",
                        'exercices': [
                            "Que produit une force sur un objet ?",
                            "Cite une force de la vie quotidienne."
                        ]
                    },
                    'Chapitre 2 : Travail et énergie': {
                        'contenu': "Le travail d'une force correspond à l'énergie échangée.\nL'énergie peut être cinétique ou potentielle.",
                        'exercices': [
                            "Qu'est-ce que l'énergie cinétique ?",
                            "Donne un exemple d'énergie potentielle."
                        ]
                    },
                    'Chapitre 3 : Chimie — Réactions chimiques': {
                        'contenu': "Une réaction chimique transforme des réactifs en produits.\nLa masse se conserve au cours d'une réaction.",
                        'exercices': [
                            "Que deviennent les réactifs ?",
                            "La masse se conserve-t-elle toujours ?"
                        ]
                    }
                },
                'svt': {
                    'Chapitre 1 : Génétique': {
                        'contenu': "Les caractères héréditaires sont transmis par les gènes.\nLes chromosomes portent l'information génétique.",
                        'exercices': [
                            "Où se trouvent les gènes ?",
                            "Qu'est-ce qu'un caractère héréditaire ?"
                        ]
                    },
                    'Chapitre 2 : Écosystèmes': {
                        'contenu': "Un écosystème comprend des êtres vivants et leur milieu.\nLes équilibres sont fragiles.",
                        'exercices': [
                            "Cite un écosystème.",
                            "Pourquoi faut-il le protéger ?"
                        ]
                    }
                },
                'histoire': {
                    'Chapitre 1 : Le monde au XIXe siècle': {
                        'contenu': "Le XIXe siècle est marqué par les révolutions industrielles et politiques.",
                        'exercices': [
                            "Cite une transformation majeure.",
                            "Quel continent est le plus industrialisé ?"
                        ]
                    },
                    'Chapitre 2 : Colonisation et impérialisme': {
                        'contenu': "Les puissances européennes étendent leur domination au XIXe siècle.",
                        'exercices': [
                            "Pourquoi coloniser ?",
                            "Conséquence pour l'Afrique ?"
                        ]
                    }
                },
                'geographie': {
                    'Chapitre 1 : Mondialisation': {
                        'contenu': "La mondialisation est l'intensification des échanges à l'échelle mondiale.",
                        'exercices': [
                            "Cite un effet de la mondialisation.",
                            "Qui en profite le plus ?"
                        ]
                    },
                    'Chapitre 2 : Développement durable': {
                        'contenu': "Le développement durable répond aux besoins présents sans compromettre l'avenir.",
                        'exercices': [
                            "Cite un pilier du développement durable.",
                            "Pourquoi protéger l'environnement ?"
                        ]
                    }
                },
                'education_civique': {
                    'Chapitre 1 : Droits humains': {
                        'contenu': "Les droits humains garantissent la dignité de chaque personne.",
                        'exercices': [
                            "Cite un droit humain.",
                            "Pourquoi les respecter ?"
                        ]
                    },
                    'Chapitre 2 : Paix et cohésion sociale': {
                        'contenu': "La paix repose sur le respect, la justice et le dialogue.",
                        'exercices': [
                            "Donne une action pour la paix.",
                            "Pourquoi la cohésion sociale est importante ?"
                        ]
                    }
                }
            }

            # Create Leçons and Exercices
            total_lecons = 0
            total_exercices = 0

            for matiere_code, chapitres in programme_1ere.items():
                matiere = matieres[matiere_code]

                for titre_chapitre, data in chapitres.items():
                    # Create/update Leçon
                    lecon, _ = Lecon.objects.update_or_create(
                        titre=titre_chapitre,
                        matiere=matiere,
                        niveau_scolaire='1ere',
                        defaults={
                            'contenu_principal': data['contenu'],
                            'niveau_global': 'avancé',
                            'difficulte': 7,
                            'temps_estime': 40
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
                                'difficulte': 7,
                                'reponse_correcte': ''
                            }
                        )
                        total_exercices += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ 1ère population terminée: {total_lecons} leçons, {total_exercices} exercices créés/actualisés.'
                )
            )

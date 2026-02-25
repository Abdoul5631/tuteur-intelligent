"""
Management command pour peupler le curriculum complet de l'application
Crée tous les niveaux scolaires, matières, leçons et exercices de démonstration
"""

from django.core.management.base import BaseCommand
from core.models import Matiere, Lecon, Exercice


class Command(BaseCommand):
    help = 'Peupler le curriculum complet avec des données réalistes'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Début du peuplement du curriculum...\n")
        
        # Définition du curriculum complet
        curriculum = {
            # ================== PRIMAIRE ==================
            "CP1": {
                "Mathématiques": {
                    "lecons": [
                        {
                            "titre": "Les nombres de 0 à 10",
                            "contenu_principal": "Apprendre à reconnaître et écrire les nombres de 0 à 10. Les nombres sont des symboles pour représenter des quantités.",
                            "contenu_simplifie": "Les chiffres 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10",
                            "contenu_approfondi": "Numération, décomposition, comparaison de quantités"
                        },
                        {
                            "titre": "Additions simples",
                            "contenu_principal": "Additionner deux nombres simples (résultat ≤ 10)",
                            "contenu_simplifie": "1 + 1 = 2, 2 + 3 = 5",
                            "contenu_approfondi": "Propriété commutative: 2 + 3 = 3 + 2"
                        }
                    ]
                },
                "Français": {
                    "lecons": [
                        {
                            "titre": "Reconnaissance des lettres",
                            "contenu_principal": "Apprendre l'alphabet et reconnaître les majuscules et minuscules",
                            "contenu_simplifie": "A, a, B, b, C, c...",
                            "contenu_approfondi": "Phonétique associée à chaque lettre"
                        },
                        {
                            "titre": "Lecture simple",
                            "contenu_principal": "Lire des mots simples et courts",
                            "contenu_simplifie": "chat, rat, soleil, maison",
                            "contenu_approfondi": "Syllabes et phonèmes"
                        }
                    ]
                }
            },
            "CM1": {
                "Mathématiques": {
                    "lecons": [
                        {
                            "titre": "Les fractions simples",
                            "contenu_principal": "Une fraction représente une partie d'un tout. 1/2 signifie une partie sur deux.",
                            "contenu_simplifie": "1/2 = moitié, 1/4 = quart, 1/3 = tiers",
                            "contenu_approfondi": "Numérateur, dénominateur, fractions équivalentes"
                        },
                        {
                            "titre": "Multiplication et division",
                            "contenu_principal": "La multiplication est une addition répétée. 3 × 4 = 12",
                            "contenu_simplifie": "Tables de 1 à 10",
                            "contenu_approfondi": "Propriétés (commutative, associative), technique de division"
                        },
                        {
                            "titre": "Périmètre et Aire",
                            "contenu_principal": "Périmètre = distance autour. Aire = espace dedans.",
                            "contenu_simplifie": "Périmètre = 4 × côté (carré), Aire = longueur × largeur (rectangle)",
                            "contenu_approfondi": "Formules pour différentes formes géométriques"
                        }
                    ]
                },
                "Français": {
                    "lecons": [
                        {
                            "titre": "Les verbes et conjugaison",
                            "contenu_principal": "Un verbe exprime une action. Exemple: courir, sauter, manger.",
                            "contenu_simplifie": "Présent: je suis, tu es, il/elle est",
                            "contenu_approfondi": "Conjugaison au présent, passé composé, futur simple"
                        },
                        {
                            "titre": "L'accord des adjectifs",
                            "contenu_principal": "L'adjectif décrit le nom et doit s'accorder avec lui.",
                            "contenu_simplifie": "un chat noir, une maison blanche",
                            "contenu_approfondi": "Accords en genre et nombre"
                        },
                        {
                            "titre": "Introduction à la littérature",
                            "contenu_principal": "Lire et comprendre de petits textes (contes, fables)",
                            "contenu_simplifie": "La cigale et la fourmi, Le corbeau et le renard",
                            "contenu_approfondi": "Analyse de personnages, morale de l'histoire"
                        }
                    ]
                },
                "Sciences": {
                    "lecons": [
                        {
                            "titre": "Le cycle de l'eau",
                            "contenu_principal": "L'eau s'évapore du soleil, monte, refroidit et retombe en pluie.",
                            "contenu_simplifie": "Évaporation → Condensation → Précipitation",
                            "contenu_approfondi": "États de l'eau, points de changement d'état"
                        }
                    ]
                }
            },
            # ================== COLLÈGE ==================
            "6ème": {
                "Mathématiques": {
                    "lecons": [
                        {
                            "titre": "Les nombres entiers et décimaux",
                            "contenu_principal": "Les nombres décimaux possèdent une virgule. Exemple: 3,14",
                            "contenu_simplifie": "Partie entière et partie décimale",
                            "contenu_approfondi": "Comparaison, ordre, opérations sur décimaux"
                        },
                        {
                            "titre": "Équations du premier degré",
                            "contenu_principal": "Résoudre une équation comme 2x + 5 = 13",
                            "contenu_simplifie": "Isoler x en inversant les opérations",
                            "contenu_approfondi": "Vérification de la solution, graphique"
                        },
                        {
                            "titre": "Géométrie: angles et triangles",
                            "contenu_principal": "Un angle se mesure en degrés. Trois types: aigu (<90°), droit (90°), obtus (>90°)",
                            "contenu_simplifie": "Triangle isocèle, équilatéral, rectangle",
                            "contenu_approfondi": "Propriétés, calcul d'angles"
                        }
                    ]
                },
                "Français": {
                    "lecons": [
                        {
                            "titre": "La phrase complexe",
                            "contenu_principal": "Une phrase complexe contient une proposition principal et una ou plusieurs subordonnées.",
                            "contenu_simplifie": "Proposition principal + subordinée (qui, que, parce que)",
                            "contenu_approfondi": "Classification des propositions, ponctuation"
                        },
                        {
                            "titre": "Orthographe: homophones",
                            "contenu_principal": "Des mots qui se prononcent pareil mais n'ont pas le même sens.",
                            "contenu_simplifie": "a/à, c'est/ces/ses, ou/où, dont/do",
                            "contenu_approfondi": "Stratégies de distinction"
                        }
                    ]
                },
                "SVT": {
                    "lecons": [
                        {
                            "titre": "La biodiversité",
                            "contenu_principal": "Chaque région a sa propre flore et faune spécifiques.",
                            "contenu_simplifie": "Animaux et plantes d'une région donnée",
                            "contenu_approfondi": "Écosystème, chaîne alimentaire, adaptation"
                        }
                    ]
                }
            },
            "3ème": {
                "Mathématiques": {
                    "lecons": [
                        {
                            "titre": "Le théorème de Pythagore",
                            "contenu_principal": "Dans un triangle rectangle: a² + b² = c²",
                            "contenu_simplifie": "3² + 4² = 5²: 9 + 16 = 25",
                            "contenu_approfondi": "Réciproque, applications géométriques"
                        },
                        {
                            "titre": "Probabilités",
                            "contenu_principal": "La probabilité mesure la chance qu'un événement arrive (entre 0 et 1).",
                            "contenu_simplifie": "Probabilité du dé: 1/6 pour chaque face",
                            "contenu_approfondi": "Événements incompatibles, indépendants"
                        }
                    ]
                },
                "Français": {
                    "lecons": [
                        {
                            "titre": "Analyse littéraire",
                            "contenu_principal": "Étudier un texte: auteur, contexte, style, message",
                            "contenu_simplifie": "Qui a écrit? Quand? Pour dire quoi?",
                            "contenu_approfondi": "Figures de style, ton, perspective narrative"
                        }
                    ]
                }
            },
            # ================== LYCÉE ==================
            "2nde": {
                "Mathématiques": {
                    "lecons": [
                        {
                            "titre": "Fonctions linéaires et affines",
                            "contenu_principal": "Fonction linéaire: f(x) = ax. Fonction affine: f(x) = ax + b",
                            "contenu_simplifie": "Représentation graphique = droite",
                            "contenu_approfondi": "Pente, ordonnée à l'origine, résolution d'équation"
                        },
                        {
                            "titre": "Statistiques et probabilités",
                            "contenu_principal": "Moyenne, médiane, écart-type; fréquence et probabilité",
                            "contenu_simplifie": "Moyenne = somme / nombre d'éléments",
                            "contenu_approfondi": "Variance, écart-type, loi binomiale"
                        }
                    ]
                },
                "Philosophie": {
                    "lecons": [
                        {
                            "titre": "Introduction à la philosophie",
                            "contenu_principal": "La philosophie pose les grandes questions: Qu'est-ce que le bien? Qu'est-ce que la justice?",
                            "contenu_simplifie": "Penser, douter, réfléchir",
                            "contenu_approfondi": "Principales écoles de pensée"
                        }
                    ]
                }
            },
            "Terminale": {
                "Mathématiques": {
                    "lecons": [
                        {
                            "titre": "Dérivées et intégrales",
                            "contenu_principal": "Dérivée = taux de variation. Intégrale = aire sous la courbe.",
                            "contenu_simplifie": "Dérivée de x² = 2x",
                            "contenu_approfondi": "Théorème fondamental du calcul, applications en physique"
                        }
                    ]
                },
                "Philosophie": {
                    "lecons": [
                        {
                            "titre": "L'existence et le sens",
                            "contenu_principal": "Qu'est-ce qui donne un sens à l'existence? Liberté, responsabilité, mort",
                            "contenu_simplifie": "questions existentielles",
                            "contenu_approfondi": "Existentialisme, absurdisme, nihilisme"
                        }
                    ]
                }
            }
        }

        # Exercices par type
        all_exercises_by_level = {
            "CP1": [
                {"question": "Quel nombre vient après 5?", "reponse": "6", "type": "Nombre"},
                {"question": "2 + 3 = ?", "reponse": "5", "type": "Addition"},
            ],
            "CM1": [
                {"question": "Convertis 1/2 en décimal", "reponse": "0.5", "type": "Fraction"},
                {"question": "Quel est le périmètre d'un carré de 5 cm?", "reponse": "20 cm", "type": "Géometrie"},
                {"question": "5 × 6 = ?", "reponse": "30", "type": "Multiplication"},
            ],
            "6ème": [
                {"question": "Résous: 2x + 5 = 13", "reponse": "4", "type": "Équation"},
                {"question": "Quel est le cube de 2?", "reponse": "8", "type": "Calcul"},
                {"question": "Un triangle isocèle a combien de côtés égaux?", "reponsa": "2", "type": "Géométrie"},
            ],
            "3ème": [
                {"question": "3² + 4² = ?", "reponse": "25", "type": "Pythagore"},
                {"question": "Probabilité de tirer un as dans 52 cartes?", "reponse": "4/52 ou 1/13", "type": "Probabilité"},
            ],
            "2nde": [
                {"question": "Quelle est la dérivée de x³?", "reponse": "3x²", "type": "Dérivée"},
                {"question": "La pente de la droite y = 2x + 3?", "reponse": "2", "type": "Fonction"},
            ],
            "Terminale": [
                {"question": "Intégrale de x dx?", "reponse": "x²/2 + C", "type": "Intégrale"},
                {"question": "log(1000) en base 10?", "reponse": "3", "type": "Logarithme"},
            ]
        }

        total_matieres = 0
        total_lecons = 0
        total_exercices = 0

        # Créer les matieres et lecons
        for niveau, matieres_dict in curriculum.items():
            # Normaliser le code du niveau
            niveau_code = nivel_name_to_code(niveau)
            
            for matiere_name, lessons_dict in matieres_dict.items():
                # Mapper le nom en code de choix
                matiere_code = matiere_name_to_code(matiere_name)
                
                # Créer ou récupérer la matière
                matiere, created = Matiere.objects.get_or_create(
                    nom=matiere_code,
                    niveau_scolaire=niveau_code
                )
                if created:
                    total_matieres += 1
                    self.stdout.write(f"  ✓ Matière créée: {matiere_name} ({niveau})")
                
                # Créer les leçons
                for idx, lesson_data in enumerate(lessons_dict.get("lecons", []), 1):
                    lecon, created = Lecon.objects.get_or_create(
                        titre=lesson_data["titre"],
                        matiere=matiere,
                        defaults={
                            "contenu_principal": lesson_data.get("contenu_principal", ""),
                            "contenu_simplifie": lesson_data.get("contenu_simplifie", ""),
                            "contenu_approfondi": lesson_data.get("contenu_approfondi", ""),
                        }
                    )
                    if created:
                        total_lecons += 1
                        self.stdout.write(f"    └─ Leçon: {lesson_data['titre']}")
                    
                    # Créer des exercices pour cette leçon
                    exercises = all_exercises_by_level.get(niveau, [])
                    for ex_idx, exercise_data in enumerate(exercises[:3], 1):  # 3 exos par leçon max
                        exercice, created = Exercice.objects.get_or_create(
                            lecon=lecon,
                            question=exercise_data["question"],
                            defaults={
                                "reponse": exercise_data.get("reponse", exercise_data.get("reponsa", "")),
                                "type": exercise_data.get("type", "Général"),
                            }
                        )
                        if created:
                            total_exercices += 1
                            self.stdout.write(f"       └─ Exercice {ex_idx}: {exercise_data['question'][:50]}...")

        # Résumé
        self.stdout.write("\n" + "="*60)
        self.stdout.write(self.style.SUCCESS(f"""
✅ CURRICULUM COMPLET CRÉÉ!

📊 Statistiques:
   • Matières: {total_matieres}
   • Leçons: {total_lecons}
   • Exercices: {total_exercices}

🎓 Niveaux inclus:
   • Primaire: CP1, CM1
   • Collège: 6ème, 3ème
   • Lycée: 2nde, Terminale

💡 Prêt pour le test complet!
        """))
        self.stdout.write("="*60)

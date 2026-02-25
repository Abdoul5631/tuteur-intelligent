"""
Moteur IA pédagogique local 🎓
Sans dépendances externes, basé sur :
- Analyse de mots-clés
- Base de connaissances pédagogiques
- Templates dynamiques par niveau
"""

import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime

# ========================
# BASE DE CONNAISSANCES PÉDAGOGIQUES
# ========================

KNOWLEDGE_BASE = {
    "volume": {
        "keywords": ["volume", "espace", "pavé", "cube", "sphère", "cylindre"],
        "cm1_cm2": {
            "explanation": (
                "Le volume permet de savoir combien d'espace occupe un objet.\n\n"
                "Pour un **pavé droit** (boîte) :\n"
                "**Volume = longueur × largeur × hauteur**\n\n"
                "Pour un **cube** (tous les côtés égaux) :\n"
                "**Volume = côté × côté × côté**\n\n"
                "Pour une **sphère** :\n"
                "**Volume = 4/3 × π × rayon³**"
            ),
            "examples": [
                "Une boîte de 5 cm × 4 cm × 3 cm a un volume de 60 cm³",
                "Un cube de 2 m de côté a un volume de 8 m³"
            ]
        },
        "6eme_5eme": {
            "explanation": (
                "Le volume d'un solide est la mesure de l'espace qu'il occupe.\n\n"
                "**Formules principales :**\n"
                "- Pavé droit : V = L × l × h\n"
                "- Cube : V = a³\n"
                "- Cylindre : V = π × r² × h\n"
                "- Sphère : V = 4/3 × π × r³\n"
                "- Cône : V = 1/3 × π × r² × h\n"
                "- Pyramide : V = 1/3 × aire_base × hauteur"
            ),
            "examples": [
                "Volume d'une piscine de 8 m × 5 m × 2 m = 80 m³",
                "Volume d'une canette cylindrique de rayon 4 cm et hauteur 12 cm"
            ]
        },
        "4eme_3eme": {
            "explanation": (
                "Le volume d'un solide est un scalaire mesurant l'étendue 3D.\n\n"
                "**Formules généralisées :**\n"
                "- Solides réguliers : utiliser les formules spécifiques\n"
                "- Changements d'unités : 1 m³ = 1000 L\n"
                "- Principe de Cavalieri : solides de même hauteur = même volume\n"
                "\n**Applications pratiques :**\n"
                "- Calcul de capacité (litres)\n"
                "- Densité = masse / volume"
            ),
            "examples": [
                "Trouver le rayon d'une sphère de volume 4186 cm³",
                "Une piscine de 10 m³ contient combien de litres ?"
            ]
        }
    },
    "aire": {
        "keywords": ["aire", "surface", "périmètre", "rectangle", "carré", "triangle", "cercle"],
        "cm1_cm2": {
            "explanation": (
                "L'aire est la mesure de la surface d'une forme.\n\n"
                "**Formules simples :**\n"
                "- Carré : **Aire = côté × côté**\n"
                "- Rectangle : **Aire = longueur × largeur**\n"
                "- Triangle : **Aire = base × hauteur ÷ 2**\n"
                "- Cercle : **Aire = π × rayon²**"
            ),
            "examples": [
                "Un carré de 5 cm de côté a une aire de 25 cm²",
                "Un rectangle de 6 m × 4 m a une aire de 24 m²"
            ]
        },
        "6eme_5eme": {
            "explanation": (
                "L'aire mesure la surface d'une figure plane exprimée en unités carrées.\n\n"
                "**Formules principales :**\n"
                "- Triangle : A = (base × hauteur) / 2\n"
                "- Parallélogramme : A = base × hauteur\n"
                "- Trapèze : A = ((base1 + base2) × hauteur) / 2\n"
                "- Disque : A = π × r²\n\n"
                "Attention : ne pas confondre **aire** et **périmètre**"
            ),
            "examples": [
                "Aire d'un triangle avec base 8 cm et hauteur 5 cm",
                "Aire d'un trapèze avec bases 4 m et 6 m, hauteur 3 m"
            ]
        },
        "4eme_3eme": {
            "explanation": (
                "L'aire est une grandeur géométrique mesurant l'étendue d'une surface.\n\n"
                "**Propriétés :**\n"
                "- Invariante par translation et rotation\n"
                "- Additive pour les figures composées\n"
                "- Unités : m², cm², hectare, etc.\n\n"
                "**Cas complexes :**\n"
                "- Figures composées : décomposer\n"
                "- Figures courbes : approximation ou intégration\n"
                "- Conversions d'unités"
            ),
            "examples": [
                "Calculer l'aire d'une figure en L composée de deux rectangles",
                "Convertir 2,5 ha en m²"
            ]
        }
    },
    "theoreme_pythagore": {
        "keywords": ["pythagore", "hypoténuse", "triangle rectangle", "carré", "racine"],
        "cm1_cm2": {
            "explanation": (
                "Le **théorème de Pythagore** s'applique aux **triangles rectangles**.\n\n"
                "Dans un triangle rectangle :\n"
                "**hypoténuse² = côté1² + côté2²**\n\n"
                "Exemple : Dans un triangle de côtés 3 et 4 :\n"
                "hypoténuse² = 3² + 4² = 9 + 16 = 25\n"
                "hypoténuse = 5"
            ),
            "examples": [
                "Triangle avec côtés 5 et 12 : hypoténuse = 13",
                "Triangle avec côtés 6 et 8 : hypoténuse = 10"
            ]
        },
        "6eme_5eme": {
            "explanation": (
                "**Théorème de Pythagore :**\n"
                "Dans un triangle rectangle, le carré de l'hypoténuse égale la somme des carrés des deux autres côtés.\n\n"
                "c² = a² + b²\n\n"
                "**Réciproque :** Si c² = a² + b², alors le triangle est rectangle.\n\n"
                "**Applications :**\n"
                "- Vérifier si un triangle est rectangle\n"
                "- Calculer une longueur manquante"
            ),
            "examples": [
                "Vérifier si 5, 12, 13 forment un triangle rectangle",
                "Trouver la hauteur d'une échelle appuyée sur un mur"
            ]
        },
        "4eme_3eme": {
            "explanation": (
                "**Théorème de Pythagore et applications :**\n\n"
                "Énoncé : Dans tout triangle rectangle, c² = a² + b²\n\n"
                "**Réciproque et contraposée :**\n"
                "- Si c² = a² + b² alors le triangle est rectangle\n"
                "- Si c² ≠ a² + b² alors le triangle n'est pas rectangle\n\n"
                "**Extensions :**\n"
                "- Généralisation en 3D\n"
                "- Calcul de distances\n"
                "- Loi du cosinus (généralisation)"
            ),
            "examples": [
                "Calculer la diagonale d'un parallélépipède",
                "Vérifier la relation entre côtés d'un triangle quelconque"
            ]
        }
    },
    "fractions": {
        "keywords": ["fraction", "numérateur", "dénominateur", "division", "simplifier"],
        "cm1_cm2": {
            "explanation": (
                "Une **fraction** représente une partie d'un tout.\n\n"
                "**3/4** se dit \"trois quarts\" :\n"
                "- 3 = numérateur (partie du haut)\n"
                "- 4 = dénominateur (nombre de parts) (partie du bas)\n\n"
                "Exemple : Une pizza coupée en 4 parts. Si tu en manges 3, tu as mangé 3/4 de pizza."
            ),
            "examples": [
                "1/2 = la moitié",
                "2/3 = deux tiers"
            ]
        },
        "6eme_5eme": {
            "explanation": (
                "**Fractions et opérations :**\n\n"
                "Simplifier : diviser numérateur et dénominateur par le même nombre\n"
                "3/6 = 1/2\n\n"
                "**Addition/Soustraction :** même dénominateur d'abord\n"
                "1/4 + 2/4 = 3/4\n\n"
                "**Multiplication :** numérateur × numérateur, dénominateur × dénominateur\n"
                "2/3 × 3/4 = 6/12 = 1/2"
            ),
            "examples": [
                "Simplifier 8/12",
                "Calculer 1/3 + 1/6",
                "Multiplier 2/5 × 3/7"
            ]
        },
        "4eme_3eme": {
            "explanation": (
                "**Fractions, rationnels et algèbre :**\n\n"
                "Propriétés d'égalité : a/b = c/d ⟺ ad = bc\n\n"
                "**Opérations rationnelles :**\n"
                "- Division : (a/b) ÷ (c/d) = (a/b) × (d/c)\n"
                "- Puissance : (a/b)ⁿ = aⁿ/bⁿ\n"
                "- Inverse : inverse de a/b est b/a\n\n"
                "Applications : proportions, pourcentages, probabilités"
            ),
            "examples": [
                "Résoudre x/3 = 4/6",
                "Calculer (2/3)³",
                "Simplifier ((4/5) × (10/3)) ÷ (2/9)"
            ]
        }
    }
}

# ========================
# GÉNÉRATEUR D'EXERCICES
# ========================

EXERCISE_TEMPLATES = {
    "volume": {
        "cm1_cm2": [
            {
                "template": "Un carton mesure {j} cm de long, {k} cm de large et {l} cm de haut. Calcule son volume.",
                "params": {"j": range(3, 10), "k": range(3, 10), "l": range(3, 8)},
                "answer_type": "multiplication"
            },
            {
                "template": "Un cube a {a} cm de côté. Quel est son volume ?",
                "params": {"a": range(2, 8)},
                "answer_type": "cube"
            }
        ],
        "6eme_5eme": [
            {
                "template": "Calcule le volume d'un cylindre de rayon {r} cm et de hauteur {h} cm.",
                "params": {"r": range(2, 6), "h": range(5, 15)},
                "answer_type": "cylinder"
            },
            {
                "template": "Un réservoir en forme de pavé droit a pour dimensions {l}m × {w}m × {d}m. Quel est son volume en litres ?",
                "params": {"l": range(2, 6), "w": range(2, 6), "d": range(1, 4)},
                "answer_type": "capacity"
            }
        ],
        "4eme_3eme": [
            {
                "template": "Une sphère a un volume de {v} cm³. Calcule son rayon (arrondir à 0,1 cm).",
                "params": {"v": [1000, 2000, 4000, 8000]},
                "answer_type": "inverse_sphere"
            },
            {
                "template": "Un cône a pour base un cercle de rayon {r} cm et pour hauteur {h} cm. Calcule son volume.",
                "params": {"r": range(3, 7), "h": range(6, 15)},
                "answer_type": "cone"
            }
        ]
    },
    "aire": {
        "cm1_cm2": [
            {
                "template": "Un rectangle a pour longueur {l} cm et largeur {w} cm. Calcule son aire.",
                "params": {"l": range(4, 12), "w": range(2, 10)},
                "answer_type": "rectangle_area"
            },
            {
                "template": "Un carré a {a} cm de côté. Quelle est son aire ?",
                "params": {"a": range(3, 10)},
                "answer_type": "square_area"
            }
        ],
        "6eme_5eme": [
            {
                "template": "Un triangle a une base de {b} cm et une hauteur de {h} cm. Calcule son aire.",
                "params": {"b": range(4, 12), "h": range(3, 10)},
                "answer_type": "triangle_area"
            },
            {
                "template": "Un disque a un rayon de {r} cm. Calcule son aire (utiliser π ≈ 3,14).",
                "params": {"r": range(2, 8)},
                "answer_type": "circle_area"
            }
        ],
        "4eme_3eme": [
            {
                "template": "Un trapèze a des bases de {b1} m et {b2} m, et une hauteur de {h} m. Calcule son aire.",
                "params": {"b1": range(3, 8), "b2": range(2, 7), "h": range(2, 6)},
                "answer_type": "trapeze_area"
            },
            {
                "template": "Calcule l'aire totale d'un parallélépipède rectangle de dimensions {l}cm × {w}cm × {h}cm.",
                "params": {"l": range(2, 6), "w": range(2, 6), "h": range(2, 5)},
                "answer_type": "surface_area"
            }
        ]
    },
    "fractions": {
        "cm1_cm2": [
            {
                "template": "Simplifie la fraction {num}/{denom}.",
                "params": {"num": [2, 3, 4, 6, 8, 10], "denom": [4, 6, 8, 12, 16, 20]},
                "answer_type": "simplify"
            },
            {
                "template": "Quelle fraction vaut {val} (sur 10) ?",
                "params": {"val": range(1, 10)},
                "answer_type": "fraction_notation"
            }
        ],
        "6eme_5eme": [
            {
                "template": "Calcule {n1}/{d1} + {n2}/{d2}.",
                "params": {"n1": range(1, 5), "d1": [4, 6, 8], "n2": range(1, 5), "d2": [4, 6, 8]},
                "answer_type": "fraction_add"
            },
            {
                "template": "Calcule {n1}/{d1} × {n2}/{d2}.",
                "params": {"n1": range(1, 6), "d1": [3, 4, 5], "n2": range(1, 6), "d2": [3, 4, 5]},
                "answer_type": "fraction_multiply"
            }
        ],
        "4eme_3eme": [
            {
                "template": "Résous l'équation : x/{d} = {n}/{d2}.",
                "params": {"d": [3, 4, 5], "n": range(2, 6), "d2": [6, 8, 10]},
                "answer_type": "fraction_equation"
            },
            {
                "template": "Calcule ({n1}/{d1} - {n2}/{d2}) × {n3}/{d3}.",
                "params": {"n1": range(3, 8), "d1": [4, 6], "n2": range(1, 4), "d2": [4, 6], "n3": range(2, 5), "d3": [3, 4, 5]},
                "answer_type": "fraction_complex"
            }
        ]
    }
}

# ========================
# CLASSE PRINCIPALE : IA PÉDAGOGIQUE
# ========================

class PedagogicalAI:
    """IA locale basée sur règles pédagogiques et templates"""
    
    def __init__(self):
        self.knowledge_base = KNOWLEDGE_BASE
        self.exercise_templates = EXERCISE_TEMPLATES
    
    def _normalize_level(self, level: Optional[str]) -> str:
        """Normaliser le niveau scolaire"""
        if not level:
            return "cm1_cm2"
        level_lower = level.lower().replace(" ", "_").replace("-", "_")
        for key in ["4eme_3eme", "6eme_5eme", "cm1_cm2"]:
            if key.replace("_", "").replace("eme", "e") in level_lower.replace("é", "e"):
                return key
        return "cm1_cm2"
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extraire mots-clés pertinents du texte"""
        text_lower = text.lower()
        found_keywords = []
        for topic, data in self.knowledge_base.items():
            for keyword in data["keywords"]:
                if keyword in text_lower:
                    found_keywords.append(topic)
                    break
        return found_keywords
    
    def _is_greeting(self, text: str) -> bool:
        """Détecter un message d'accueil"""
        greetings = ["bonjour", "hello", "hi", "salut", "bonsoir", "hey", "coucou"]
        text_lower = text.lower().strip()
        return any(g in text_lower for g in greetings)
    
    
    def _generate_personalized_greeting(self, utilisateur_data: Dict) -> str:
        """Générer un accueil personnalisé"""
        prenom = utilisateur_data.get("prenom", "élève")
        niveau = utilisateur_data.get("niveau_scolaire", "CM1-CM2")
        
        greetings = [
            f"Bonjour {prenom} 👋 ! Je suis ton tuteur IA. Sur quelle leçon de {niveau} veux-tu travailler aujourd'hui ?",
            f"Salut {prenom} ! 🎓 Que veux-tu apprendre sur la leçon d'aujourd'hui ?",
            f"Héllo {prenom} ! Je suis là pour t'aider avec tes maths. Qu'est-ce que tu as oublié ? 😊",
        ]
        return random.choice(greetings)
    
    def chat_tuteur(
        self,
        message: str,
        niveau: Optional[str] = None,
        matiere: str = "mathématiques",
        prenom: str = "élève",
        niveau_scolaire: str = "CM1-CM2",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Répondre comme tuteur pédagogique intelligent
        """
        if not message or len(message.strip()) < 2:
            return {
                "response": "Peux-tu poser une question précise ? Je suis là pour t'aider !",
                "exercises": [],
                "confidence": 0.5
            }
        
        message_clean = message.strip()
        message_lower = message_clean.lower()
        normalized_level = self._normalize_level(niveau or niveau_scolaire)
        
        # Cas 1 : Accueil SEULEMENT si c'est UNIQUEMENT un salut sans question
        # Vérifier si c'est un simple salut + question (ex: "Bonjour, la philosophie c'est quoi?")
        greetings = ["bonjour", "hello", "hi", "salut", "bonsoir", "hey", "coucou"]
        is_only_greeting = any(g in message_lower for g in greetings) and len(message_clean.split()) <= 2
        
        if is_only_greeting:
            return {
                "response": self._generate_personalized_greeting({
                    "prenom": prenom,
                    "niveau_scolaire": niveau_scolaire
                }),
                "exercises": [],
                "confidence": 0.95
            }
        
        # Cas 2 : Regarder d'abord si c'est une question sur un sujet connu (philosophie, histoire, etc.)
        subject_response = self._try_smart_response(message_lower, normalized_level)
        if subject_response:
            return subject_response
        
        # Cas 3 : Question sur un concept de la base de connaissances
        keywords = self._extract_keywords(message_lower)
        if keywords:
            topic = keywords[0]
            if topic in self.knowledge_base:
                topic_data = self.knowledge_base[topic]
                explanation = topic_data.get(normalized_level, {}).get(
                    "explanation",
                    topic_data.get("cm1_cm2", {}).get("explanation", "")
                )
                
                if not explanation:
                    explanation = f"Je connais le sujet '{topic}' mais pas encore sa description pour ton niveau. Peux-tu réessayer ?"
                
                return {
                    "response": explanation,
                    "exercises": [],
                    "confidence": 0.9,
                    "topic": topic
                }
        
        # Cas 4 : Fallback
        response_templates = {
            "cm1_cm2": (
                f"C'est une bonne question ! 🤔\n\n"
                "Je peux t'aider sur :\n"
                "• Les formules de volume et d'aire\n"
                "• Le théorème de Pythagore\n"
                "• Les fractions\n\n"
                "Quelle partie veux-tu explorer ?"
            ),
            "6eme_5eme": (
                f"Bonne question ! 📐\n\n"
                "Je peux t'aider sur :\n"
                "• Géométrie : volumes, aires, formules\n"
                "• Théorème de Pythagore\n"
                "• Proportionnalité et pourcentages\n\n"
                "Précise un peu plus pour une meilleure explication !"
            ),
            "4eme_3eme": (
                f"Intéressant ! 🔬\n\n"
                "Je maîtrise :\n"
                "• Calculs avancés en géométrie\n"
                "• Résolution d'équations\n"
                "• Analyse critique de problèmes complexes\n\n"
                "Développe ta question pour que je comprenne mieux."
            )
        }
        
        response = response_templates.get(normalized_level, response_templates["cm1_cm2"])
        return {
            "response": response,
            "exercises": [],
            "confidence": 0.6
        }
    
    def _try_smart_response(self, message_lower: str, level: str) -> Optional[Dict[str, Any]]:
        """Générer une réponse intelligente pour les sujets non-mathématiques"""
        smart_definitions = {
            "philosophie": {
                "cm1_cm2": (
                    "La philosophie t'aide à mieux RÉFLÉCHIR sur le monde autour de toi ! 🤔\n\n"
                    "À ton âge, on peut explorer :\n"
                    "• C'est quoi l'amitié ?\n"
                    "• Pourquoi on doit dire la vérité ?\n"
                    "• Comment être juste avec ses camarades ?\n\n"
                    "Poser de questions, c'est déjà faire de la philosophie !"
                ),
                "6eme_5eme": (
                    "La philosophie est l'art de poser des questions essentielles sur l'existence. 🧠\n\n"
                    "Ses branches principales :\n"
                    "• **Métaphysique** : Qu'est-ce qui existe vraiment ?\n"
                    "• **Éthique** : Comment vivre correctement ?\n"
                    "• **Logique** : Comment bien raisonner ?\n\n"
                    "À ton niveau, tu peux explorer des questions comme :\n"
                    "• Qu'est-ce que la justice ?\n"
                    "• Sommes-nous libres ?"
                ),
                "4eme_3eme": (
                    "La philosophie (philo = amour, sophia = sagesse) s'organise autour de grandes questions : 🎓\n\n"
                    "• **Métaphysique** : La nature de la réalité\n"
                    "• **Épistémologie** : Comment connaître ?\n"
                    "• **Éthique** : Qu'est-ce qu'une bonne vie ?\n"
                    "• **Politique** : Comment organiser la société ?\n\n"
                    "Courants : Stoïcisme, Platonisme, Existentialisme, Rationalisme, Empirisme."
                )
            },
            "histoire": {
                "cm1_cm2": (
                    "L'histoire t'apprend comment les gens vivaient AVANT ! 📖\n\n"
                    "Par exemple :\n"
                    "• Les Égyptiens ont construit les pyramides\n"
                    "• Les chevaliers habitaient dans les châteaux\n"
                    "• Les dinosaures ont vécu il y a très longtemps"
                ),
                "6eme_5eme": (
                    "L'histoire étudie les événements du passé et comment ils nous ont amenés au présent. 📚\n\n"
                    "Les grandes périodes :\n"
                    "• Préhistoire : Avant l'écriture\n"
                    "• Antiquité : Égypte, Rome, Grèce\n"
                    "• Moyen Âge : Féodalité, chevaliers\n"
                    "• Renaissance : Redécouverte de l'art"
                ),
                "4eme_3eme": (
                    "L'histoire est l'étude critique du passé basée sur des documents. 📜\n\n"
                    "Méthodes :\n"
                    "• Sources primaires : Documents originaux\n"
                    "• Sources secondaires : Analyses d'historiens\n"
                    "• Archéologie : Fouilles et artefacts"
                )
            },
            "géographie": {
                "cm1_cm2": (
                    "La géographie c'est l'étude de la Terre et des gens ! 🌍\n\n"
                    "On apprend :\n"
                    "• Où sont les continents, les océans\n"
                    "• Comment les gens vivent\n"
                    "• Les montagnes, les fleuves"
                ),
                "6eme_5eme": (
                    "La géographie étudie la Terre, les paysages et les populations. 🗺️\n\n"
                    "Elle répond à :\n"
                    "• Pourquoi y a-t-il des déserts et des forêts ?\n"
                    "• Comment les gens s'adaptent ?\n"
                    "• Qu'est-ce qui caractérise chaque région ?"
                ),
                "4eme_3eme": (
                    "La géographie combine étude physique (nature) et humaine (populations). 🌐\n\n"
                    "Domaines :\n"
                    "• Géographie physique : Relief, climat, biomes\n"
                    "• Géographie humaine : Cultures, économie, politique"
                )
            },
            "sciences": {
                "cm1_cm2": (
                    "Les sciences t'apprennent comment TOUT fonctionne ! 🔬\n\n"
                    "Par exemple :\n"
                    "• Pourquoi le ciel est bleu ?\n"
                    "• Comment les plantes poussent ?\n"
                    "• Qu'est-ce que l'énergie ?"
                ),
                "6eme_5eme": (
                    "Les sciences explorent la matière, l'énergie et la vie. 🧪\n\n"
                    "Domaines :\n"
                    "• Physique : Mouvement, forces, énergie\n"
                    "• Chimie : Matière et transformations\n"
                    "• Biologie : Êtres vivants et cycles"
                ),
                "4eme_3eme": (
                    "Les sciences étudient la nature à travers l'observation et l'expérimentation. 🔭\n\n"
                    "Domaines :\n"
                    "• Physique-Chimie : Lois de la nature\n"
                    "• SVT : Génétique, évolution, écosystèmes"
                )
            },
            "français": {
                "cm1_cm2": (
                    "Le français t'aide à mieux parler, lire et écrire ! 📝\n\n"
                    "On apprend :\n"
                    "• Construire les phrases\n"
                    "• Grammaire et orthographe\n"
                    "• Lire des histoires"
                ),
                "6eme_5eme": (
                    "Le français comprend plusieurs domaines : 📖\n\n"
                    "• Grammaire : Verbes, noms, adjectifs\n"
                    "• Orthographe : Bien écrire\n"
                    "• Littérature : Lire et analyser les textes"
                ),
                "4eme_3eme": (
                    "Le français est l'étude complète de la langue et de la littérature. 📚\n\n"
                    "Domaines :\n"
                    "• Linguistique : Structure de la langue\n"
                    "• Littérature : Mouvements, genres, auteurs"
                )
            }
        }
        
        # Rechercher le sujet dans le message
        for topic, definitions in smart_definitions.items():
            if topic in message_lower:
                response = definitions.get(level, definitions.get("6eme_5eme", definitions.get("cm1_cm2")))
                exercises = self._generate_exercises_for_topic(topic, level)
                return {
                    "response": response,
                    "exercises": exercises,
                    "confidence": 0.85,
                    "topic": topic
                }
        
        # Si le sujet n'est pas reconnu, générer une réponse générique intelligente
        return self._generate_generic_explanation(message_lower, level)
    
    def _generate_generic_explanation(self, message: str, level: str) -> Dict[str, Any]:
        """Générer une explication pour n'importe quel sujet"""
        # Extraire les mots clés principaux
        words = message.split()
        
        # Construire une réponse intelligente basée sur le niveau
        if level == "cm1_cm2":
            response = (
                f"C'est une très bonne question sur {words[0] if words else 'ce sujet'} ! 🎯\n\n"
                "Je pense que tu cherches à comprendre **comment cela fonctionne**.\n\n"
                "Voici ce qui est important :\n"
                "• Observer et poser des questions\n"
                "• Chercher des exemples concrets\n"
                "• Essayer de trouver des réponses par l'expérience\n\n"
                "Continue à t'intéresser à ce sujet - c'est excellent pour apprendre ! 🌟"
            )
        elif level == "6eme_5eme":
            response = (
                f"C'est une question pertinente sur **{words[0] if words else 'ce domaine'}** ! 📊\n\n"
                "Pour mieux comprendre ce sujet :\n"
                "• **Définition** : Cherche d'abord à bien définir les termes\n"
                "• **Concepts clés** : Identifie les idées principales\n"
                "• **Contexte** : Comprends comment cela se rapporte à d'autres domaines\n"
                "• **Applications** : Vois les usages pratiques\n\n"
                "Continue à creuser - tu développes une excellente curiosité intellectuelle ! 🧠"
            )
        else:  # 4eme_3eme
            response = (
                f"Excellente interrogation sur **{words[0] if words else 'ce sujet complexe'}** ! 🎓\n\n"
                "Pour une analyse approfondie :\n"
                "• **Analyse critique** : Examine les différentes perspectives\n"
                "• **Fondamentaux** : Comprends les principes sous-jacents\n"
                "• **Nuances** : Identifie les cas particuliers et exceptions\n"
                "• **Synthèse** : Intègre les informations pour créer ta propre compréhension\n\n"
                "Ce type de réflexion critique est exactement ce qu'attend le programme ! ✨"
            )
        
        exercises = self._generate_generic_exercises(level)
        
        return {
            "response": response,
            "exercises": exercises,
            "confidence": 0.7,
            "type": "generic"
        }
    
    def _generate_exercises_for_topic(self, topic: str, level: str) -> List[Dict]:
        """Générer des exercices pour un sujet spécifique"""
        exercises_map = {
            "philosophie": {
                "cm1_cm2": [
                    {
                        "question": "Pense à tes amis : qu'est-ce qui rend l'amitié importante pour toi ?",
                        "type": "réflexion"
                    },
                    {
                        "question": "Est-il toujours bien de dire la vérité ? Donne un exemple.",
                        "type": "discussion"
                    }
                ],
                "6eme_5eme": [
                    {
                        "question": "Qu'est-ce qu'être juste ? Donne 3 exemples de situations justes.",
                        "type": "analyse"
                    },
                    {
                        "question": "Sommes-nous vraiment libres de choisir ? Explique.",
                        "type": "réflexion"
                    }
                ],
                "4eme_3eme": [
                    {
                        "question": "Analyse : 'Existe-t-il une vérité absolue ou tout est-il relatif ?'",
                        "type": "argumentation"
                    },
                    {
                        "question": "Débat : La liberté humaine est-elle compatible avec la responsabilité ?",
                        "type": "critique"
                    }
                ]
            },
            "histoire": {
                "cm1_cm2": [
                    {
                        "question": "Nomme 3 différences entre la vie aujourd'hui et il y a 100 ans.",
                        "type": "comparaison"
                    },
                    {
                        "question": "Pourquoi les gens construisaient-ils des châteaux au Moyen Âge ?",
                        "type": "compréhension"
                    }
                ],
                "6eme_5eme": [
                    {
                        "question": "Classe ces civilisations par ordre chronologique : Rome, Égypte, Moyen Âge, Renaissance.",
                        "type": "chronologie"
                    },
                    {
                        "question": "Qu'est-ce qui a causé le passage du Moyen Âge à la Renaissance ?",
                        "type": "causalité"
                    }
                ],
                "4eme_3eme": [
                    {
                        "question": "Compare les causes de la Révolution française avec celles de la Révolution russe.",
                        "type": "analyse"
                    },
                    {
                        "question": "Évalue : 'La Révolution française a-t-elle vraiment changé la société ?'",
                        "type": "critique"
                    }
                ]
            }
        }
        
        if topic in exercises_map:
            return exercises_map[topic].get(level, exercises_map[topic].get("6eme_5eme", []))
        
        return self._generate_generic_exercises(level)
    
    def _generate_generic_exercises(self, level: str) -> List[Dict]:
        """Générer des exercices génériques adaptés au niveau"""
        if level == "cm1_cm2":
            return [
                {
                    "question": "Explique avec tes propres mots ce que tu as compris.",
                    "type": "explication"
                },
                {
                    "question": "Donne un exemple concret de ce sujet.",
                    "type": "application"
                }
            ]
        elif level == "6eme_5eme":
            return [
                {
                    "question": "Résume les points clés en 3-4 phrases.",
                    "type": "synthèse"
                },
                {
                    "question": "Quel est le lien entre ce sujet et quelque chose que tu connais déjà ?",
                    "type": "connexion"
                },
                {
                    "question": "Imagine une situation réelle où cela s'applique.",
                    "type": "application"
                }
            ]
        else:  # 4eme_3eme
            return [
                {
                    "question": "Analyse les causes et conséquences de ce concept.",
                    "type": "analyse"
                },
                {
                    "question": "Critique : Quels seraient les arguments pour ET contre cette idée ?",
                    "type": "critique"
                },
                {
                    "question": "Comment ce sujet s'intègre-t-il avec d'autres domaines ?",
                    "type": "synthèse"
                }
            ]
    
    def generate_exercises(
        self,
        count: int = 2,
        niveau: Optional[str] = None,
        topic: Optional[str] = None,
        matiere: str = "mathématiques",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Générer des exercices pédagogiques
        
        Args:
            count: Nombre d'exercices (min 1)
            niveau: Niveau scolaire
            topic: Sujet spécifique (ex: "volume", "fractions")
        
        Returns:
            Dict avec liste d'exercices en JSON
        """
        count = max(1, min(count, 5))  # Entre 1 et 5
        normalized_level = self._normalize_level(niveau)
        
        exercises = []
        
        # Sélectionner les topics
        available_topics = list(self.exercise_templates.keys())
        if topic and topic in self.exercise_templates:
            selected_topics = [topic]
        else:
            selected_topics = random.sample(available_topics, min(len(available_topics), count))
        
        # Générer les exercices
        for _ in range(count):
            selected_topic = random.choice(selected_topics)
            if selected_topic not in self.exercise_templates:
                continue
            
            topic_templates = self.exercise_templates[selected_topic].get(normalized_level, [])
            if not topic_templates:
                topic_templates = self.exercise_templates[selected_topic].get("cm1_cm2", [])
            
            if not topic_templates:
                continue
            
            template_obj = random.choice(topic_templates)
            
            # Générer les paramètres
            params = {}
            for key, value in template_obj.get("params", {}).items():
                if isinstance(value, range):
                    params[key] = random.choice(list(value))
                else:
                    params[key] = random.choice(list(value))
            
            # Créer la question
            try:
                question = template_obj["template"].format(**params)
            except KeyError:
                question = template_obj["template"]
            
            exercise = {
                "id": len(exercises) + 1,
                "question": question,
                "topic": selected_topic,
                "level": normalized_level,
                "type": template_obj.get("answer_type", "calculation")
            }
            
            exercises.append(exercise)
        
        return {
            "exercises": exercises,
            "count": len(exercises),
            "timestamp": datetime.now().isoformat(),
            "success": True
        }

# ========================
# SINGLETON
# ========================

_pedagogical_ai = None

def get_pedagogical_ai() -> PedagogicalAI:
    """Obtenir l'instance unique de l'IA pédagogique"""
    global _pedagogical_ai
    if _pedagogical_ai is None:
        _pedagogical_ai = PedagogicalAI()
    return _pedagogical_ai

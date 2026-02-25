"""
Curriculum complet par niveau (CP1 → Terminale).
Création automatique à la demande : matières, leçons, exercices.
Aucune dépendance à un script manuel.
"""
from core.models import NiveauScolaire, Matiere, Lecon, Exercice

NIVEAUX = [
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
NIVEAUX_MAP = {c[0]: (c[1], c[2], c[3]) for c in NIVEAUX}

# Matières par niveau (programme francophone)
MATIERES_PAR_NIVEAU = {
    'cp1': [
        ('mathematiques', 'Mathématiques', '#3B82F6', '🔢'),
        ('francais', 'Français', '#10B981', '📖'),
        ('lecture', 'Lecture', '#8B5CF6', '📚'),
        ('ecriture', 'Écriture', '#F59E0B', '✏️'),
        ('education_civique', 'Éducation civique', '#EF4444', '🏛️'),
    ],
    'cp2': [
        ('mathematiques', 'Mathématiques', '#3B82F6', '🔢'),
        ('francais', 'Français', '#10B981', '📖'),
        ('lecture', 'Lecture', '#8B5CF6', '📚'),
        ('ecriture', 'Écriture', '#F59E0B', '✏️'),
        ('education_civique', 'Éducation civique', '#EF4444', '🏛️'),
        ('sciences', 'Sciences', '#06B6D4', '🔬'),
    ],
    'ce1': [
        ('mathematiques', 'Mathématiques', '#3B82F6', '🔢'),
        ('francais', 'Français', '#10B981', '📖'),
        ('lecture', 'Lecture', '#8B5CF6', '📚'),
        ('ecriture', 'Écriture', '#F59E0B', '✏️'),
        ('education_civique', 'Éducation civique', '#EF4444', '🏛️'),
        ('sciences', 'Sciences', '#06B6D4', '🔬'),
        ('histoire_geo', 'Histoire-Géographie', '#84CC16', '🗺️'),
    ],
    'ce2': [
        ('mathematiques', 'Mathématiques', '#3B82F6', '🔢'),
        ('francais', 'Français', '#10B981', '📖'),
        ('lecture', 'Lecture', '#8B5CF6', '📚'),
        ('ecriture', 'Écriture', '#F59E0B', '✏️'),
        ('sciences', 'Sciences', '#06B6D4', '🔬'),
        ('histoire_geo', 'Histoire-Géographie', '#84CC16', '🗺️'),
        ('anglais', 'Anglais', '#EC4899', '🌍'),
    ],
    'cm1': [
        ('mathematiques', 'Mathématiques', '#3B82F6', '🔢'),
        ('francais', 'Français', '#10B981', '📖'),
        ('sciences', 'Sciences', '#06B6D4', '🔬'),
        ('histoire_geo', 'Histoire-Géographie', '#84CC16', '🗺️'),
        ('anglais', 'Anglais', '#EC4899', '🌍'),
        ('education_civique', 'Éducation civique', '#EF4444', '🏛️'),
    ],
    'cm2': [
        ('mathematiques', 'Mathématiques', '#3B82F6', '🔢'),
        ('francais', 'Français', '#10B981', '📖'),
        ('sciences', 'Sciences', '#06B6D4', '🔬'),
        ('histoire_geo', 'Histoire-Géographie', '#84CC16', '🗺️'),
        ('anglais', 'Anglais', '#EC4899', '🌍'),
        ('education_civique', 'Éducation civique', '#EF4444', '🏛️'),
    ],
    '6eme': [
        ('mathematiques', 'Mathématiques', '#3B82F6', '🔢'),
        ('francais', 'Français', '#10B981', '📖'),
        ('sciences', 'Sciences', '#06B6D4', '🔬'),
        ('histoire_geo', 'Histoire-Géographie', '#84CC16', '🗺️'),
        ('anglais', 'Anglais', '#EC4899', '🌍'),
        ('sciences_vie', 'SVT', '#14B8A6', '🧬'),
        ('physique_chimie', 'Physique-Chimie', '#F97316', '⚗️'),
    ],
    '5eme': [
        ('mathematiques', 'Mathématiques', '#3B82F6', '🔢'),
        ('francais', 'Français', '#10B981', '📖'),
        ('sciences', 'Sciences', '#06B6D4', '🔬'),
        ('histoire_geo', 'Histoire-Géographie', '#84CC16', '🗺️'),
        ('anglais', 'Anglais', '#EC4899', '🌍'),
        ('sciences_vie', 'SVT', '#14B8A6', '🧬'),
        ('physique_chimie', 'Physique-Chimie', '#F97316', '⚗️'),
    ],
    '4eme': [
        ('mathematiques', 'Mathématiques', '#3B82F6', '🔢'),
        ('francais', 'Français', '#10B981', '📖'),
        ('sciences', 'Sciences', '#06B6D4', '🔬'),
        ('histoire_geo', 'Histoire-Géographie', '#84CC16', '🗺️'),
        ('anglais', 'Anglais', '#EC4899', '🌍'),
        ('sciences_vie', 'SVT', '#14B8A6', '🧬'),
        ('physique_chimie', 'Physique-Chimie', '#F97316', '⚗️'),
    ],
    '3eme': [
        ('mathematiques', 'Mathématiques', '#3B82F6', '🔢'),
        ('francais', 'Français', '#10B981', '📖'),
        ('sciences', 'Sciences', '#06B6D4', '🔬'),
        ('histoire_geo', 'Histoire-Géographie', '#84CC16', '🗺️'),
        ('anglais', 'Anglais', '#EC4899', '🌍'),
        ('sciences_vie', 'SVT', '#14B8A6', '🧬'),
        ('physique_chimie', 'Physique-Chimie', '#F97316', '⚗️'),
    ],
    'seconde': [
        ('mathematiques', 'Mathématiques', '#3B82F6', '🔢'),
        ('francais', 'Français', '#10B981', '📖'),
        ('sciences_vie', 'SVT', '#14B8A6', '🧬'),
        ('physique_chimie', 'Physique-Chimie', '#F97316', '⚗️'),
        ('histoire_geo', 'Histoire-Géographie', '#84CC16', '🗺️'),
        ('anglais', 'Anglais', '#EC4899', '🌍'),
    ],
    '1ere': [
        ('mathematiques', 'Mathématiques', '#3B82F6', '🔢'),
        ('francais', 'Français', '#10B981', '📖'),
        ('sciences_vie', 'SVT', '#14B8A6', '🧬'),
        ('physique_chimie', 'Physique-Chimie', '#F97316', '⚗️'),
        ('histoire_geo', 'Histoire-Géographie', '#84CC16', '🗺️'),
        ('anglais', 'Anglais', '#EC4899', '🌍'),
        ('ses', 'SES', '#A855F7', '📊'),
    ],
    'terminale': [
        ('mathematiques', 'Mathématiques', '#3B82F6', '🔢'),
        ('francais', 'Français', '#10B981', '📖'),
        ('sciences_vie', 'SVT', '#14B8A6', '🧬'),
        ('physique', 'Physique', '#F97316', '⚛️'),
        ('chimie', 'Chimie', '#22C55E', '⚗️'),
        ('histoire_geo', 'Histoire-Géographie', '#84CC16', '🗺️'),
        ('anglais', 'Anglais', '#EC4899', '🌍'),
        ('philosophie', 'Philosophie', '#6366F1', '🤔'),
        ('ses', 'SES', '#A855F7', '📊'),
    ],
}

# Niveau global pour le champ legacy
def _niveau_global(code):
    if code in ('cp1', 'cp2', 'ce1', 'ce2', 'cm1', 'cm2'):
        return 'débutant'
    if code in ('6eme', '5eme', '4eme', '3eme'):
        return 'intermédiaire'
    return 'avancé'


def _lecons_et_exercices_par_matiere_niveau(nom_matiere, code_niveau, libelle_niveau):
    """Retourne une liste (titre, contenu, [(question, reponse), ...]) par matière et niveau."""
    # Contenu type par matière (exemples pédagogiques réels)
    tpl = (nom_matiere, code_niveau, libelle_niveau)
    if nom_matiere == 'mathematiques':
        return [
            ('Les nombres jusqu\'à 10', 'On apprend à compter de 0 à 10. Chaque nombre a une écriture en chiffres.', [('Combien font 2 + 3 ?', '5'), ('Quel nombre vient après 7 ?', '8')]) if code_niveau in ('cp1', 'cp2') else
            ('Addition et soustraction', 'L\'addition permet d\'ajouter des quantités. La soustraction permet d\'enlever.', [('Combien font 5 + 4 ?', '9'), ('Combien font 10 - 3 ?', '7')]) if code_niveau in ('ce1', 'ce2') else
            ('Les tables de multiplication', 'La table de 2 : 2×1=2, 2×2=4, 2×3=6...', [('Combien font 6 × 7 ?', '42'), ('Combien font 8 × 9 ?', '72')]) if code_niveau in ('cm1', 'cm2', '6eme', '5eme') else
            ('Équations du premier degré', 'Résoudre ax + b = c : isoler x en passant les termes.', [('Résoudre : x + 5 = 12. Que vaut x ?', '7'), ('Résoudre : 2x = 18. Que vaut x ?', '9')]) if code_niveau in ('4eme', '3eme', 'seconde', '1ere', 'terminale') else
            ('Révisions calcul', 'Réviser les opérations de base.', [('Combien font 15 + 27 ?', '42'), ('Combien font 100 - 38 ?', '62')]),
            ('Géométrie : les formes', 'Le carré a 4 côtés égaux. Le triangle a 3 côtés. Le cercle est rond.', [('Combien de côtés a un triangle ?', '3'), ('Combien de côtés a un carré ?', '4')]) if code_niveau in ('cp1', 'cp2', 'ce1') else
            ('Fractions et proportion', 'Une fraction représente une partie. 1/2 = la moitié.', [('Quelle est la moitié de 10 ?', '5'), ('Quel est 50 % de 20 ?', '10')]) if code_niveau in ('cm1', 'cm2', '6eme') else
            ('Géométrie dans l\'espace', 'Le cube a 6 faces carrées. Le pavé a des faces rectangulaires.', [('Combien de faces a un cube ?', '6'), ('Quel est le périmètre d\'un carré de côté 5 cm ?', '20')]) if code_niveau in ('5eme', '4eme') else
            ('Fonctions et représentations', 'Une fonction associe à chaque x une image f(x).', [('Si f(x)=2x+1, que vaut f(3) ?', '7'), ('Que vaut 3² ?', '9')]) if code_niveau in ('seconde', '1ere', 'terminale') else
            ('Révisions géométrie', 'Formes, périmètres et aires.', [('Combien font 3 × 4 ?', '12'), ('Combien de degrés dans un angle droit ?', '90')]),
        ]
    if nom_matiere == 'francais':
        return [
            ('Les lettres de l\'alphabet', 'L\'alphabet a 26 lettres : A, B, C... On les prononce pour former des mots.', [('Combien y a-t-il de lettres dans l\'alphabet français ?', '26'), ('Quelle est la première lettre ?', 'A')]) if code_niveau in ('cp1', 'cp2') else
            ('Les syllabes', 'Un mot est fait de syllabes. Exemple : ma-man a deux syllabes.', [('Combien de syllabes dans "école" ?', '2'), ('Écris "papa" avec un P.', 'papa')]) if code_niveau in ('ce1', 'ce2') else
            ('La phrase simple', 'Une phrase commence par une majuscule et finit par un point.', [('Quel signe met-on à la fin d\'une phrase ?', 'un point'), ('Quelle lettre met-on en majuscule au début ?', 'la première')]) if code_niveau in ('cm1', 'cm2') else
            ('Grammaire : le verbe', 'Le verbe indique l\'action. Il se conjugue avec le sujet.', [('Dans "Il mange", quel est le verbe ?', 'mange'), ('Conjuguer "chanter" au présent avec "nous".', 'nous chantons')]) if code_niveau in ('6eme', '5eme', '4eme') else
            ('Lecture analytique', 'Analyser un texte : thème, personnages, procédés.', [('Qu\'est-ce qu\'un narrateur ?', 'celui qui raconte l\'histoire'), ('Qu\'est-ce qu\'une métaphore ?', 'une comparaison sans mot de comparaison')]) if code_niveau in ('3eme', 'seconde', '1ere', 'terminale') else
            ('Orthographe et vocabulaire', 'Bien écrire et enrichir son vocabulaire.', [('Écris "demain" correctement.', 'demain'), ('Quel est le féminin de "acteur" ?', 'actrice')]),
        ]
    if nom_matiere == 'lecture':
        return [
            ('Reconnaître les mots', 'On associe les lettres aux sons pour lire des mots simples.', [('Quel son fait la lettre A ?', 'a'), ('Lis le mot : "sac".', 'sac')]),
            ('Comprendre une phrase', 'Lire une phrase et comprendre qui fait quoi.', [('Dans "Le chat mange", qui mange ?', 'le chat'), ('Quel mot indique une action ?', 'mange')]),
            ('Petits textes', 'Lire un court texte et répondre à des questions.', [('Combien de personnages dans l\'histoire ?', '2'), ('Où se passe l\'histoire ?', 'à l\'école')]),
        ]
    if nom_matiere == 'ecriture':
        return [
            ('Tracer les lettres', 'On écrit les lettres en majuscules et en minuscules.', [('Écris la lettre A en majuscule.', 'A'), ('Combien de lettres dans "lit" ?', '3')]),
            ('Copier des mots', 'Copier sans faute des mots simples.', [('Écris le mot "maman".', 'maman'), ('Écris le mot "papa".', 'papa')]),
            ('Écrire une phrase', 'Construire une phrase avec un sujet et un verbe.', [('Écris une phrase avec le mot "école".', 'Je vais à l\'école.'), ('Quel signe termine une phrase ?', 'un point')]),
        ]
    if nom_matiere == 'education_civique':
        return [
            ('Les règles de la classe', 'En classe on lève la main pour parler, on écoute les autres.', [('Que fait-on pour parler en classe ?', 'on lève la main'), ('Pourquoi faut-il écouter ?', 'pour respecter les autres')]),
            ('Les symboles de la République', 'Le drapeau est bleu, blanc, rouge. La devise est Liberté, Égalité, Fraternité.', [('Quelles sont les couleurs du drapeau français ?', 'bleu blanc rouge'), ('Quelle est la devise de la République ?', 'Liberté Égalité Fraternité')]),
            ('Vivre ensemble', 'Le respect, le partage et l\'entraide à l\'école.', [('Que signifie "vivre ensemble" ?', 'respecter et partager'), ('Comment aider un camarade ?', 'en partageant et en expliquant')]),
        ]
    if nom_matiere in ('sciences', 'sciences_vie'):
        return [
            ('Le monde vivant', 'Les animaux et les plantes sont des êtres vivants.', [('Qui a besoin d\'eau pour vivre ?', 'les plantes et les animaux'), ('Cite un être vivant.', 'un arbre')]) if code_niveau in ('cp2', 'ce1', 'ce2') else
            ('Le corps humain', 'Le corps a des organes : le cœur, les poumons, le cerveau.', [('Quel organe fait battre le sang ?', 'le cœur'), ('Où va l\'air quand on respire ?', 'dans les poumons')]) if code_niveau in ('cm1', 'cm2', '6eme') else
            ('La cellule', 'Tous les êtres vivants sont faits de cellules.', [('Qu\'est-ce qu\'une cellule ?', 'l\'unité du vivant'), ('Quel organite fait la photosynthèse ?', 'chloroplaste')]) if code_niveau in ('5eme', '4eme', '3eme') else
            ('Génétique et évolution', 'L\'ADN porte l\'information génétique. Les espèces évoluent.', [('Où se trouve l\'ADN ?', 'dans le noyau'), ('Qu\'est-ce qu\'un gène ?', 'un segment d\'ADN')]) if code_niveau in ('seconde', '1ere', 'terminale') else
            ('Sciences et expériences', 'Observer et faire des expériences pour comprendre.', [('Qu\'est-ce qu\'une hypothèse ?', 'une idée à vérifier'), ('Pourquoi répète-t-on une expérience ?', 'pour vérifier')]),
        ]
    if nom_matiere == 'histoire_geo':
        return [
            ('Le temps qui passe', 'Hier, aujourd\'hui, demain. Les saisons.', [('Combien y a-t-il de saisons ?', '4'), ('Quelle saison vient après l\'été ?', 'l\'automne')]) if code_niveau in ('ce1', 'ce2') else
            ('La France', 'La France a une capitale, des régions, des fleuves.', [('Quelle est la capitale de la France ?', 'Paris'), ('Cite un fleuve français.', 'la Seine')]) if code_niveau in ('cm1', 'cm2', '6eme') else
            ('L\'Antiquité', 'Les Romains, la Gaule, Jules César.', [('Qui a conquis la Gaule ?', 'Jules César'), ('Quelle était la capitale de l\'Empire romain ?', 'Rome')]) if code_niveau in ('6eme', '5eme') else
            ('Les Révolutions', '1789 : la Révolution française. Liberté, égalité.', [('En quelle année a eu lieu la Révolution française ?', '1789'), ('Quelle devise de la République ?', 'Liberté Égalité Fraternité')]) if code_niveau in ('4eme', '3eme', 'seconde') else
            ('Géographie humaine', 'Population, villes, développement.', [('Qu\'est-ce qu\'une métropole ?', 'une grande ville'), ('Qu\'est-ce que la densité ?', 'habitants au km²')]) if code_niveau in ('1ere', 'terminale') else
            ('Histoire et géographie', 'Repères dans le temps et l\'espace.', [('Cite un continent.', 'l\'Europe'), ('Quel océan borde la France ?', 'l\'Atlantique')]),
        ]
    if nom_matiere == 'anglais':
        return [
            ('Hello and goodbye', 'Say hello: Hello! Goodbye: Bye!', [('How do you say "bonjour" in English?', 'hello'), ('How do you say "au revoir" in English?', 'goodbye')]),
            ('Numbers 1-20', 'One, two, three, four, five...', [('How do you say "cinq" in English?', 'five'), ('How do you say "dix" in English?', 'ten')]),
            ('Colors', 'Red, blue, green, yellow, black, white.', [('How do you say "rouge" in English?', 'red'), ('What color is the sky?', 'blue')]),
        ]
    if nom_matiere in ('physique_chimie', 'physique', 'chimie'):
        return [
            ('Les états de la matière', 'Solide, liquide, gaz. L\'eau peut être glace ou vapeur.', [('Quels sont les trois états de la matière ?', 'solide liquide gaz'), ('À 0°C l\'eau liquide devient quoi ?', 'glace')]) if code_niveau in ('6eme', '5eme') else
            ('Forces et mouvements', 'Une force peut mettre en mouvement. La gravité attire.', [('Qui a découvert la gravité ?', 'Newton'), ('Qu\'est-ce que la masse ?', 'quantité de matière')]) if code_niveau in ('4eme', '3eme', 'seconde') else
            ('Chimie : atomes et molécules', 'La matière est faite d\'atomes. Les molécules sont des assemblages.', [('Quel est le symbole de l\'eau ?', 'H2O'), ('Qu\'est-ce qu\'un atome ?', 'plus petite partie de la matière')]) if code_niveau in ('1ere', 'terminale') else
            ('Électricité et énergie', 'Le courant électrique, les circuits.', [('Qu\'est-ce qu\'un circuit fermé ?', 'un circuit où le courant passe'), ('Quelle unité pour l\'intensité ?', 'ampère')]),
        ]
    if nom_matiere == 'philosophie':
        return [
            ('La philosophie : qu\'est-ce que penser ?', 'La philosophie questionne le monde et nous-mêmes.', [('Qu\'est-ce que la philosophie ?', 'réflexion sur le monde et l\'homme'), ('Cite un philosophe grec.', 'Socrate')]),
            ('Liberté et responsabilité', 'Être libre, c\'est pouvoir choisir. Avec la liberté vient la responsabilité.', [('La liberté s\'arrête où ?', 'là où commence celle des autres'), ('Qu\'est-ce que la responsabilité ?', 'répondre de ses actes')]),
            ('La conscience', 'Conscience de soi, conscience du monde.', [('Qu\'est-ce que la conscience ?', 'capacité à se connaître et connaître le monde'), ('Que signifie "Cogito ergo sum" ?', 'je pense donc je suis')]),
        ]
    if nom_matiere == 'ses':
        return [
            ('Les acteurs de l\'économie', 'Ménages, entreprises, État. Marché.', [('Qui sont les acteurs économiques ?', 'ménages entreprises État'), ('Qu\'est-ce qu\'un marché ?', 'lieu de rencontre offre et demande')]),
            ('Croissance et développement', 'PIB, indicateurs de développement.', [('Qu\'est-ce que le PIB ?', 'richesse produite'), ('Qu\'est-ce que le développement durable ?', 'développement qui préserve l\'avenir')]),
        ]
    # Défaut : une leçon générique par matière
    return [
        (f'Découverte {libelle_niveau}', f'Contenu adapté au niveau {libelle_niveau} pour cette matière.', [('Première question', 'réponse'), ('Deuxième question', 'réponse')]),
        (f'Approfondissement {libelle_niveau}', f'On approfondit les notions vues précédemment.', [('Question 1', 'réponse 1'), ('Question 2', 'réponse 2')]),
    ]


def ensure_curriculum_complet_pour_niveau(code_niveau: str) -> None:
    """Crée ou complète tout le curriculum pour un niveau : NiveauScolaire, matières, leçons, exercices."""
    if not code_niveau or code_niveau not in NIVEAUX_MAP:
        return
    libelle, ordre, cycle = NIVEAUX_MAP[code_niveau]
    niveau, _ = NiveauScolaire.objects.get_or_create(
        code=code_niveau,
        defaults={'libelle': libelle, 'ordre': ordre, 'cycle': cycle}
    )
    ng = _niveau_global(code_niveau)
    matieres_config = MATIERES_PAR_NIVEAU.get(code_niveau, MATIERES_PAR_NIVEAU['ce1'])
    for nom, desc, couleur, icone in matieres_config:
        matiere, _ = Matiere.objects.get_or_create(
            nom=nom,
            defaults={'description': desc, 'couleur_hex': couleur, 'icone': icone}
        )
        lecons_data = _lecons_et_exercices_par_matiere_niveau(nom, code_niveau, libelle)
        for ordre_lec, (titre, contenu, exercices_list) in enumerate(lecons_data):
            lecon, created = Lecon.objects.get_or_create(
                matiere=matiere,
                niveau=niveau,
                titre=titre,
                defaults={
                    'contenu_principal': contenu,
                    'niveau_global': ng,
                    'ordre': ordre_lec,
                }
            )
            if created or not lecon.exercices.exists():
                for ordre_ex, (question, reponse) in enumerate(exercices_list):
                    Exercice.objects.get_or_create(
                        lecon=lecon,
                        matiere=matiere,
                        question=question,
                        defaults={
                            'reponse_correcte': reponse,
                            'niveau': ng,
                            'ordre': ordre_ex,
                        }
                    )


def ensure_contenu_minimal_pour_niveau(code_niveau: str) -> None:
    """Point d'entrée unique : garantit tout le curriculum pour le niveau (appelé par matieres_du_niveau_eleve)."""
    ensure_curriculum_complet_pour_niveau(code_niveau)

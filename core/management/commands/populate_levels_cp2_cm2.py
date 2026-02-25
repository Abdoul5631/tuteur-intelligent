"""
Populate CP2, CE1, CE2, CM1, CM2 curriculum (lessons + 2 exercises each)
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Matiere, Lecon, Exercice


class Command(BaseCommand):
    help = 'Populate CP2 → CM2 curriculum (Français, Mathématiques, Sciences, Histoire-Géographie, Éducation civique)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🚀 Starting population for CP2 → CM2..."))

        with transaction.atomic():
            # Ensure matieres exist (use choice keys)
            matieres_keys = {
                'francais': 'francais',
                'mathematiques': 'mathematiques',
                'sciences': 'sciences',
                'histoire_geo': 'histoire_geo',
                'education_civique': 'education_civique',
            }
            matieres = {}
            for key in matieres_keys:
                try:
                    m = Matiere.objects.get(nom=matieres_keys[key])
                except Matiere.DoesNotExist:
                    m = Matiere.objects.create(nom=matieres_keys[key], description=f"Matière {matieres_keys[key]}")
                    self.stdout.write(self.style.WARNING(f"Created missing Matiere: {matieres_keys[key]}"))
                matieres[key] = m

            # Curriculum definitions based exactly on provided text for CP2 and CE1;
            # CE2-CM2 follow the same structure with concise content based on given topics.
            curriculum = {
                'cp2': {
                    'francais': [
                        {
                            'titre': 'Lecture de mots simples',
                            'contenu': 'On lit des mots formés de syllabes simples.',
                            'exercices': [
                                {'question': 'Lis : ba – ta – ma', 'type': 'redaction', 'reponse': 'Lecture orale'},
                                {'question': 'Entoure les mots : chat – a – papa', 'type': 'choix_multiple', 'reponse': 'chat, papa', 'options': ['chat','a','papa']},
                            ]
                        },
                        {
                            'titre': 'Phrase simple',
                            'contenu': 'Une phrase commence par une majuscule et finit par un point.',
                            'exercices': [
                                {'question': 'Mets un point : Je vais à l’école', 'type': 'reponse_courte', 'reponse': 'Je vais à l’école.'},
                                {'question': 'Entoure la majuscule', 'type': 'choix_multiple', 'reponse': 'J (Je)', 'options': ['J','v','l']},
                            ]
                        }
                    ],
                    'mathematiques': [
                        {
                            'titre': 'Nombres de 1 à 100',
                            'contenu': 'On compte jusqu’à 100.',
                            'exercices': [
                                {'question': 'Complète : 45, 46, …', 'type': 'reponse_courte', 'reponse': '47'},
                                {'question': 'Écris en chiffres : soixante', 'type': 'reponse_courte', 'reponse': '60'},
                            ]
                        },
                        {
                            'titre': 'Addition simple',
                            'contenu': "Additionner, c'est ajouter.",
                            'exercices': [
                                {'question': '6 + 3 = …', 'type': 'calcul', 'reponse': '9'},
                                {'question': '10 + 5 = …', 'type': 'calcul', 'reponse': '15'},
                            ]
                        }
                    ],
                    'sciences': [
                        {
                            'titre': 'Les animaux',
                            'contenu': 'Les animaux peuvent être domestiques ou sauvages.',
                            'exercices': [
                                {'question': 'Cite un animal domestique', 'type': 'reponse_courte', 'reponse': 'chien, chat, poule, etc.'},
                                {'question': 'Cite un animal sauvage', 'type': 'reponse_courte', 'reponse': 'lion, éléphant, tigre, etc.'},
                            ]
                        },
                        {
                            'titre': 'Les plantes',
                            'contenu': 'Les plantes ont des racines, une tige et des feuilles.',
                            'exercices': [
                                {'question': 'Cite une partie de la plante', 'type': 'reponse_courte', 'reponse': 'racine, tige, feuille'},
                                {'question': "À quoi sert la racine ?", 'type': 'reponse_courte', 'reponse': 'Absorber l\'eau et les nutriments'},
                            ]
                        }
                    ],
                    'histoire_geo': [
                        {
                            'titre': 'L\'école',
                            'contenu': "L'école est un lieu d'apprentissage.",
                            'exercices': [
                                {'question': 'Que fait-on à l\'école ?', 'type': 'reponse_courte', 'reponse': 'On apprend, on lit, on écrit.'},
                                {'question': 'Cite un matériel scolaire', 'type': 'reponse_courte', 'reponse': 'crayon, cahier, règle'},
                            ]
                        },
                        {
                            'titre': 'Le village',
                            'contenu': 'Le village est le lieu où on vit.',
                            'exercices': [
                                {'question': 'Cite un lieu du village', 'type': 'reponse_courte', 'reponse': 'église, marché, école'},
                                {'question': 'Qui dirige le village ?', 'type': 'reponse_courte', 'reponse': 'Le chef du village / le maire'},
                            ]
                        }
                    ],
                    'education_civique': [
                        {
                            'titre': 'Le respect',
                            'contenu': 'Respecter les autres est important.',
                            'exercices': [
                                {'question': 'Donne un exemple de respect', 'type': 'reponse_courte', 'reponse': 'écouter, partager, dire merci'},
                                {'question': 'Faut-il respecter le maître ?', 'type': 'vrai_faux', 'reponse': 'Oui'},
                            ]
                        },
                        {
                            'titre': 'L\'obéissance',
                            'contenu': 'Obéir, c\'est suivre les règles.',
                            'exercices': [
                                {'question': 'À qui doit-on obéir ?', 'type': 'reponse_courte', 'reponse': 'Aux adultes responsables, aux enseignants'},
                                {'question': 'Pourquoi obéir ?', 'type': 'reponse_courte', 'reponse': 'Pour être en sécurité et vivre ensemble'},
                            ]
                        }
                    ]
                },

                'ce1': {
                    'francais': [
                        {
                            'titre': 'Lecture de phrases',
                            'contenu': 'Une phrase exprime une idée.',
                            'exercices': [
                                {'question': 'Lis la phrase', 'type': 'redaction', 'reponse': 'Lecture orale'},
                                {'question': 'Compte les mots', 'type': 'reponse_courte', 'reponse': 'Accepte le nombre correct'},
                            ]
                        },
                        {
                            'titre': 'Nom et verbe',
                            'contenu': 'Le nom désigne, le verbe indique l\'action.',
                            'exercices': [
                                {'question': 'Entoure le verbe', 'type': 'choix_multiple', 'reponse': 'verbe'},
                                {'question': 'Entoure le nom', 'type': 'choix_multiple', 'reponse': 'nom'},
                            ]
                        }
                    ],
                    'mathematiques': [
                        {
                            'titre': 'Addition et soustraction',
                            'contenu': 'Additions et soustractions simples.',
                            'exercices': [
                                {'question': '15 + 4 =', 'type': 'calcul', 'reponse': '19'},
                                {'question': '20 − 5 =', 'type': 'calcul', 'reponse': '15'},
                            ]
                        },
                        {
                            'titre': 'Comparer les nombres',
                            'contenu': 'Comparer des nombres pour identifier le plus grand.',
                            'exercices': [
                                {'question': '12 __ 18', 'type': 'choix_multiple', 'reponse': '<', 'options': ['<','>','=','≤']},
                                {'question': 'Entoure le plus grand', 'type': 'choix_multiple', 'reponse': '18', 'options': ['12','18']},
                            ]
                        }
                    ],
                    'sciences': [
                        {
                            'titre': 'L\'eau',
                            'contenu': 'L\'eau est essentielle à la vie.',
                            'exercices': [
                                {'question': 'Cite un usage de l\'eau', 'type': 'reponse_courte', 'reponse': 'boire, cuisiner, laver'},
                                {'question': 'L\'eau est-elle importante ?', 'type': 'vrai_faux', 'reponse': 'Oui'},
                            ]
                        },
                        {
                            'titre': 'L\'hygiène',
                            'contenu': 'Règles d\'hygiène de base.',
                            'exercices': [
                                {'question': 'Quand se laver les mains ?', 'type': 'choix_multiple', 'reponse': 'Avant de manger et après les toilettes', 'options': ['Avant de manger','Après les toilettes','Jamais']},
                                {'question': 'Pourquoi l\'hygiène est importante ?', 'type': 'reponse_courte', 'reponse': 'Prévenir les maladies'},
                            ]
                        }
                    ],
                    'histoire_geo': [
                        {
                            'titre': 'La famille',
                            'contenu': 'La famille et ses membres.',
                            'exercices': [
                                {'question': 'Qui compose la famille ?', 'type': 'reponse_courte', 'reponse': 'Le père, la mère, les enfants'},
                                {'question': 'Cite un membre', 'type': 'reponse_courte', 'reponse': 'grand-parent, frère, sœur'},
                            ]
                        },
                        {
                            'titre': 'Les lieux publics',
                            'contenu': 'Exemples et usages des lieux publics.',
                            'exercices': [
                                {'question': 'Cite un lieu public', 'type': 'reponse_courte', 'reponse': 'école, marché, hôpital'},
                                {'question': 'À quoi sert-il ?', 'type': 'reponse_courte', 'reponse': 'Permet des services ou rencontres'},
                            ]
                        }
                    ],
                    'education_civique': [
                        {
                            'titre': "Droits de l\'enfant",
                            'contenu': 'Notions simples sur les droits de l\'enfant.',
                            'exercices': [
                                {'question': 'Cite un droit', 'type': 'reponse_courte', 'reponse': 'Le droit à l\'éducation'},
                                {'question': 'L\'enfant a-t-il droit à l\'école ?', 'type': 'vrai_faux', 'reponse': 'Oui'},
                            ]
                        },
                        {
                            'titre': 'La politesse',
                            'contenu': 'Comportements polis et vocabulaire associé.',
                            'exercices': [
                                {'question': 'Donne un mot poli', 'type': 'reponse_courte', 'reponse': 's\'il vous plaît, merci'},
                                {'question': 'Pourquoi être poli ?', 'type': 'reponse_courte', 'reponse': 'Pour bien vivre ensemble'},
                            ]
                        }
                    ]
                },

                # CE2 / CM1 / CM2 concise topics, 2 lessons per subject using given topics
                'ce2': {},
                'cm1': {},
                'cm2': {},
            }

            # Helper to add concise structured lessons for CE2-CM2
            def add_brief_level(level_key, topics_map):
                curriculum[level_key] = {}
                for mat_key, topics in topics_map.items():
                    curriculum[level_key][mat_key] = []
                    for idx, topic in enumerate(topics, 1):
                        titre = topic.get('titre')
                        contenu = topic.get('contenu')
                        exercices = topic.get('exercices')
                        curriculum[level_key][mat_key].append({'titre': titre, 'contenu': contenu, 'exercices': exercices})

            # CE2 topics (as provided): multiplication simple, corps humain, commune, règles
            ce2_topics = {
                'francais': [
                    {'titre': 'Lecture avancée', 'contenu': 'Lecture et compréhension de textes courts.', 'exercices': [
                        {'question': 'Lis et comprends le court texte', 'type': 'redaction', 'reponse': 'Réponse libre'},
                        {'question': 'Réponds à une question sur le texte', 'type': 'reponse_courte', 'reponse': 'Réponse courte'}]},
                    {'titre': 'Vocabulaire et orthographe', 'contenu': 'Mots et orthographe courante.', 'exercices': [
                        {'question': 'Écris le mot correctement', 'type': 'reponse_courte', 'reponse': 'Mot correct'},
                        {'question': 'Entoure la bonne orthographe', 'type': 'choix_multiple', 'reponse': 'bonne orthographe'}]},
                ],
                'mathematiques': [
                    {'titre': 'Multiplication simple', 'contenu': 'Introduction aux tables simples.', 'exercices': [
                        {'question': '2 x 3 =', 'type': 'calcul', 'reponse': '6'},
                        {'question': '4 x 5 =', 'type': 'calcul', 'reponse': '20'}]},
                    {'titre': 'Problèmes simples', 'contenu': 'Résoudre petits problèmes avec multiplications.', 'exercices': [
                        {'question': 'Si 2 sacs ont 3 pommes chacun, combien ?','type':'calcul','reponse':'6'},
                        {'question':'Résous le petit problème','type':'reponse_courte','reponse':'Réponse'}]},
                ],
                'sciences': [
                    {'titre': 'Le corps humain (CE2)', 'contenu': 'Organes et fonctions de base.', 'exercices': [
                        {'question':'Cite un organe','type':'reponse_courte','reponse':'cœur, poumons'},
                        {'question':'À quoi sert le cœur ?','type':'reponse_courte','reponse':'Pomper le sang'}]},
                    {'titre': 'Environnement local', 'contenu': 'Notions sur la commune.', 'exercices': [
                        {'question':'Cite un service de la commune','type':'reponse_courte','reponse':'école, mairie'},
                        {'question':'Pourquoi s\'occuper de la commune ?','type':'reponse_courte','reponse':'Pour vivre mieux'}]},
                ],
                'histoire_geo': [
                    {'titre':'La commune','contenu':'Organisation locale et rôle du maire.','exercices':[
                        {'question':'Qui dirige la commune ?','type':'reponse_courte','reponse':'Le maire'},
                        {'question':'Cite un service public','type':'reponse_courte','reponse':'école, mairie'}]},
                    {'titre':'Règles et vie collective','contenu':'Règles de vie en communauté.','exercices':[
                        {'question':'Donne une règle de la classe','type':'reponse_courte','reponse':'Écouter, respecter'},
                        {'question':'Pourquoi respecter les règles ?','type':'reponse_courte','reponse':'Pour vivre ensemble'}]},
                ],
                'education_civique': [
                    {'titre':'Responsabilités','contenu':'Notions de devoirs et responsabilités.', 'exercices':[
                        {'question':'Qu\'est-ce qu\'une responsabilité ?','type':'reponse_courte','reponse':'Faire ce qui est attendu'},
                        {'question':'Donne un exemple','type':'reponse_courte','reponse':'Ranger sa classe'}]},
                    {'titre':'Règles locales','contenu':'Règles pour bien vivre ensemble.', 'exercices':[
                        {'question':'Une règle utile ?','type':'reponse_courte','reponse':'Respect, propreté'},
                        {'question':'Pourquoi respecter la loi ?','type':'reponse_courte','reponse':'Sécurité et justice'}]},
                ]
            }

            # CM1 topics: fractions simples, environnement, régions du Burkina
            cm1_topics = {
                'francais': [
                    {'titre':'Compréhension de texte (CM1)','contenu':'Lire et expliquer un texte plus long.','exercices':[
                        {'question':'Résume le texte','type':'redaction','reponse':'Résumé court'},
                        {'question':'Trouve le mot-clé','type':'reponse_courte','reponse':'Mot'}]},
                    {'titre':'Vocabulaire avancé','contenu':'Mots de vocabulaire liés au thème.','exercices':[
                        {'question':'Donne un synonyme','type':'reponse_courte','reponse':'Synonyme'},
                        {'question':'Donne un antonyme','type':'reponse_courte','reponse':'Antonyme'}]},
                ],
                'mathematiques': [
                    {'titre':'Fractions simples','contenu':'Comprendre la moitié, le quart.', 'exercices':[
                        {'question':'1/2 de 8 =','type':'calcul','reponse':'4'},
                        {'question':'1/4 de 12 =','type':'calcul','reponse':'3'}]},
                    {'titre':'Problèmes et applications','contenu':'Utiliser fractions dans problèmes simples.','exercices':[
                        {'question':'Problème simple','type':'reponse_courte','reponse':'Réponse'},
                        {'question':'Résous','type':'calcul','reponse':'Réponse numérique'}]},
                ],
                'sciences': [
                    {'titre':'Environnement local (CM1)','contenu':'Étude du milieu et ressources.', 'exercices':[
                        {'question':'Cite une ressource','type':'reponse_courte','reponse':'Eau, terre'},
                        {'question':'Pourquoi protéger l\'environnement ?','type':'reponse_courte','reponse':'Pour l\'avenir'}]},
                    {'titre':'Régions du Burkina','contenu':'Introduction aux régions locales.', 'exercices':[
                        {'question':'Cite une région','type':'reponse_courte','reponse':'Région X'},
                        {'question':'Capitale de la région','type':'reponse_courte','reponse':'Réponse'}]},
                ],
                'histoire_geo': [
                    {'titre':'Géographie locale','contenu':'Espaces, cartes et repères.', 'exercices':[
                        {'question':'Indique un repère','type':'reponse_courte','reponse':'École, rivière'},
                        {'question':'Cite un point cardinal','type':'reponse_courte','reponse':'Nord, Sud'}]},
                    {'titre':'Histoire locale','contenu':'Éléments historiques simples.', 'exercices':[
                        {'question':'Un fait historique local','type':'reponse_courte','reponse':'Réponse'},
                        {'question':'Pourquoi c\'est important ?','type':'reponse_courte','reponse':'Comprendre le passé'}]},
                ],
                'education_civique': [
                    {'titre':'Citoyenneté locale','contenu':'Notions de participation civique.', 'exercices':[
                        {'question':'Comment aider la commune ?','type':'reponse_courte','reponse':'Participer, nettoyer'},
                        {'question':'Donne un exemple','type':'reponse_courte','reponse':'Bénévolat'}]},
                    {'titre':'Règles et droits','contenu':'Droits et devoirs simples.', 'exercices':[
                        {'question':'Un droit important','type':'reponse_courte','reponse':'Éducation'},
                        {'question':'Un devoir','type':'reponse_courte','reponse':'Respecter les autres'}]},
                ]
            }

            # CM2 topics: problèmes, santé, Afrique, symboles nationaux
            cm2_topics = {
                'francais': [
                    {'titre':'Rédaction et argumentation','contenu':'Écrire un court texte argumenté.', 'exercices':[
                        {'question':'Rédige un paragraphe','type':'redaction','reponse':'Texte'},
                        {'question':'Donne une idée principale','type':'reponse_courte','reponse':'Idée'}]},
                    {'titre':'Analyse de texte','contenu':'Identifier idées et détails.', 'exercices':[
                        {'question':'Trouve l\'idée principale','type':'reponse_courte','reponse':'Idée'},
                        {'question':'Cite un détail','type':'reponse_courte','reponse':'Détail'}]},
                ],
                'mathematiques': [
                    {'titre':'Résolution de problèmes','contenu':'Stratégies pour résoudre problèmes.', 'exercices':[
                        {'question':'Problème à résoudre','type':'reponse_courte','reponse':'Réponse'},
                        {'question':'Montre les étapes','type':'redaction','reponse':'Étapes'}]},
                    {'titre':'Santé et mesures','contenu':'Notions de santé appliquées aux mathématiques (mesures).', 'exercices':[
                        {'question':'Mesure simple','type':'calcul','reponse':'Réponse'},
                        {'question':'Pourquoi mesurer ?','type':'reponse_courte','reponse':'Pour comparer'}]},
                ],
                'sciences': [
                    {'titre':'Santé et hygiène (CM2)','contenu':'Notions de santé et prévention.', 'exercices':[
                        {'question':'Donne une règle de santé','type':'reponse_courte','reponse':'Se laver les mains'},
                        {'question':'Pourquoi se soigner ?','type':'reponse_courte','reponse':'Pour guérir'}]},
                    {'titre':'Afrique : milieux et cultures','contenu':'Introduction aux pays africains et cultures.', 'exercices':[
                        {'question':'Cite un pays africain','type':'reponse_courte','reponse':'Burkina Faso, Mali, etc.'},
                        {'question':'Cite une pratique culturelle','type':'reponse_courte','reponse':'Réponse'}]},
                ],
                'histoire_geo': [
                    {'titre':'Symboles nationaux','contenu':'Drapeau, hymne, emblèmes.', 'exercices':[
                        {'question':'Quel est le drapeau ?','type':'reponse_courte','reponse':'Description'},
                        {'question':'Quel est l\'hymne national ?','type':'reponse_courte','reponse':'Titre'}]},
                    {'titre':'Histoire et patrimoine','contenu':'Éléments du patrimoine national.', 'exercices':[
                        {'question':'Cite un monument national','type':'reponse_courte','reponse':'Réponse'},
                        {'question':'Pourquoi le préserver ?','type':'reponse_courte','reponse':'Pour l\'histoire'}]},
                ],
                'education_civique': [
                    {'titre':'Droits et devoirs (CM2)','contenu':'Notions civiques avancées.', 'exercices':[
                        {'question':'Cite un droit fondamental','type':'reponse_courte','reponse':'Éducation, santé'},
                        {'question':'Cite un devoir','type':'reponse_courte','reponse':'Respect de la loi'}]},
                    {'titre':'Participation citoyenne','contenu':'Comment participer à la vie publique.', 'exercices':[
                        {'question':'Comment participer ?','type':'reponse_courte','reponse':'Vote, bénévolat'},
                        {'question':'Pourquoi participer ?','type':'reponse_courte','reponse':'Pour améliorer la communauté'}]},
                ]
            }

            add_brief_level('ce2', ce2_topics)
            add_brief_level('cm1', cm1_topics)
            add_brief_level('cm2', cm2_topics)

            # Create all lessons/exercises
            total_lecons = 0
            total_exos = 0
            for niveau, matieres_map in curriculum.items():
                for mat_key, lecons_list in matieres_map.items():
                    matiere = matieres.get(mat_key)
                    if not matiere:
                        continue
                    for ordre_idx, lecon_data in enumerate(lecons_list, 1):
                        lecon, created = Lecon.objects.update_or_create(
                            matiere=matiere,
                            titre=lecon_data['titre'],
                            defaults={
                                'contenu_principal': lecon_data.get('contenu',''),
                                'niveau_scolaire': niveau,
                                'niveau_global': 'débutant',
                                'ordre': ordre_idx,
                                'difficulte': 3,
                                'temps_estime': 15,
                            }
                        )
                        total_lecons += 1
                        for ex_idx, ex in enumerate(lecon_data['exercices'], 1):
                            exercice, ex_created = Exercice.objects.update_or_create(
                                lecon=lecon,
                                question=ex['question'],
                                defaults={
                                    'matiere': matiere,
                                    'type_exercice': ex.get('type', 'reponse_courte'),
                                    'reponse_correcte': ex.get('reponse',''),
                                    'options': ex.get('options', []),
                                    'niveau': niveau,
                                    'ordre': ex_idx,
                                }
                            )
                            total_exos += 1

            self.stdout.write(self.style.SUCCESS(f"\n✅ Population terminée: {total_lecons} leçons, {total_exos} exercices créés/actualisés."))

"""
Management command to populate CP1 curriculum with complete lessons and exercises
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Matiere, Lecon, Exercice, NiveauScolaire


class Command(BaseCommand):
    help = 'Populate the database with CP1 curriculum (lessons and exercises)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🚀 Starting CP1 curriculum population..."))
        
        with transaction.atomic():
            # Create or get NiveauScolaire for CP1
            niveau_cp1, created = NiveauScolaire.objects.get_or_create(
                code='cp1',
                defaults={
                    'libelle': 'CP1',
                    'ordre': 1,
                    'cycle': 'Primaire'
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS("✓ Created NiveauScolaire: CP1"))
            
            # Create or get Matieres
            matieres_data = {
                'francais': ('francais', 'Français', '🔤'),
                'mathematiques': ('mathematiques', 'Mathématiques', '🔢'),
                'sciences': ('sciences', 'Sciences', '🔬'),
                'histoire_geo': ('histoire_geo', 'Histoire-Géographie', '🌍'),
                'education_civique': ('education_civique', 'Éducation civique', '👥'),
            }
            
            matieres = {}
            for key, (code, nom, icone) in matieres_data.items():
                # Try to get by nom display or create
                try:
                    matiere = Matiere.objects.get(nom=code)
                except Matiere.DoesNotExist:
                    matiere = Matiere.objects.create(
                        nom=code,
                        description=f"Matière: {nom}",
                        icone=icone
                    )
                    self.stdout.write(self.style.SUCCESS(f"✓ Created Matière: {nom}"))
                matieres[key] = matiere
            
            # CP1 Curriculum Data
            curriculum = {
                'francais': {
                    'matiere': matieres['francais'],
                    'lecons': [
                        {
                            'titre': 'Les voyelles (a, e, i, o, u)',
                            'contenu_principal': '''Les voyelles sont des lettres que l'on peut prononcer seules.

Les voyelles sont : a, e, i, o, u.

Elles sont très importantes pour former des mots. Chaque voyelle a un son différent.
- "a" comme dans apple
- "e" comme dans élève
- "i" comme dans igloo
- "o" comme dans orange
- "u" comme dans univers''',
                            'ordre': 1,
                            'exercices': [
                                {
                                    'question': 'Entoure les voyelles : b – a – t – o – l',
                                    'type_exercice': 'choix_multiple',
                                    'reponse_correcte': 'a, o',
                                    'options': ['a', 'b', 'o', 't', 'l'],
                                },
                                {
                                    'question': 'Complète la série : a – e – … – o – u',
                                    'type_exercice': 'reponse_courte',
                                    'reponse_correcte': 'i',
                                },
                            ]
                        },
                        {
                            'titre': 'Les consonnes',
                            'contenu_principal': '''Les consonnes sont des lettres que l'on ne peut pas prononcer seules.

Contrairement aux voyelles, les consonnes ont besoin d'être associées à une voyelle pour faire un son.

Exemples de consonnes : b, c, d, f, g, h, j, k, l, m, n, p, q, r, s, t, v, w, x, y, z.

Les consonnes aident à former des mots quand elles sont combinées avec les voyelles.''',
                            'ordre': 2,
                            'exercices': [
                                {
                                    'question': 'Entoure les consonnes : a – b – i – d – o',
                                    'type_exercice': 'choix_multiple',
                                    'reponse_correcte': 'b, d',
                                    'options': ['a', 'b', 'i', 'd', 'o'],
                                },
                                {
                                    'question': 'Cite 3 consonnes',
                                    'type_exercice': 'reponse_courte',
                                    'reponse_correcte': 'Accepte toute réponse avec 3 consonnes valides',
                                },
                            ]
                        },
                    ]
                },
                'mathematiques': {
                    'matiere': matieres['mathematiques'],
                    'lecons': [
                        {
                            'titre': 'Les nombres de 1 à 10',
                            'contenu_principal': '''Les nombres servent à compter.

On apprend à compter de 1 à 10 :
1 - 2 - 3 - 4 - 5 - 6 - 7 - 8 - 9 - 10

Chaque nombre représente une quantité d'objets.
- 1 = un objet
- 2 = deux objets
- 3 = trois objets
... et ainsi de suite jusqu'à 10.

C'est la base pour comprendre les mathématiques.''',
                            'ordre': 1,
                            'exercices': [
                                {
                                    'question': 'Compte les objets : 🍎🍎🍎. Il y a combien de pommes ?',
                                    'type_exercice': 'calcul',
                                    'reponse_correcte': '3',
                                },
                                {
                                    'question': 'Complète : 1 – 2 – 3 – … – 5',
                                    'type_exercice': 'reponse_courte',
                                    'reponse_correcte': '4',
                                },
                            ]
                        },
                        {
                            'titre': 'Comparer des quantités',
                            'contenu_principal': '''On peut comparer les quantités en utilisant :
- "plus que" (ou "plus grand que")
- "moins que" (ou "plus petit que")
- "égal à" (ou "pareil")

Par exemple :
3 ● ● ● est plus petit que 5 ● ● ● ● ●
4 objets est égal à 4 objets
2 ● ● est moins que 6 ● ● ● ● ● ●

Pour comparer, on compte les objets et on regarde quel groupe en a plus.''',
                            'ordre': 2,
                            'exercices': [
                                {
                                    'question': 'Regarde : 3 ●●● et 5 ●●●●●. Qui est plus grand ?',
                                    'type_exercice': 'choix_multiple',
                                    'reponse_correcte': '5',
                                    'options': ['3', '5'],
                                },
                                {
                                    'question': 'Entoure : 2 ___ 4. C\'est plus petit ou plus grand ?',
                                    'type_exercice': 'choix_multiple',
                                    'reponse_correcte': 'plus petit',
                                    'options': ['plus petit', 'plus grand', 'égal'],
                                },
                            ]
                        },
                    ]
                },
                'sciences': {
                    'matiere': matieres['sciences'],
                    'lecons': [
                        {
                            'titre': 'Le corps humain',
                            'contenu_principal': '''Le corps humain a plusieurs parties importantes :

1. La tête - où se trouvent les yeux, le nez, la bouche, les oreilles
2. Le tronc - le centre du corps
3. Les bras - qui servent à attraper et à faire diverses actions
4. Les jambes - qui servent à marcher et à se déplacer
5. Les mains et les pieds - les extrémités

Tous ces éléments travaillent ensemble pour nous permettre de faire différentes choses.''',
                            'ordre': 1,
                            'exercices': [
                                {
                                    'question': 'Cite 2 parties du corps',
                                    'type_exercice': 'reponse_courte',
                                    'reponse_correcte': 'Accepte toute réponse avec 2 parties du corps',
                                },
                                {
                                    'question': 'À quoi servent les jambes ?',
                                    'type_exercice': 'reponse_courte',
                                    'reponse_correcte': 'À marcher, à courir, à se déplacer',
                                },
                            ]
                        },
                        {
                            'titre': 'Les cinq sens',
                            'contenu_principal': '''Nous avons cinq sens qui nous permettent de percevoir le monde :

1. La vue - avec les yeux, on voit les couleurs, les formes
2. L\'ouïe - avec les oreilles, on entend les bruits et la musique
3. L\'odorat - avec le nez, on sent les odeurs
4. Le goût - avec la langue, on goûte les saveurs
5. Le toucher - avec la peau, on sent la texture des choses

Chaque sens nous donne des informations différentes sur le monde qui nous entoure.
Ensemble, ils nous aident à apprendre et à nous orienter.''',
                            'ordre': 2,
                            'exercices': [
                                {
                                    'question': 'Avec quoi voit-on ?',
                                    'type_exercice': 'choix_multiple',
                                    'reponse_correcte': 'yeux',
                                    'options': ['les yeux', 'les oreilles', 'le nez', 'la langue'],
                                },
                                {
                                    'question': 'Cite deux sens',
                                    'type_exercice': 'reponse_courte',
                                    'reponse_correcte': 'Accepte toute réponse avec 2 sens valides',
                                },
                            ]
                        },
                    ]
                },
                'histoire_geo': {
                    'matiere': matieres['histoire_geo'],
                    'lecons': [
                        {
                            'titre': 'La famille',
                            'contenu_principal': '''La famille est le groupe de personnes avec qui nous vivons.

Une famille typique est composée de :
- Le père
- La mère
- Les enfants

Il peut y avoir aussi :
- Les grands-parents
- Les frères et sœurs
- Les cousins et cousines
- Les oncles et tantes

La famille est importante car elle nous aide à grandir, à apprendre, et elle nous aime.
Nous passons du temps ensemble et nous nous aidons les uns les autres.''',
                            'ordre': 1,
                            'exercices': [
                                {
                                    'question': 'Qui sont les membres principaux d\'une famille ?',
                                    'type_exercice': 'reponse_courte',
                                    'reponse_correcte': 'Le père, la mère et les enfants',
                                },
                                {
                                    'question': 'Qui d\'autre peut faire partie d\'une famille ?',
                                    'type_exercice': 'reponse_courte',
                                    'reponse_correcte': 'Les grands-parents, les frères, les sœurs, les cousins',
                                },
                            ]
                        },
                        {
                            'titre': 'Le village ou le quartier',
                            'contenu_principal': '''Le village ou le quartier est l\'endroit où nous vivons.

C\'est le groupe de maisons et de bâtiments près de notre maison.

Dans un village ou un quartier, il y a :
- Des maisons où vivent les gens
- Une école où on apprend
- Un marché où on achète des choses
- Une place publique pour se rassembler
- Souvent une église ou une mosquée

Le village ou le quartier est notre communauté locale.
Nous y connaissons nos voisins et nous y passons nos journées.''',
                            'ordre': 2,
                            'exercices': [
                                {
                                    'question': 'Comment s\'appelle ton village ou quartier ?',
                                    'type_exercice': 'reponse_courte',
                                    'reponse_correcte': 'Accepte le nom local de l\'élève',
                                },
                                {
                                    'question': 'Cite un lieu de ton quartier',
                                    'type_exercice': 'reponse_courte',
                                    'reponse_correcte': 'Accepte: école, marché, place, maison, église, etc.',
                                },
                            ]
                        },
                    ]
                },
                'education_civique': {
                    'matiere': matieres['education_civique'],
                    'lecons': [
                        {
                            'titre': 'Le respect',
                            'contenu_principal': '''Respecter, c\'est bien se comporter avec les autres.

Le respect signifie :
- Écouter les autres
- Ne pas faire du mal aux autres
- Partager et être gentil
- Dire "s\'il vous plaît" et "merci"
- Obéir aux adultes
- Attendre son tour

Le respect est très important pour vivre ensemble en paix et en harmonie.
Quand on respecte les autres, les autres nous respectent aussi.''',
                            'ordre': 1,
                            'exercices': [
                                {
                                    'question': 'Donne un exemple de respect',
                                    'type_exercice': 'reponse_courte',
                                    'reponse_correcte': 'Accepte: écouter, partager, être gentil, attendre son tour, être obéissant',
                                },
                                {
                                    'question': 'Faut-il respecter les adultes ?',
                                    'type_exercice': 'vrai_faux',
                                    'reponse_correcte': 'Oui',
                                },
                            ]
                        },
                        {
                            'titre': 'La propreté',
                            'contenu_principal': '''La propreté protège notre santé.

Une bonne hygiène signifie :
- Se laver les mains avant de manger
- Se laver les mains après être allé aux toilettes
- Garder notre chambre et notre école propres
- Se brosser les dents
- Jeter les déchets aux bons endroits
- Garder les rues et les espaces publics propres

La propreté est importante car :
- Elle prévient les maladies
- Elle rend notre environnement agréable
- Elle montre du respect pour nous-mêmes et pour les autres''',
                            'ordre': 2,
                            'exercices': [
                                {
                                    'question': 'Quand faut-il se laver les mains ?',
                                    'type_exercice': 'choix_multiple',
                                    'reponse_correcte': 'Avant de manger et après les toilettes',
                                    'options': ['Avant de manger', 'Après les toilettes', 'Le soir', 'Tout le temps'],
                                },
                                {
                                    'question': 'Cite une chose qu\'il ne faut pas jeter par terre',
                                    'type_exercice': 'reponse_courte',
                                    'reponse_correcte': 'Accepte: papier, plastique, verre, nourriture, stylo, etc.',
                                },
                            ]
                        },
                    ]
                },
            }
            
            # Create lessons and exercises
            for matiere_key, matiere_data in curriculum.items():
                matiere = matiere_data['matiere']
                self.stdout.write(f"\n📚 Processing {matiere.get_nom_display()}...")
                
                for lecon_data in matiere_data['lecons']:
                    # Create lesson
                    lecon, created = Lecon.objects.update_or_create(
                        matiere=matiere,
                        titre=lecon_data['titre'],
                        defaults={
                            'contenu_principal': lecon_data['contenu_principal'],
                            'niveau_scolaire': 'cp1',
                            'niveau_global': 'débutant',
                            'ordre': lecon_data.get('ordre', 0),
                            'difficulte': 2,
                            'temps_estime': 15,
                        }
                    )
                    
                    status = "Updated" if not created else "Created"
                    self.stdout.write(f"  ✓ {status} lesson: {lecon.titre}")
                    
                    # Create exercises
                    for idx, exercice_data in enumerate(lecon_data['exercices'], 1):
                        exercice, created = Exercice.objects.update_or_create(
                            lecon=lecon,
                            question=exercice_data['question'],
                            defaults={
                                'matiere': matiere,
                                'type_exercice': exercice_data.get('type_exercice', 'choix_multiple'),
                                'reponse_correcte': exercice_data['reponse_correcte'],
                                'options': exercice_data.get('options', []),
                                'ordre': idx,
                            }
                        )
                        status = "Updated" if not created else "Created"
                        self.stdout.write(f"    ✓ {status} exercise {idx}")
        
        self.stdout.write(self.style.SUCCESS("\n✅ CP1 curriculum population completed successfully!"))
        self.stdout.write(self.style.WARNING("\n📖 Summary:"))
        self.stdout.write(f"  • 5 Matières")
        self.stdout.write(f"  • 10 Leçons (2 par matière)")
        self.stdout.write(f"  • 20 Exercices (2 par leçon)")

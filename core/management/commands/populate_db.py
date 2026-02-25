from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date

from core.models import Lecon, Exercice, Utilisateur, Matiere, NiveauScolaire


class Command(BaseCommand):
    help = 'Populate database with test data'

    def handle(self, *args, **options):
        # Créer les niveaux scolaires (CP1 → Terminale)
        from django.core.management import call_command
        call_command('populate_niveaux')

        # Créer les matières (visibles dans Tuteur IA et filtres)
        matieres_data = [
            ('mathematiques', 'Mathématiques', '#3B82F6', '🔢'),
            ('francais', 'Français', '#10B981', '📖'),
            ('sciences', 'Sciences', '#F59E0B', '🔬'),
            ('anglais', 'Anglais', '#8B5CF6', '🌍'),
            ('histoire_geo', 'Histoire-Géographie', '#EF4444', '🗺️'),
        ]
        matiere_math = None
        for nom, desc, couleur, icone in matieres_data:
            m, _ = Matiere.objects.get_or_create(
                nom=nom,
                defaults={'description': desc, 'couleur_hex': couleur, 'icone': icone}
            )
            if nom == 'mathematiques':
                matiere_math = m

        self.stdout.write('✅ Matières créées')

        # Utilisateurs de test — niveau scolaire défini une seule fois (CP1 → Terminale)
        users_data = [
            {
                'username': 'alice',
                'email': 'alice@test.com',
                'password': '123456',
                'prenom': 'Alice',
                'nom': 'Dupont',
                'date_naissance': date(2010, 5, 15),
                'niveau_scolaire': 'ce1',
                'parent_email': 'parent.alice@test.com',
                'telephone': '+33612345678',
            },
            {
                'username': 'bob',
                'email': 'bob@test.com',
                'password': '123456',
                'prenom': 'Bob',
                'nom': 'Martin',
                'date_naissance': date(2009, 8, 20),
                'niveau_scolaire': '5eme',
                'parent_email': 'parent.bob@test.com',
                'telephone': '+33623456789',
            },
            {
                'username': 'charlie',
                'email': 'charlie@test.com',
                'password': '123456',
                'prenom': 'Charlie',
                'nom': 'Bernard',
                'date_naissance': date(2008, 3, 10),
                'niveau_scolaire': '1ere',
                'parent_email': 'parent.charlie@test.com',
                'telephone': '+33634567890',
            },
        ]

        for ud in users_data:
            password = ud.pop('password')
            niveau_scolaire = ud.pop('niveau_scolaire')
            username = ud.pop('username')
            email = ud.pop('email')
            niveau_global = 'débutant' if niveau_scolaire in ('cp1', 'cp2', 'ce1', 'ce2', 'cm1', 'cm2') else (
                'intermédiaire' if niveau_scolaire in ('6eme', '5eme', '4eme', '3eme') else 'avancé'
            )
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email, 'first_name': ud['prenom'], 'last_name': ud['nom'], 'is_active': True}
            )
            # Toujours mettre à jour le mot de passe (hashé) pour permettre la connexion
            user.set_password(password)
            user.is_active = True
            user.save(update_fields=['password', 'is_active'])

            Utilisateur.objects.get_or_create(
                user=user,
                defaults={
                    'nom': ud['nom'],
                    'prenom': ud['prenom'],
                    'date_naissance': ud['date_naissance'],
                    'niveau_scolaire': niveau_scolaire,
                    'niveau_global': niveau_global,
                    'parent_email': ud['parent_email'],
                    'telephone': ud['telephone'],
                }
            )

        self.stdout.write(self.style.SUCCESS('✅ Utilisateurs créés (alice/123456=CE1, bob/123456=5ème, charlie/123456=1ère)'))

        # Récupérer les matières et niveaux pour créer les leçons par niveau
        matiere_fr = Matiere.objects.filter(nom='francais').first()
        matiere_sciences = Matiere.objects.filter(nom='sciences').first()

        # Leçons par niveau scolaire (niveau = FK NiveauScolaire) pour chaîne niveau → matières → leçons → exercices
        def creer_lecon(matiere, code_niveau, titre, contenu, exercices_list):
            ns = NiveauScolaire.objects.filter(code=code_niveau).first()
            if not ns:
                return
            lecon, _ = Lecon.objects.get_or_create(
                matiere=matiere,
                niveau=ns,
                titre=titre,
                defaults={
                    'contenu_principal': contenu,
                    'niveau_global': 'débutant' if code_niveau in ('cp1', 'cp2', 'ce1', 'ce2', 'cm1', 'cm2') else (
                        'intermédiaire' if code_niveau in ('6eme', '5eme', '4eme', '3eme') else 'avancé'
                    ),
                }
            )
            for ex in exercices_list:
                Exercice.objects.get_or_create(
                    lecon=lecon,
                    matiere=matiere,
                    question=ex['question'],
                    defaults={'reponse_correcte': ex['reponse_correcte'], 'niveau': ex.get('niveau', 'débutant')}
                )

        # CE1 — Maths + Français (pour alice)
        creer_lecon(
            matiere_math, 'ce1', "Les bases de l'addition",
            "L'addition, c'est mettre ensemble. 2 + 3 = 5.",
            [
                {'question': 'Quelle est la somme de 2 + 3 ?', 'reponse_correcte': '5'},
                {'question': 'Quelle est la somme de 5 + 4 ?', 'reponse_correcte': '9'},
                {'question': 'Quelle est la somme de 10 + 7 ?', 'reponse_correcte': '17'},
            ]
        )
        creer_lecon(
            matiere_math, 'ce1', 'Géométrie basique',
            "Le triangle a 3 côtés. Le carré a 4 côtés égaux. L'angle droit fait 90°.",
            [
                {'question': 'Combien de côtés a un triangle ?', 'reponse_correcte': '3'},
                {'question': "Quel est le nom d'une forme à 4 côtés égaux ?", 'reponse_correcte': 'carré'},
                {'question': 'Quel est le nombre de degrés dans un angle droit ?', 'reponse_correcte': '90'},
            ]
        )
        if matiere_fr:
            creer_lecon(
                matiere_fr, 'ce1', 'Les voyelles',
                "Les voyelles sont A, E, I, O, U, Y. On les prononce dans chaque mot.",
                [
                    {'question': 'Combien y a-t-il de voyelles en français ?', 'reponse_correcte': '6'},
                    {'question': "Quelle lettre n'est pas une voyelle : A, B ou E ?", 'reponse_correcte': 'B'},
                ]
            )

        # 5ème — Maths + Sciences (pour bob)
        creer_lecon(
            matiere_math, '5eme', 'Les tables de multiplication',
            "Réviser les tables de 1 à 10. Par exemple 6 × 7 = 42.",
            [
                {'question': 'Quel est le résultat de 6 × 7 ?', 'reponse_correcte': '42'},
                {'question': 'Quel est le résultat de 8 × 9 ?', 'reponse_correcte': '72'},
            ]
        )
        creer_lecon(
            matiere_math, '5eme', 'Fractions et pourcentages',
            "Une fraction représente une partie. 50% = 1/2. 25% = 1/4.",
            [
                {'question': 'Quelle est la moitié de 64 ?', 'reponse_correcte': '32'},
                {'question': 'Quel est 50% de 200 ?', 'reponse_correcte': '100'},
            ]
        )
        if matiere_sciences:
            creer_lecon(
                matiere_sciences, '5eme', 'Le système solaire',
                "Le Soleil est une étoile. La Terre tourne autour du Soleil en un an.",
                [
                    {'question': 'Autour de quoi la Terre tourne-t-elle ?', 'reponse_correcte': 'le Soleil'},
                ]
            )

        # 1ère — Maths (pour charlie)
        creer_lecon(
            matiere_math, '1ere', 'Équations linéaires',
            "Résoudre ax + b = c : isoler x. Exemple : x + 5 = 12 donc x = 7.",
            [
                {'question': 'Résoudre: x + 5 = 12 (réponse: x = ?)', 'reponse_correcte': '7'},
                {'question': 'Résoudre: 2x = 18 (réponse: x = ?)', 'reponse_correcte': '9'},
            ]
        )

        self.stdout.write(self.style.SUCCESS('✅ Leçons et exercices créés (CE1, 5ème, 1ère)'))
        self.stdout.write(self.style.SUCCESS('\n🎉 Base prête. Connexion: alice/123456 (CE1), bob/123456 (5ème), charlie/123456 (1ère)'))

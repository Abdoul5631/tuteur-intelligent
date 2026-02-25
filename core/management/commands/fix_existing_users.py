"""
Commande : python manage.py fix_existing_users

- Crée un profil Utilisateur pour tout User qui n'en a pas (utilisateurs créés manuellement).
- Réactive les comptes désactivés (is_active=False) si souhaité.
- Les mots de passe en clair sont réparés au premier login (voir login_user).
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Utilisateur


class Command(BaseCommand):
    help = 'Crée le profil Utilisateur pour les User sans profil et réactive les comptes si besoin'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reactivate',
            action='store_true',
            help='Remet is_active=True pour tous les User',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Affiche ce qui serait fait sans modifier la base',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        reactivate = options['reactivate']

        if dry_run:
            self.stdout.write(self.style.WARNING('Mode dry-run : aucune modification.'))

        # Créer Utilisateur pour chaque User sans profil
        created = 0
        for user in User.objects.all():
            if not Utilisateur.objects.filter(user=user).exists():
                if not dry_run:
                    Utilisateur.objects.create(
                        user=user,
                        nom=user.last_name or user.username,
                        prenom=user.first_name or user.username,
                        niveau_scolaire='ce1',
                        niveau_global='débutant',
                    )
                created += 1
                self.stdout.write(f'  Profil créé pour: {user.username}')

        if created:
            self.stdout.write(self.style.SUCCESS(f'{"[dry-run] " if dry_run else ""}Profil(s) créé(s): {created}'))
        else:
            self.stdout.write('Aucun User sans profil.')

        # Optionnel : réactiver les comptes
        if reactivate:
            inactive = User.objects.filter(is_active=False)
            count = inactive.count()
            if count and not dry_run:
                inactive.update(is_active=True)
            if count:
                self.stdout.write(self.style.SUCCESS(f'{"[dry-run] " if dry_run else ""}Compte(s) réactivé(s): {count}'))

        self.stdout.write(self.style.SUCCESS('Terminé. Connexion possible pour tous les utilisateurs avec profil.'))

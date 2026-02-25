from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core import serializers
from django.db import transaction
from datetime import datetime
import os

from core.models import Utilisateur


class Command(BaseCommand):
    help = 'Backup and delete ALL user accounts. Use --yes to confirm. Optionally create an admin with --create-admin user pass'

    def add_arguments(self, parser):
        parser.add_argument('--yes', action='store_true', help='Confirm destructive action')
        parser.add_argument('--create-admin', nargs=2, metavar=('USERNAME', 'PASSWORD'), help='Create an admin user after purge')
        parser.add_argument('--backup-dir', default='.', help='Directory to write backup fixture')

    def handle(self, *args, **options):
        if not options['yes']:
            raise CommandError("This command is destructive. Re-run with --yes to confirm.")

        backup_dir = options['backup_dir']
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        users_backup = os.path.join(backup_dir, f'users_backup_{timestamp}.json')
        profils_backup = os.path.join(backup_dir, f'utilisateurs_backup_{timestamp}.json')

        # Backup users and Utilisateur fixtures
        with open(users_backup, 'w', encoding='utf-8') as f:
            f.write(serializers.serialize('json', User.objects.all()))

        with open(profils_backup, 'w', encoding='utf-8') as f:
            f.write(serializers.serialize('json', Utilisateur.objects.all()))

        self.stdout.write(self.style.SUCCESS(f'Backed up User -> {users_backup}'))
        self.stdout.write(self.style.SUCCESS(f'Backed up Utilisateur -> {profils_backup}'))

        # Delete all profils first, then users
        try:
            with transaction.atomic():
                deleted_profils, _ = Utilisateur.objects.all().delete()
                deleted_users, _ = User.objects.all().delete()
        except Exception as e:
            raise CommandError(f'Error during deletion: {e}')

        self.stdout.write(self.style.SUCCESS(f'Deleted Utilisateur records and User accounts.'))

        # Optionally create admin
        if options['create_admin']:
            username, password = options['create_admin']
            if not username or not password:
                raise CommandError('Both username and password must be provided for --create-admin')
            admin = User.objects.create_superuser(username=username, email='', password=password)
            self.stdout.write(self.style.SUCCESS(f'Created superuser: {username}'))

        self.stdout.write(self.style.SUCCESS('Auth reset complete.'))

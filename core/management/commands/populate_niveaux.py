"""Remplit la table NiveauScolaire (CP1 → Terminale)"""
from django.core.management.base import BaseCommand
from core.models import NiveauScolaire

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


class Command(BaseCommand):
    help = 'Remplit les niveaux scolaires CP1 → Terminale'

    def handle(self, *args, **options):
        for code, libelle, ordre, cycle in NIVEAUX:
            NiveauScolaire.objects.update_or_create(
                code=code,
                defaults={'libelle': libelle, 'ordre': ordre, 'cycle': cycle}
            )
        self.stdout.write(self.style.SUCCESS(f'✅ {len(NIVEAUX)} niveaux créés (CP1 → Terminale)'))

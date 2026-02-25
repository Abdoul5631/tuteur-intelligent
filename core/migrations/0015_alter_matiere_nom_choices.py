# Migration: ajout des matières Lecture, Écriture, Éducation civique

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_lecon_niveau_global_alter_matiere_nom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matiere',
            name='nom',
            field=models.CharField(
                choices=[
                    ('mathematiques', 'Mathématiques'),
                    ('francais', 'Français'),
                    ('lecture', 'Lecture'),
                    ('ecriture', 'Écriture'),
                    ('education_civique', 'Éducation civique'),
                    ('histoire_geo', 'Histoire-Géographie'),
                    ('sciences', 'Sciences'),
                    ('anglais', 'Anglais'),
                    ('sciences_vie', 'Sciences de la Vie et de la Terre'),
                    ('physique', 'Physique'),
                    ('chimie', 'Chimie'),
                    ('physique_chimie', 'Physique-Chimie'),
                    ('technologie', 'Technologie'),
                    ('eps', 'EPS'),
                    ('arts', 'Arts Plastiques'),
                    ('musique', 'Musique'),
                    ('ses', 'Sciences Économiques et Sociales'),
                    ('philosophie', 'Philosophie'),
                    ('espagnol', 'Espagnol'),
                    ('allemand', 'Allemand'),
                ],
                max_length=100,
                unique=True,
            ),
        ),
    ]

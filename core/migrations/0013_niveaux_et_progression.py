# Migration: NiveauScolaire, ProgressionNotion, Lecon.niveau (FK)
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0012_alter_exercice_options_alter_lecon_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='NiveauScolaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('libelle', models.CharField(max_length=50)),
                ('ordre', models.IntegerField(default=0)),
                ('cycle', models.CharField(choices=[('primaire', 'Primaire'), ('college', 'Collège'), ('lycee', 'Lycée')], max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Niveaux scolaires',
                'ordering': ['ordre'],
            },
        ),
        migrations.CreateModel(
            name='ProgressionNotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notion', models.CharField(max_length=100)),
                ('statut', models.CharField(choices=[('faible', 'À revoir'), ('encours', 'En cours'), ('maitrise', 'Maîtrisé')], default='encours', max_length=20)),
                ('score_moyen', models.FloatField(default=0.0)),
                ('nb_tentatives', models.IntegerField(default=0)),
                ('derniere_tentative', models.DateTimeField(blank=True, null=True)),
                ('matiere', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='progression_notions', to='core.matiere')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progression_notions', to='core.utilisateur')),
            ],
            options={
                'verbose_name_plural': 'Progression par notion',
                'unique_together': {('utilisateur', 'notion')},
            },
        ),
        migrations.AddField(
            model_name='lecon',
            name='niveau',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lecons', to='core.niveauscolaire'),
        ),
    ]

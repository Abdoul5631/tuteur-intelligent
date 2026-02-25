# Cette migration ajoute les modèles IA et améliore les modèles existants
# Créée automatiquement en utilisant: python manage.py makemigrations

from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_utilisateur_date_inscription_and_more'),  # À ajuster selon votre dernière migration
    ]

    operations = [
        # 1. Créer le modèle Matière
        migrations.CreateModel(
            name='Matiere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(choices=[('mathematiques', 'Mathématiques'), ('francais', 'Français'), ('histoire_geo', 'Histoire-Géographie'), ('sciences', 'Sciences'), ('anglais', 'Anglais'), ('sciences_vie', 'Sciences de la Vie'), ('physique_chimie', 'Physique-Chimie'), ('technologie', 'Technologie'), ('eps', 'EPS'), ('arts', 'Arts Plastiques'), ('musique', 'Musique')], max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('couleur_hex', models.CharField(default='#3B82F6', max_length=7)),
                ('icone', models.CharField(default='📚', max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Matières',
            },
        ),

        # 2. Améliorer Utilisateur
        migrations.AddField(
            model_name='utilisateur',
            name='niveau_scolaire',
            field=models.CharField(choices=[('cp1', 'CP1'), ('cp2', 'CP2'), ('ce1', 'CE1'), ('ce2', 'CE2'), ('cm1', 'CM1'), ('cm2', 'CM2'), ('6eme', '6ème'), ('5eme', '5ème'), ('4eme', '4ème'), ('3eme', '3ème'), ('seconde', 'Seconde'), ('1ere', '1ère'), ('terminale', 'Terminale')], default='cp1', max_length=50),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='niveau_global',
            field=models.CharField(choices=[('débutant', 'Débutant'), ('intermédiaire', 'Intermédiaire'), ('avancé', 'Avancé')], default='débutant', max_length=50),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='matiere_principale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='utilisateurs_principaux', to='core.matiere'),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='style_apprentissage',
            field=models.CharField(blank=True, choices=[('visuel', 'Visuel'), ('auditif', 'Auditif'), ('kinesthesique', 'Kinesthésique'), ('lecture_ecriture', 'Lecture-Écriture')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='domaines_forts',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='domaines_faibles',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='total_exercices_completes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='score_moyen',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='temps_total_apprentissage',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='derniere_activite',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='date_modification',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='matieres_disponibles',
            field=models.ManyToManyField(blank=True, related_name='utilisateurs', to='core.matiere'),
        ),

        # 3. Améliorer Leçon
        migrations.AddField(
            model_name='lecon',
            name='matiere',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='lecons', to='core.matiere'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lecon',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='lecon',
            name='niveau_scolaire',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.RenameField(
            model_name='lecon',
            old_name='niveau',
            new_name='niveau_global',
        ),
        migrations.AddField(
            model_name='lecon',
            name='contenu_principal',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='lecon',
            name='contenu_simplifie',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='lecon',
            name='contenu_approfondi',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='lecon',
            name='image',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='lecon',
            name='video_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='lecon',
            name='concepts_cles',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='lecon',
            name='ordre',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='lecon',
            name='difficulte',
            field=models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AddField(
            model_name='lecon',
            name='temps_estime',
            field=models.IntegerField(default=20),
        ),
        migrations.AddField(
            model_name='lecon',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='lecon',
            name='date_modification',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='lecon',
            name='prerequis',
            field=models.ManyToManyField(blank=True, to='core.lecon'),
        ),

        # 4. Améliorer Exercice
        migrations.AddField(
            model_name='exercice',
            name='matiere',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='exercices', to='core.matiere'),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name='exercice',
            old_name='reponse',
            new_name='reponse_correcte',
        ),
        migrations.AddField(
            model_name='exercice',
            name='type_exercice',
            field=models.CharField(choices=[('choix_multiple', 'Choix Multiple'), ('reponse_courte', 'Réponse Courte'), ('redaction', 'Rédaction'), ('calcul', 'Calcul'), ('vrai_faux', 'Vrai/Faux'), ('matching', 'Appariement')], default='choix_multiple', max_length=50),
        ),
        migrations.AddField(
            model_name='exercice',
            name='options',
            field=models.JSONField(blank=True, default=list, help_text='Pour choix multiple'),
        ),
        migrations.AddField(
            model_name='exercice',
            name='erreurs_courantes',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='exercice',
            name='explication_bonne_reponse',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='exercice',
            name='explication_detaillee',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='exercice',
            name='solution_etape_par_etape',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='exercice',
            name='difficulte',
            field=models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AddField(
            model_name='exercice',
            name='points_valeur',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='exercice',
            name='temps_estime',
            field=models.IntegerField(default=300),
        ),
        migrations.AddField(
            model_name='exercice',
            name='concepts_evalues',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='exercice',
            name='ordre',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='exercice',
            name='actif',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='exercice',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='exercice',
            name='date_modification',
            field=models.DateTimeField(auto_now=True),
        ),

        # 5. Améliorer Résultat
        migrations.AddField(
            model_name='resultat',
            name='numero_tentative',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='resultat',
            name='temps_resolution',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='resultat',
            name='feedback_detaille',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='resultat',
            name='encouragement',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='resultat',
            name='analyse_erreur',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='resultat',
            name='suggestion_amelioration',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='resultat',
            name='score',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),

        # 6. Créer ConversationIA
        migrations.CreateModel(
            name='ConversationIA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(blank=True, max_length=200)),
                ('contexte', models.JSONField(blank=True, default=dict)),
                ('date_debut', models.DateTimeField(auto_now_add=True)),
                ('date_fin', models.DateTimeField(blank=True, null=True)),
                ('resume', models.TextField(blank=True)),
                ('points_cles_identifies', models.JSONField(blank=True, default=list)),
                ('nombre_messages', models.IntegerField(default=0)),
                ('tokens_utilises', models.IntegerField(default=0)),
                ('lecon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.lecon')),
                ('matiere', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.matiere')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations_ia', to='core.utilisateur')),
            ],
            options={
                'ordering': ['-date_debut'],
            },
        ),

        # 7. Créer ConversationMessage
        migrations.CreateModel(
            name='ConversationMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('user', 'Utilisateur'), ('assistant', 'Assistant IA')], max_length=50)),
                ('type_message', models.CharField(choices=[('question', 'Question'), ('explication', 'Explication'), ('exercice', 'Exercice'), ('feedback', 'Feedback'), ('encouragement', 'Encouragement'), ('autre', 'Autre')], default='autre', max_length=50)),
                ('contenu', models.TextField()),
                ('tokens', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='core.conversationia')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
    ]

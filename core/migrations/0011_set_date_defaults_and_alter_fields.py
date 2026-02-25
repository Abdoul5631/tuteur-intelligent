from django.db import migrations, models
import django.utils.timezone


def set_date_defaults(apps, schema_editor):
    Lecon = apps.get_model('core', 'Lecon')
    Exercice = apps.get_model('core', 'Exercice')
    Utilisateur = apps.get_model('core', 'Utilisateur')
    now = django.utils.timezone.now()
    Lecon.objects.filter(date_creation__isnull=True).update(date_creation=now)
    Exercice.objects.filter(date_creation__isnull=True).update(date_creation=now)
    Utilisateur.objects.filter(date_modification__isnull=True).update(date_modification=now)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_exercice_options_alter_lecon_options_and_more'),
    ]

    operations = [
        migrations.RunPython(set_date_defaults, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='lecon',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='exercice',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='date_modification',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_exercice_options_alter_lecon_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilisateur',
            name='niveau',
        ),
    ]
"""Empty no-op migration kept for repository cleanliness.

If this file originally contained important schema operations, restore
them from your version control history. This version avoids huge
duplicate import blocks and fixes editor/linter noise.
"""
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_remove_niveau_field"),
    ]

    operations = []

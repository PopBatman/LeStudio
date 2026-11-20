from django.db import migrations

from composition.catalogue_v1 import TITLES, manifest


def seed(apps, schema_editor):
    definitions = apps.get_model("composition", "ComponentVersion").objects.using(schema_editor.connection.alias)
    for key, label in TITLES.items():
        definitions.get_or_create(site=None, key=key, version=1, defaults={
            "label": label, "renderer": key, "manifest": manifest(key), "origin": "standard",
        })


class Migration(migrations.Migration):
    dependencies = [("composition", "0002_catalogue")]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]

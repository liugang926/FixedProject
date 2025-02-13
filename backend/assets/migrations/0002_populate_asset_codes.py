from django.db import migrations
import uuid

def generate_unique_code():
    return f"ASSET-{uuid.uuid4().hex[:8].upper()}"

def populate_asset_codes(apps, schema_editor):
    Asset = apps.get_model('assets', 'Asset')
    db_alias = schema_editor.connection.alias
    for asset in Asset.objects.using(db_alias).filter(code=''):
        while True:
            code = generate_unique_code()
            if not Asset.objects.using(db_alias).filter(code=code).exists():
                asset.code = code
                asset.save()
                break

def reverse_code(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('assets', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_asset_codes, reverse_code),
    ]
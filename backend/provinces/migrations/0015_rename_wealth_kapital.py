from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('provinces', '0014_development_points'),
    ]

    operations = [
        migrations.RenameField(
            model_name='provinceresources',
            old_name='wealth',
            new_name='kapital',
        ),
    ]

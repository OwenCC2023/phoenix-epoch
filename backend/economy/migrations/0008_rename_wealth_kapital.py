from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('economy', '0007_control_pool_snapshot'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nationresourcepool',
            old_name='wealth',
            new_name='kapital',
        ),
    ]

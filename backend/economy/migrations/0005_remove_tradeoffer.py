from django.db import migrations


class Migration(migrations.Migration):
    """Drop the legacy TradeOffer model. Replaced by the route-based trade system."""

    dependencies = [
        ('economy', '0004_add_nation_happiness'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TradeOffer',
        ),
    ]

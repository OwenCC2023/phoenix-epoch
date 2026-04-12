from django.db import migrations


class Migration(migrations.Migration):
    """Drop the legacy TradeOffer model. Replaced by the route-based trade system."""

    dependencies = [
        ('economy', '0005_add_literacy_and_research_unlock'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TradeOffer',
        ),
    ]

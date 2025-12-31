from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ("siteui", "0012_alter_route_options_alter_operator_operator_name"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="route",
            unique_together=set(),
        ),
    ]

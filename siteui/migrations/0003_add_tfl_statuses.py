from django.db import migrations


def add_tfl_statuses(apps, schema_editor):
    ServiceStatusType = apps.get_model("siteui", "ServiceStatusType")

    statuses = [
        # GOOD SERVICE
        ("Good Service", "Service operating normally", "#00A000", 0),

        # MINOR DISRUPTION
        ("Minor Delays", "Minor delays on some services", "#FFD200", 1),
        ("Reduced Service", "Reduced service operating", "#FFD200", 1),
        ("Bus Service Changed", "Bus service operating with changes", "#FFD200", 1),

        # SEVERE DISRUPTION
        ("Severe Delays", "Severe delays on the service", "#DC241F", 2),
        ("Part Closure", "Service partly closed", "#DC241F", 2),
        ("Part Suspended", "Service partly suspended", "#DC241F", 2),

        # NO SERVICE
        ("Suspended", "Service suspended", "#000000", 3),
        ("No Service", "No service operating", "#000000", 3),
        ("Service Closed", "Service closed", "#000000", 3),
        ("Not Running", "Service not running", "#000000", 3),

        # PLANNED / INFORMATION
        ("Planned Closure", "Planned closure", "#003688", 4),
        ("Planned Work", "Planned work", "#003688", 4),
        ("Planned Engineering Work", "Planned engineering work", "#003688", 4),
        ("Special Service", "Special service", "#003688", 4),
        ("Information", "Service information", "#003688", 4),
    ]

    for name, description, colour, severity in statuses:
        ServiceStatusType.objects.get_or_create(
            name=name,
            defaults={
                "description": description,
                "colour_hex": colour,
                "severity": severity,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("siteui", "0002_servicestatustype_severity"),
    ]

    operations = [
        migrations.RunPython(add_tfl_statuses),
    ]

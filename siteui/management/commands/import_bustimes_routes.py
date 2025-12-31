import requests

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from siteui.models import Operator, Route, Mode


BUSTIMES_URL = "https://bustimes.org/api/services/"


class Command(BaseCommand):
    help = "Import routes from Bustimes.org into the local database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--operator-code",
            required=True,
            help="Bustimes operator code used by the API (e.g. FHAM)",
        )
        parser.add_argument(
            "--operator-slug",
            required=True,
            help="Bustimes operator slug stored in Operator.bustimes_slug (e.g. fham)",
        )

    def handle(self, *args, **options):
        operator_code = options["operator_code"]
        operator_slug = options["operator_slug"]

        operator = Operator.objects.filter(bustimes_slug=operator_slug).first()
        if not operator:
            self.stderr.write(
                self.style.ERROR(
                    f"Operator with bustimes_slug='{operator_slug}' not found"
                )
            )
            return

        response = requests.get(
            BUSTIMES_URL,
            params={"operator": operator_code},
            timeout=20,
        )
        response.raise_for_status()

        results = response.json().get("results", [])
        if not results:
            self.stderr.write(
                self.style.WARNING("Bustimes API returned no services")
            )
            return

        # Resolve / create bus mode once
        bus_mode, _ = Mode.objects.get_or_create(name="Bus")

        created = 0
        updated = 0

        for item in results:
            # Split description safely
            parts = [p.strip() for p in item["description"].split(" - ")]

            origin = parts[0]
            destination = parts[-1]
            via = " - ".join(parts[1:-1]) if len(parts) > 2 else ""

            route, was_created = Route.objects.update_or_create(
                bustimes_id=item["id"],
                defaults={
                    "service": item["line_name"],
                    "origin": origin,
                    "destination": destination,
                    "via": via,
                    "operator": operator,
                    "mode": bus_mode,
                },
            )

            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete for {operator.operator_name}: "
                f"{created} created, {updated} updated"
            )
        )

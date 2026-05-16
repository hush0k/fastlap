from django.core.management import BaseCommand

from apps.drivers.models import Driver


class Command(BaseCommand):
    help = "Seed Drivers data"

    def handle(self, *args, **kwargs) -> None:
        drivers = [
            {
                "first_name": "Max",
                "last_name": "Verstappen",
                "nationality": "NL",
                "number": 1,
                "is_active": True,
            },
            {
                "first_name": "Lewis",
                "last_name": "Hamilton",
                "nationality": "GB",
                "number": 44,
                "is_active": True,
            },
            {
                "first_name": "Charles",
                "last_name": "Leclerc",
                "nationality": "MC",
                "number": 16,
                "is_active": True,
            },
            {
                "first_name": "Lando",
                "last_name": "Norris",
                "nationality": "GB",
                "number": 4,
                "is_active": True,
            },
            {
                "first_name": "Carlos",
                "last_name": "Sainz",
                "nationality": "ES",
                "number": 55,
                "is_active": True,
            },
            {
                "first_name": "Fernando",
                "last_name": "Alonso",
                "nationality": "ES",
                "number": 14,
                "is_active": True,
            },
            {
                "first_name": "George",
                "last_name": "Russell",
                "nationality": "GB",
                "number": 63,
                "is_active": True,
            },
            {
                "first_name": "Sergio",
                "last_name": "Perez",
                "nationality": "MX",
                "number": 11,
                "is_active": True,
            },
        ]

        for data in drivers:
            Driver.objects.get_or_create(
                first_name=data["first_name"],
                last_name=data["last_name"],
                defaults=data,
            )

        self.stdout.write(self.style.SUCCESS("Successfully added Drivers"))

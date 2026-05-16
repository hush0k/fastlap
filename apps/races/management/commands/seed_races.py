from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.races.models import Race, Series


class Command(BaseCommand):
    help = "Seed races data"

    def handle(self, *args, **kwargs) -> None:
        series_data = [
            {"name": "Formula 1", "category": "car"},
            {"name": "MotoGP", "category": "moto"},
            {"name": "Le Mans", "category": "endurance"},
            {"name": "GT3 European Series", "category": "endurance"},
        ]

        series_objects = {}
        for data in series_data:
            s, _ = Series.objects.get_or_create(name=data["name"], defaults=data)
            series_objects[data["name"]] = s

        f1 = series_objects["Formula 1"]

        races = [
            {
                "name": "Bahrain Grand Prix",
                "round_number": 1,
                "scheduled_at": timezone.now(),
                "status": "finished",
                "watch_platform": "f1_tv",
                "laps_total": 57,
            },
            {
                "name": "Saudi Arabian Grand Prix",
                "round_number": 2,
                "scheduled_at": timezone.now(),
                "status": "finished",
                "watch_platform": "f1_tv",
                "laps_total": 50,
            },
            {
                "name": "Australian Grand Prix",
                "round_number": 3,
                "scheduled_at": timezone.now(),
                "status": "upcoming",
                "watch_platform": "f1_tv",
                "laps_total": 58,
            },
        ]

        for data in races:
            Race.objects.get_or_create(
                name=data["name"],
                defaults={**data, "series": f1},
            )

        self.stdout.write(self.style.SUCCESS("Races seeded successfully"))

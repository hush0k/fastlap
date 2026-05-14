from datetime import date

from django.core.management import BaseCommand

from apps.races.models import Series
from apps.tournaments.models import Tournament


class Command(BaseCommand):
    help = "Seed tournaments"

    def handle(self, *args, **kwargs) -> None:
        f1 = Series.objects.filter(name="Formula 1").first()
        if not f1:
            f1 = Series.objects.create(name="Formula 1")

        tournaments = [
            {
                "name": "Formula 1 World Championship 2024",
                "series": f1,
                "year": 2024,
                "status": "finished",
                "start_date": date(2024, 3, 2),
                "end_date": date(2024, 12, 8),
                "total_rounds": 24,
            },
            {
                "name": "Formula 1 World Championship 2025",
                "series": f1,
                "year": 2025,
                "status": "live",
                "start_date": date(2025, 3, 16),
                "end_date": date(2025, 12, 7),
                "total_rounds": 24,
            },
        ]

        for tournament in tournaments:
            t, _ = Tournament.objects.get_or_create(
                name=tournament["name"], defaults=tournament
            )

        self.stdout.write(self.style.SUCCESS("Successfully added Tournaments"))
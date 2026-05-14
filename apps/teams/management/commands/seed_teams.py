from django.core.management import BaseCommand

from apps.teams.models import Team


class Command(BaseCommand):
    help = "Seed team data"

    def handle(self, *args, **kwargs) ->None:
        teams = [
            {"name": "Red Bull Racing", "short_name": "RBR", "country": "AT", "founded_year": 2005},
            {"name": "Ferrari", "short_name": "FER", "country": "IT", "founded_year": 1950},
            {"name": "Mercedes", "short_name": "MER", "country": "DE", "founded_year": 2010},
            {"name": "McLaren", "short_name": "MCL", "country": "GB", "founded_year": 1966},
            {"name": "Aston Martin", "short_name": "AMR", "country": "GB", "founded_year": 2021},
            {"name": "Alpine", "short_name": "ALP", "country": "FR", "founded_year": 2021},
        ]

        for data in teams:
            Team.objects.get_or_create(
                short_name=data["name"],
                defaults=data
            )

        self.stdout.write(self.style.SUCCESS("Successfully added Teams"))
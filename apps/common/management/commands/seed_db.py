from django.core import management
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Seed database'

    def handle(self, *args, **kwargs) ->None:
        self.stdout.write("Seeding races and series...")
        management.call_command("seed_races")

        self.stdout.write("Seeding drivers...")
        management.call_command("seed_drivers")

        self.stdout.write("Seeding teams...")
        management.call_command("seed_teams")

        self.stdout.write("Seeding team staff...")
        management.call_command("seed_team_stuff")

        self.stdout.write("Seeding race tracks...")
        management.call_command("seed_race_tracks")

        self.stdout.write("Seeding tournaments...")
        management.call_command("seed_tournaments")

        self.stdout.write("Seeding news...")
        management.call_command("seed_news")

        self.stdout.write(self.style.SUCCESS('Seed database'))
from django.core.management import BaseCommand

from apps.race_tracks.models import Track


class Command(BaseCommand):
    help = "Seed race tracks"
    def handle(self, *args, **kwargs) ->None:
        tracks = [
            {"name": "Bahrain International Circuit", "country": "BH", "city": "Sakhir", "length_km": 5.41, "number_of_turns": 15, "timezone": "Asia/Bahrain"},
            {"name": "Jeddah Corniche Circuit", "country": "SA", "city": "Jeddah", "length_km": 6.17, "number_of_turns": 27, "timezone": "Asia/Riyadh"},
            {"name": "Albert Park Circuit", "country": "AU", "city": "Melbourne", "length_km": 5.28, "number_of_turns": 16, "timezone": "Australia/Melbourne"},
            {"name": "Monza Circuit", "country": "IT", "city": "Monza", "length_km": 5.79, "number_of_turns": 11, "timezone": "Europe/Rome"},
            {"name": "Circuit de Monaco", "country": "MC", "city": "Monaco", "length_km": 3.34, "number_of_turns": 19, "timezone": "Europe/Monaco"},
            {"name": "Silverstone Circuit", "country": "GB", "city": "Silverstone", "length_km": 5.89, "number_of_turns": 18, "timezone": "Europe/London"},
        ]

        for track in tracks:
            Track.objects.get_or_create(
                name=track["name"],
                defaults=track
            )

        self.stdout.write(self.style.SUCCESS("Seed race tracks"))

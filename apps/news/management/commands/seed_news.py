from datetime import timezone

from django.core.management import BaseCommand

from apps.news.models import Tag, Article
from apps.users.models import User


class Command(BaseCommand):
    help = 'Seed race tracks'
    def handle (self, *args, **kwargs)-> None:
        tags = ["F!", "Le Mans", "GT3", "MotoGP", "Endurance", "Car", "Motorcycle"]
        tag_objects = []
        for name in tags:
            t, _ = Tag.objects.get_or_create(name=name)
            tag_objects.append(t)

        author = User.objects.filter(is_staff=True).first()
        if not author:
            self.stdout.write(self.style.ERROR("Create a superuser first: python manage.py createsuperuser"))
            return

        articles = [
            {
                "name": "Verstappen dominates Bahrain Grand Prix",
                "content": "Max Verstappen delivered yet another masterclass performance at the Bahrain International Circuit, leading from start to finish to claim victory in the opening round of the Formula 1 World Championship. " * 5,
                "is_published": True,
                "published_at": timezone.now(),
            },
            {
                "name": "Hamilton joins Ferrari for 2025 season",
                "content": "In one of the most shocking moves in Formula 1 history, seven-time world champion Lewis Hamilton has confirmed he will join Scuderia Ferrari for the 2025 season, ending his long-standing partnership with Mercedes. " * 5,
                "is_published": True,
                "published_at": timezone.now(),
            },
            {
                "name": "Le Mans 2024 Preview: Who will take victory?",
                "content": "The 24 Hours of Le Mans is set to deliver another classic with a record number of entries and several manufacturers battling for overall honours at the famous Circuit de la Sarthe this weekend. " * 5,
                "is_published": True,
                "published_at": timezone.now(),
            },
        ]

        for data in articles:
            article, created = Article.objects.get_or_create(
                name=data["name"],
                defaults={**data, "author": author},
            )
            if created:
                article.tags.set(tag_objects[:2])

        self.stdout.write(self.style.SUCCESS("Seed race tracks"))
"""
Management command to seed news articles.
"""

# Django modules
from django.core.management import BaseCommand
from django.utils import timezone

# Project modules
from apps.news.models import Article, Tag
from apps.users.models import User


class Command(BaseCommand):
    """
    Seed news articles with tags and author.
    """
    
    help = "Seed news articles"
    
    def handle(self, *args, **options) -> None:
        """
        Main method to seed news data.
        """
        tags = ["F1", "Le Mans", "GT3", "MotoGP", "Endurance", "Car", "Motorcycle"]
        tag_objects = []
        
        for name in tags:
            t, created = Tag.objects.get_or_create(name=name)
            tag_objects.append(t)
            if created:
                self.stdout.write(f"  Created tag: {name}")
        
        author = User.objects.filter(is_staff=True).first()
        
        if not author:
            self.stdout.write(
                self.style.ERROR("Create a superuser first: python manage.py createsuperuser")
            )
            return
        
        self.stdout.write(f"Using author: {author.email}")
        
        articles = [
            {
                "name": "Verstappen dominates Bahrain Grand Prix",
                "content": "Max Verstappen delivered yet another masterclass performance at the Bahrain International Circuit, leading from start to finish to claim victory in the opening round of the Formula 1 World Championship. " * 5,
                "is_published": True,
                "published_at": timezone.now(),
                "tags": ["F1", "Car"],
            },
            {
                "name": "Hamilton joins Ferrari for 2025 season",
                "content": "In one of the most shocking moves in Formula 1 history, seven-time world champion Lewis Hamilton has confirmed he will join Scuderia Ferrari for the 2025 season, ending his long-standing partnership with Mercedes. " * 5,
                "is_published": True,
                "published_at": timezone.now(),
                "tags": ["F1", "Car"],
            },
            {
                "name": "Le Mans 2024 Preview: Who will take victory?",
                "content": "The 24 Hours of Le Mans is set to deliver another classic with a record number of entries and several manufacturers battling for overall honours at the famous Circuit de la Sarthe this weekend. " * 5,
                "is_published": True,
                "published_at": timezone.now(),
                "tags": ["Le Mans", "Endurance"],
            },
        ]
        
        created_count = 0
        existing_count = 0
        
        for data in articles:
            article, created = Article.objects.get_or_create(
                name=data["name"],
                defaults={
                    "content": data["content"],
                    "author": author,
                    "is_published": data["is_published"],
                    "published_at": data["published_at"],
                }
            )
            
            if created:
                created_count += 1
                tag_names = data.get("tags", [])
                for tag_name in tag_names:
                    tag = Tag.objects.filter(name=tag_name).first()
                    if tag:
                        article.tags.add(tag)
                self.stdout.write(f"  Created article: {article.name}")
            else:
                existing_count += 1
                self.stdout.write(f"  Already exists: {article.name}")
        
        self.stdout.write(self.style.SUCCESS(
            f"\nSuccessfully seeded news: {created_count} created, {existing_count} already existed"
        ))
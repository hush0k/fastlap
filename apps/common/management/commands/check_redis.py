"""
Management command to check Redis connection.
"""

# Django modules
from django.core.cache import cache
from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    Check Redis connection and perfomance.
    """

    help = "Check Redis connection and performance"

    def handle(self, *args, **options):
        self.stdout.write("Checking Redis connection...")

        try:
            cache.set("test_key", "test_value", timeout=10)

            value = cache.get("test_key")

            if value == "test_value":
                self.stdout.write(self.style.SUCCESS("Redis is working correctly"))

                cache.delete("test_key")
                self.stdout.write(self.style.SUCCESS("Redis delete working"))

            else:
                self.stdout.write(self.style.ERROR("Redis get/set failed"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Redis error: {e}"))

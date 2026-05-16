from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class RoleEnum(TextChoices):
    CONTENT_MANAGER = "ContentManager", _("Content Manager")
    AUTHOR = "Author", _("Author")


class SeriesCategoryEnum(TextChoices):
    CAR = "car", _("Car")
    MOTO = "moto", _("Moto")
    ENDURANCE = "endurance", _("Endurance")


class RaceStatusEnum(TextChoices):
    UPCOMING = "upcoming", _("Upcoming")
    LIVE = "live", _("Live")
    FINISHED = "finished", _("Finished")
    CANCELLED = "cancelled", _("Cancelled")


class WatchPlatformEnum(TextChoices):
    F1_TV = "f1_tv", _("F1 TV")
    YOUTUBE = "youtube", _("Youtube")
    TWITCH = "twitch", _("Twitch")
    DAZN = "dazn", _("Dazn")
    ESPN = "espn", _("ESPN")
    SKY_SPORTS = "sky_sports", _("Sky Sports")


class Currency(TextChoices):
    """
    Enum of popular currencies.

    Each member is a tuple of (code, verbose_name).
    Use `.code` to get the ISO 4217 currency code and `.verbose` for the human-readable name.
    """  # noqa: E501

    USD = ("USD", _("US Dollar"))
    EUR = ("EUR", _("Euro"))
    GBP = ("GBP", _("British Pound"))
    JPY = ("JPY", _("Japanese Yen"))
    CNY = ("CNY", _("Chinese Yuan"))
    KRW = ("KRW", _("South Korean Won"))
    RUB = ("RUB", _("Russian Ruble"))
    KZT = ("KZT", _("Kazakhstani Tenge"))
    CAD = ("CAD", _("Canadian Dollar"))
    AUD = ("AUD", _("Australian Dollar"))
    CHF = ("CHF", _("Swiss Franc"))
    SEK = ("SEK", _("Swedish Krona"))
    BRL = ("BRL", _("Brazilian Real"))
    INR = ("INR", _("Indian Rupee"))
    SGD = ("SGD", _("Singapore Dollar"))

    @property
    def code(self) -> str:
        return self.value[0]

    @property
    def verbose(self) -> str:
        return self.value[1]

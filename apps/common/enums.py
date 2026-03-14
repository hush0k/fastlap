from enum import StrEnum, Enum


class SeriesCategoryEnum(StrEnum):
    CAR = "car"
    MOTO = "moto"
    ENDURANCE = "endurance"


class RaceStatusEnum(StrEnum):
    UPCOMING = "upcoming"
    LIVE = "live"
    FINISHED = "finished"
    CANCELLED = "cancelled"


class WatchPlatformEnum(StrEnum):
    F1_TV = "f1_tv"
    YOUTUBE = "youtube"
    TWITCH = "twitch"
    DAZN = "dazn"
    ESPN = "espn"
    SKY_SPORTS = "sky_sports"


class Currency(Enum):
    """
    Enum of popular currencies.

    Each member is a tuple of (code, verbose_name).
    Use `.code` to get the ISO 4217 currency code and `.verbose` for the human-readable name.
    """

    USD = ("USD", "US Dollar")
    EUR = ("EUR", "Euro")
    GBP = ("GBP", "British Pound")
    JPY = ("JPY", "Japanese Yen")
    CNY = ("CNY", "Chinese Yuan")
    KRW = ("KRW", "South Korean Won")
    RUB = ("RUB", "Russian Ruble")
    KZT = ("KZT", "Kazakhstani Tenge")
    CAD = ("CAD", "Canadian Dollar")
    AUD = ("AUD", "Australian Dollar")
    CHF = ("CHF", "Swiss Franc")
    SEK = ("SEK", "Swedish Krona")
    BRL = ("BRL", "Brazilian Real")
    INR = ("INR", "Indian Rupee")
    SGD = ("SGD", "Singapore Dollar")

    @property
    def code(self) -> str:
        return self.value[0]

    @property
    def verbose(self) -> str:
        return self.value[1]

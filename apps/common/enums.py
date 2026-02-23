from enum import StrEnum


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

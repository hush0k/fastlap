from django.db.models import TextChoices


class DriverResultStatusEnum(TextChoices):
    FINISHED = "finished", "Finished"
    DNF = "dnf", "DNF"
    DNS = "dns", "DNS"
    DSQ = "dsq", "DSQ"

from django.db.models import TextChoices


class DriverResultsStatusEnum(TextChoices):
    FINISHED = "finished", "Finished"
    DNF = "dnf", "DNF"
    DNS = "dns", "DNS"
    DSQ = "dsq", "DSQ"

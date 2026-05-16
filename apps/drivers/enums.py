from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class DriverResultStatusEnum(TextChoices):
    FINISHED = "finished", _("Finished")
    DNF = "dnf", _("DNF")
    DNS = "dns", _("DNS")
    DSQ = "dsq", _("DSQ")

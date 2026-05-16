<<<<<<< HEAD
from django_countries.fields import CountryField

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.mixins import CreatedAtMixin, NameMixin, UpdatedAtMixin
=======
from autoslug import AutoSlugField
from django_countries.fields import CountryField

from django.db import models
from django.db.models import CharField

from apps.common.mixins import CreatedAtMixin, UpdatedAtMixin
>>>>>>> 0e6107e1c089943cbfda7566fea209a804af52ae


class Team(CreatedAtMixin, UpdatedAtMixin, models.Model):
    name: CharField = CharField(max_length=255, unique=True)
    slug: AutoSlugField = AutoSlugField(populate_from="name", unique=True, null=True, blank=True)
    short_name = models.CharField(max_length=10, unique=True)
    logo = models.ImageField(upload_to="teams/logos/", null=True, blank=True)
    banner = models.ImageField(upload_to="teams/banners/", null=True, blank=True)
    country = CountryField()
    founded_year = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)

    budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    budget_currency = models.CharField(max_length=3, blank=True, default="USD")
    main_sponsor = models.CharField(max_length=255, blank=True)
    secondary_sponsor = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")
        indexes = [
            models.Index(fields=["short_name"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.short_name})"


class TeamStandings(CreatedAtMixin, UpdatedAtMixin, models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="standings",
    )
    tournament = models.ForeignKey(
        "tournaments.Tournament",
        on_delete=models.CASCADE,
        related_name="team_standings",
    )
    points = models.PositiveIntegerField(default=0)
    position = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("team", "tournament")
        ordering = ["position"]
        verbose_name = _("Team Standing")
        verbose_name_plural = _("Team Standings")

    def __str__(self):
        return f"{self.team.short_name} - {self.tournament.name}: {self.points} pts"

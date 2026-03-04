from django.db import models

from apps.common.mixins import CreatedAtMixin, NameMixin, UpdatedAtMixin


class Team(CreatedAtMixin, UpdatedAtMixin, NameMixin):
    short_name = models.CharField(max_length=3)
    logo = models.ImageField(upload_to="team_logo")
    country = models.CharField(max_length=100, blank=True)
    founded_year = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)

    # --Finance fields--
    budget = models.PositiveIntegerField(null=True, blank=True)
    budget_currency = models.CharField(max_length=3, blank=True, default="USD")
    main_sponsor = models.CharField(max_length=255, blank=True)
    secondary_sponsor = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        indexes = [
            models.Index(fields=["short_name"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.short_name})"


class TeamStandings(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="standings")
    tournament = models.ForeignKey("tournaments.Tournament", on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    position = models.PositiveIntegerField(default=0, null=True, blank=True)
    wins = models.PositiveIntegerField(default=0)
    podiums = models.PositiveIntegerField(default=0)
    def_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("team", "tournament")
        ordering = ["position"]
        verbose_name = "Team Standing"
        verbose_name_plural = "Team Standings"

    def __str__(self):
        return "{} - {}: {} points".format(
            self.team.short_name, self.tournament.name, self.points
        )

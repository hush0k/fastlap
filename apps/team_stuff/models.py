from django.db import models

from apps.common.mixins import CreatedAtMixin, NameMixin, UpdatedAtMixin


class TeamStuff(CreatedAtMixin, UpdatedAtMixin, NameMixin, models.Model):
    fist_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    in_team_sincAe = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Team Stuff"
        verbose_name_plural = "Team Stuffs"

    def __str__(self):
        return f"{self.fist_name} {self.last_name}"


class TeamRoster(models.Model):
    team = models.ForeignKey(
        "teams.Team", on_delete=models.CASCADE, related_name="roster"
    )
    stuff = models.ForeignKey(TeamStuff, on_delete=models.CASCADE, related_name="teams")
    start_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("team", "stuff", "start_date")
        ordering = ["start_date"]
        verbose_name = "Team Roster"
        verbose_name_plural = "Team Rosters"

    def __str__(self):
        return f"{self.team.short_name} - {self.stuff.fist_name} {self.stuff.last_name}"

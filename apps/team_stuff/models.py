# apps/team_stuff/models.py

from django.db import models
from django_countries.fields import CountryField

from apps.common.mixins import UpdatedAtMixin, CreatedAtMixin, NameMixin
from apps.common.models import BaseModel


class StaffMember(UpdatedAtMixin, CreatedAtMixin, NameMixin, models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    country = CountryField(blank=True)
    role = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="staff/photos/", null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "Staff Member"
        verbose_name_plural = "Staff Members"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class TeamRoster(CreatedAtMixin, UpdatedAtMixin, NameMixin, models.Model):
    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.CASCADE,
        related_name="roster",
    )
    staff_member = models.ForeignKey(
        StaffMember,
        on_delete=models.CASCADE,
        related_name="rosters",
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("team", "staff_member", "start_date")
        ordering = ["-start_date"]
        verbose_name = "Team Roster"
        verbose_name_plural = "Team Rosters"

    def __str__(self):
        return f"{self.team.short_name} — {self.staff_member.full_name}"

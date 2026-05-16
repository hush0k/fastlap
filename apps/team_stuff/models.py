from django_countries.fields import CountryField

from django.db import models

from apps.common.mixins import CreatedAtMixin, NameMixin, UpdatedAtMixin
from apps.common.utils import get_image_size_validator
from config.settings.base import STAFF_MEMBER_PHOTO_VALIDATOR_BYTES

staff_member_photo_validator = get_image_size_validator(
    STAFF_MEMBER_PHOTO_VALIDATOR_BYTES
)


class StaffMember(UpdatedAtMixin, CreatedAtMixin, NameMixin, models.Model):
    first_name: models.CharField = models.CharField(max_length=100)
    last_name: models.CharField = models.CharField(max_length=100)
    age: models.PositiveSmallIntegerField = models.PositiveSmallIntegerField(
        null=True, blank=True
    )
    country: CountryField = CountryField(blank=True)
    role: models.CharField = models.CharField(max_length=100, blank=True)
    description: models.TextField = models.TextField(blank=True)
    photo: models.ImageField = models.ImageField(
        upload_to="staff/photos/",
        null=True,
        blank=True,
        validators=[staff_member_photo_validator],
    )

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "Staff Member"
        verbose_name_plural = "Staff Members"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class TeamRoster(CreatedAtMixin, UpdatedAtMixin, NameMixin, models.Model):
    team: models.ForeignKey = models.ForeignKey(
        "teams.Team",
        on_delete=models.CASCADE,
        related_name="roster",
    )
    staff_member: models.ForeignKey = models.ForeignKey(
        StaffMember,
        on_delete=models.CASCADE,
        related_name="rosters",
    )
    start_date: models.DateField = models.DateField(null=True, blank=True)
    end_date: models.DateField = models.DateField(null=True, blank=True)
    is_active: models.BooleanField = models.BooleanField(default=True)

    class Meta:
        unique_together = ("team", "staff_member", "start_date")
        ordering = ["-start_date"]
        verbose_name = "Team Roster"
        verbose_name_plural = "Team Rosters"

    def __str__(self) -> str:
        return f"{self.team.short_name} — {self.staff_member.full_name}"

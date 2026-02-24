from django.db import models

from apps.common.mixins import CreatedAtMixin, UpdatedAtMixin, NameMixin


class TeamStuff(CreatedAtMixin, UpdatedAtMixin, ):
    fist_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    in_team_since = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Team Stuff'
        verbose_name_plural = 'Team Stuffs'

    def __str__(self):
        return '{} {}'.format(self.fist_name, self.last_name)


class TeamRoster(models.Model):
    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE, related_name='roster')
    stuff = models.ForeignKey(TeamStuff, on_delete=models.CASCADE, related_name='teams')


    class Meta:
        unique_together = ('team', 'stuff', 'start_date')
        ordering = ['start_date']
        verbose_name = 'Team Roster'
        verbose_name_plural = 'Team Rosters'

    def __str__(self):
        return '{} - {} {}'.format(self.team.short_name, self.stuff.fist_name, self.stuff.last_name)


class DriverRoster(models.Model):
    class Role(models.TextChoices):
        DRIVER = 'DRIVER', 'Driver'
        TEST_DRIVER = 'TEST_DRIVER', 'Test Driver'
        RESERVE_DRIVER = 'RESERVE_DRIVER', 'Reserve Driver'

    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE, related_name='driver_roster')
    driver = models.ForeignKey('drivers.Driver', on_delete=models.CASCADE, related_name='teams')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.DRIVER)
    joined_date = models.DateField(null=True, blank=True)
    left_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('team', 'driver')
        ordering = ['team']
        verbose_name = 'Driver Roster'
        verbose_name_plural = 'Driver Rosters'

    def __str__(self):
        return '{} - {} {}'.format(self.team.short_name, self.driver.fist_name, self.driver.last_name)

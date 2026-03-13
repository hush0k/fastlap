from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

  initial = True

  dependencies = [
    ("tournaments", "0001_initial"),
  ]

  operations = [
    migrations.CreateModel(
      name="Team",
      fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("created_at", models.DateTimeField(auto_now_add=True)),
        ("name", models.CharField(max_length=255)),
        ("slug", models.CharField(blank=True, max_length=50, null=True, unique=True)),
        ("updated_at", models.DateTimeField(auto_now=True)),
        ("short_name", models.CharField(max_length=10)),
        ("logo", models.ImageField(blank=True, null=True, upload_to="teams/logos/")),
        ("country", django_countries.fields.CountryField(blank=True, max_length=2)),
        ("founded_year", models.PositiveSmallIntegerField(blank=True, null=True)),
        ("description", models.TextField(blank=True)),
        ("budget", models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
        ("budget_currency", models.CharField(blank=True, default="USD", max_length=3)),
        ("main_sponsor", models.CharField(blank=True, max_length=255)),
        ("secondary_sponsor", models.CharField(blank=True, max_length=255)),
      ],
      options={
        "verbose_name": "Team",
        "verbose_name_plural": "Teams",
        "ordering": ["name"],
      },
    ),
    migrations.CreateModel(
      name="TeamStandings",
      fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("created_at", models.DateTimeField(auto_now_add=True)),
        ("updated_at", models.DateTimeField(auto_now=True)),
        ("points", models.PositiveIntegerField(default=0)),
        ("position", models.PositiveIntegerField(blank=True, null=True)),
        ("team", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="standings", to="teams.team")),
        ("tournament", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="team_standings", to="tournaments.tournament")),
      ],
      options={
        "verbose_name": "Team Standing",
        "verbose_name_plural": "Team Standings",
        "ordering": ["position"],
        "unique_together": {("team", "tournament")},
      },
    ),
    migrations.AddIndex(
      model_name="team",
      index=models.Index(fields=["short_name"], name="teams_team_short_n_8f8c2f_idx"),
    ),
  ]

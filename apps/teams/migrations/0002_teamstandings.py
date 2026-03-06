import autoslug.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
        ('tournaments', '0007_alter_tournament_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamStandings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(blank=True, editable=False, null=True, populate_from='name', unique=True)),
                ('points', models.PositiveIntegerField(default=0)),
                ('position', models.PositiveIntegerField(blank=True, null=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='standings', to='teams.team')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_standings', to='tournaments.tournament')),
            ],
            options={
                'verbose_name': 'Team Standing',
                'verbose_name_plural': 'Team Standings',
                'ordering': ['position'],
                'unique_together': {('team', 'tournament')},
            },
        ),
    ]

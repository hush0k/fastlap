import autoslug.fields
import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(blank=True, editable=False, null=True, populate_from='name', unique=True)),
                ('short_name', models.CharField(max_length=10)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='teams/logos/')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('founded_year', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('budget', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('budget_currency', models.CharField(blank=True, default='USD', max_length=3)),
                ('main_sponsor', models.CharField(blank=True, max_length=255)),
                ('secondary_sponsor', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Team',
                'verbose_name_plural': 'Teams',
                'ordering': ['name'],
                'indexes': [models.Index(fields=['short_name'], name='teams_team_short_n_eadde9_idx')],
            },
        ),
    ]

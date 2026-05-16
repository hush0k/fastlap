from datetime import date

from django.core.management import BaseCommand

from apps.team_stuff.models import StaffMember, TeamRoster
from apps.teams.models import Team


class Command(BaseCommand):
    help = "Seed team stuff"

    def handle(self, *args, **kwargs) -> None:
        team_stuff = [
            {
                "first_name": "Christian",
                "last_name": "Horner",
                "country": "GB",
                "role": "Team Principal",
            },
            {
                "first_name": "Toto",
                "last_name": "Wolff",
                "country": "AT",
                "role": "Team Principal",
            },
            {
                "first_name": "Frederic",
                "last_name": "Vasseur",
                "country": "FR",
                "role": "Team Principal",
            },
            {
                "first_name": "Adrian",
                "last_name": "Newey",
                "country": "GB",
                "role": "Chief Technical Officer",
            },
        ]
        stuff_objects = []
        for data in team_stuff:
            s, _ = StaffMember.objects.get_or_create(
                first_name=data["first_name"],
                last_name=data["last_name"],
                defaults=data,
            )
            stuff_objects.append(s)

        rbr = Team.objects.filter(short_name="RBR").first()
        mer = Team.objects.filter(short_name="MER").first()
        fer = Team.objects.filter(short_name="FER").first()

        if rbr and stuff_objects:
            TeamRoster.objects.get_or_create(
                team=rbr,
                staff_member=stuff_objects[0],
                start_date=date(2005, 1, 1),
                defaults={"is_active": True},
            )

        if mer and len(stuff_objects) > 1:
            TeamRoster.objects.get_or_create(
                team=mer,
                staff_member=stuff_objects[1],
                start_date=date(2010, 1, 1),
                defaults={"is_active": True},
            )

        self.stdout.write(self.style.SUCCESS("Successfully Seed Team Stuff"))

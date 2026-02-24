from django.db import migrations


def create_author_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    group, _ = Group.objects.get_or_create(name="Author")
    permissions = Permission.objects.filter(
        codename__in=[
            "add_article",
            "change_article",
            "delete_article",
        ]
    )
    group.permissions.set(permissions)


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_author_group),
    ]

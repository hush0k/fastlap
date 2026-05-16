import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


app.conf.beat_schedule = {
    "send-stat-every-1-hour": {
        "task": "apps.common.tasks.send_stat_to_admin",
        "schedule": 3600.0,
    },
}

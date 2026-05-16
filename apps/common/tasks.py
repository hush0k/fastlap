from django.core.mail import send_mail
from celery import shared_task
from config.settings.base import ADMIN_EMAIL, EMAIL_HOST
import psutil
from typing import Any


def bytes_to_gb(b):
    return round(b / (1024 ** 3), 2)


@shared_task
def send_stat_to_admin(*args: Any) -> None:
    disk = psutil.disk_usage('/')
    memory = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)

    message = (
        f"Disk: {bytes_to_gb(disk.used)}GB / {bytes_to_gb(disk.total)}GB ({disk.percent}%)\n"
        f"Memory: {bytes_to_gb(memory.used)}GB / {bytes_to_gb(memory.total)}GB ({memory.percent}%)\n"
        f"CPU: {cpu}%"
    )

    send_mail(
        "Server Stats",
        message,
        EMAIL_HOST,
        [ADMIN_EMAIL],
        fail_silently=False,
    )

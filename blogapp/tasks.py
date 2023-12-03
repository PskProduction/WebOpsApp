from celery import shared_task
from django.core.management import call_command


@shared_task
def perform_regular_task():
    call_command("dumpdata", "--output=data_backup.json")

from celery import shared_task
from celery import Celery
from celery.schedules import crontab

app = Celery()

@shared_task(Build=True)
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(
        crontab(hour=0, minute=0, day_of_week=7),
    )
from celery import Celery
from celery.schedules import crontab

from src.config import settings

app = Celery(
    "tasks", broker=settings.REDIS.URL, backend=settings.REDIS.URL
)
app.conf.update(
    timezone="Asia/Omsk",
    enable_utc=True,
)


def setup_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(
        crontab(hour=23, minute=52, day_of_week=0),
        sender.signature("src.tasks.cleanup.delete_unlinked_files"),
    )


app.on_after_configure.connect(setup_periodic_tasks)  # type: ignore

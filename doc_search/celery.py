import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doc_search.settings")
app = Celery("doc_search")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour="0", minute="0"),
        reset_all_users_keys,
        name="reset all keys",
    )


@app.task()
def reset_all_users_keys():
    from app.models import UserKeys

    UserKeys.objects.update(queries_limit=0, documents_limit=0)

import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doc_search.settings")
app = Celery("doc_search")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phoenix_epoch.settings.dev")

app = Celery("phoenix_epoch")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

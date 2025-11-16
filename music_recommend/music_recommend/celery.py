# music_recommend/celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_recommend.settings")

app = Celery("music_recommend")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

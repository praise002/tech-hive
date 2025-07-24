import os
from celery import Celery
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'clothing_store.settings.{config("SETTINGS")}')

app = Celery('tech_hive')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

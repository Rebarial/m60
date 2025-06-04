import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'm60.settings')

app = Celery('m60')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
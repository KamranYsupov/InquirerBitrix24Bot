import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.core.settings')

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.timezone = 'Europe/Moscow'

app.conf.beat_schedule = {
    'cleanup-old-tasks': {
        'task': 'web.apps.bitrix24.tasks.cleanup_old_tasks',
        'schedule': settings.AUTO_CLEAN_TASKS_SCHEDULE_SECONDS,
    },

}

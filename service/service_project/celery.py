import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service_project.settings")
app = Celery("service_project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'every': {
        'task': 'notification.tasks.check_send',
        'schedule': crontab(minute=0, hour='*/1'),# выполняет каждый час
    },

}


from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# définir l'environnement de configuration de Django pour Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movcom.settings')

app = Celery('movcom')

# Charger les configurations depuis les settings Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks dans toutes les applications installées
app.autodiscover_tasks()

# Configuration de Celery Beat
app.conf.beat_schedule = {
    'run-kmeans-every-5-minutes': {
        'task': 'recommendations.tasks.train_kmeans',
        'schedule': crontab(minute='*/5'),  # Exécute la tâche toutes les 5 minutes
    },
}

@app.task
def debug_task():
    print("Task is scheduled!")
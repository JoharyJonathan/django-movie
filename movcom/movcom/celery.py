from __future__ import absolute_import
import os
from celery import Celery

# définir l'environnement de configuration de Django pour Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movcom.settings')

app = Celery('movcom')

# Charger les configurations depuis les settings Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks dans toutes les applications installées
app.autodiscover_tasks()
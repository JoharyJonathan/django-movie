from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserMovieInteraction
from .tasks import train_kmeans

@receiver(post_save, sender=UserMovieInteraction)
def trigger_recommendation(sender, instance, **kwargs):
    train_kmeans.delay()  # Lancer la tâche d'entraînement en arrière-plan
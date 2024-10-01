from celery import shared_task
from sklearn.cluster import KMeans
from .models import UserMovieInteraction, UserCluster
from django.contrib.auth.models import User
import pandas as pd

@shared_task
def train_kmeans():
    # Extraire les données des interactions utilisateur
    interactions = UserMovieInteraction.objects.all()
    data = []

    for user in User.objects.all():
        # Simuler les données : ici on récupère juste les infos 'liked' et 'watched'
        user_data = [
            user.id,
            interactions.filter(user=user, watched=True).count(),
            interactions.filter(user=user, liked=True).count()
        ]
        data.append(user_data)
    
    df = pd.DataFrame(data, columns=['user_id', 'watched', 'liked'])
    
    # Appliquer K-Means
    kmeans = KMeans(n_clusters=5)
    df['cluster'] = kmeans.fit_predict(df[['watched', 'liked']])
    
    # Mettre à jour le cluster après K-Means
    for user_id, cluster in zip(df['user_id'], df['cluster']):
        UserCluster.objects.update_or_create(
            user_id=user_id,
            defaults={'cluster': cluster}
        )
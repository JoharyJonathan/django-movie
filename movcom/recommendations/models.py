from django.db import models
from movies.models import Movie, WatchHistory
from favorites.models import Favorite
from django.contrib.auth.models import User

# Create your models here.
class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='recommended_to')
    recommended_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255, blank=True, null=True)
    score = models.FloatField(default=0, help_text="Score based by the algorythm of recommendation")
    is_watched = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"Recommendation for {self.user.username} - {self.movie.title} (Score: {self.score})"
    
class UserMovieInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    liked = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        self.watched = WatchHistory.objects.filter(user=self.user, movie=self.movie).exists()
        
        self.liked = Favorite.objects.filter(user=self.user, movie=self.movie).exists()
        
        super(UserMovieInteraction, self).save(*args, **kwargs)

class UserCluster(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cluster = models.IntegerField()

    def __str__(self):
        return f"User {self.user.username} is in cluster {self.cluster}"
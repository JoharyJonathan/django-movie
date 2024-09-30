from django.db import models
from movies.models import Movie
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
    rating = models.IntegerField(null=True, blank=True)
    is_favorite = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'Revommendation for {self.user.username}: {self.movie.title}'
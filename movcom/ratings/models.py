from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie

# Create your models here
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField()
    
    class Meta:
        unique_together = ('user', 'movie')
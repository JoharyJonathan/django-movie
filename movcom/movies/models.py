from django.db import models

# Create your models here.
class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Genre(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    synopsys = models.TextField(blank=True, null=True)
    release_year = models.IntegerField()
    director = models.CharField(max_length=255)
    actors = models.ManyToManyField(Actor, related_name='movies')
    poster = models.ImageField(upload_to='movie_posters/', blank=True, null=True)
    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class MovieGenres(models.Model):
    movie = models.ForeignKey(Movie, related_name='movie_genres', on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, related_name='movie_genres', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('movie', 'genre')
        
    def __str__(self):
        return f"{self.movie.title} - {self.genre.name}"
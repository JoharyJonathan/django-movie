from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from movies.models import Movie
from .models import Rating

# Create your views here.
def add_rating(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    user = request.user
    user_rating = int(request.POST.get('rating'))
    
    # Check if the user has already rate this movie
    rating_obj, created = Rating.objects.update_or_create(
        user=user,
        movie=movie,
        defaults={'rating', user_rating}
    )
    
    # re-calculate the average of the rating
    new_avg_rating = Rating.objects.filter(movie=movie).aggregate(Avg('rating'))['rating__avg']
    movie.rating = new_avg_rating
    movie.save()
    
    return redirect('movie_detail', movie_id=movie.id)
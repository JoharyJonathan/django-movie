from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Favorite
from movies.models import Movie

# Create your views here.
@login_required
def toggle_favorite(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, movie=movie)

    if not created:
        # If the favorite already exists, remove it
        favorite.delete()
    return redirect('movie-detail', id=movie_id)
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
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

@login_required
def favorite_movies(request):
    favoris = Favorite.objects.filter(user=request.user).select_related('movie').order_by('id')
    nb_favoris = favoris.count()
    
    # Pagination
    paginator = Paginator(favoris, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'favorites': favoris,
        'nb_favoris': nb_favoris,
        'page_obj': page_obj
    }
    
    return render(request, 'movies/favorites.html', context)

from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Favorite

@login_required
def search_movies(request):
    query = request.GET.get('query', '')
    user_favorites = Favorite.objects.filter(user=request.user).select_related('movie')
    
    if query:
        movies = user_favorites.filter(movie__title__icontains=query)
    else:
        movies = user_favorites.none()
    
    # Ajouter l'URL des détails du film dans le résultat JSON
    results = [
        {
            'id': fav.movie.id,
            'title': fav.movie.title,
            'poster_url': fav.movie.poster.url,
            'detail_url': reverse('movie-detail', args=[fav.movie.id])  # Générer l'URL du détail
        } 
        for fav in movies
    ]
    
    return JsonResponse({'movies': results})
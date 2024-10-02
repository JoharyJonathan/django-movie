from django.shortcuts import render
from django.core.paginator import Paginator
from .models import UserCluster, UserMovieInteraction
from movies.models import Movie
from favorites.models import Favorite

# Create your views here.
def add_movie_interaction(user, movie):
    # Recuperer ou creer une nouvelle interaction
    interaction, created = UserMovieInteraction.objects.get_or_create(
        user=user,
        movie=movie
    )
    
    # Mettre a jour ou creer une nouvelle interaction
    interaction.watched = True,
    interaction.liked = Favorite.objects.filter(user=user, movie=movie).exists()
    interaction.save()
    
    return interaction

def recommend_movies(request):
    user_cluster = UserCluster.objects.get(user=request.user)
    
    # Trouver les autres utilisateurs dans le même cluster
    similar_users = UserCluster.objects.filter(cluster=user_cluster.cluster).exclude(user=request.user)
    
    # Recommander des films regardés par les autres utilisateurs du même cluster
    recommended_movies = Movie.objects.filter(usermovieinteraction__user__in=[u.user for u in similar_users]).distinct().order_by('id')
    
    paginator = Paginator(recommended_movies, 6)
    page_number = request.GET.get('page')
    recommended_movies = paginator.get_page(page_number)
    
    return render(request, 'recommendations/recommendations.html', {'recommended_movies': recommended_movies})
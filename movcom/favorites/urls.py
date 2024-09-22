from django.urls import path
from . import views

urlpatterns = [
    path('toggle-favorites/<int:movie_id>/', views.toggle_favorite, name='toggle-favorite'),
    path('favorites/', views.favorite_movies, name='favorites-movies'),
    path('search-movies/', views.search_movies, name='search-movies'),
]

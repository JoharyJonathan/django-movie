from django.urls import path
from . import views

urlpatterns = [
    path('ad/actors/', views.actor_list, name='actor_list'),
    path('ad/actors/new/', views.actor_create, name='actor_create'),
    path('ad/<int:pk>/edit/', views.actor_update, name='actor_update'),
    path('ad/actors/<int:pk>/delete/', views.actor_delete, name='actor_delete'),
    path('ad/actors/delete-multiple/', views.actor_delete_multiple, name='actor_delete_multiple'),
    path('ad/genres/new/', views.genre_create, name='genre_create'),
    path('ad/genres/', views.genre_list, name='genre_list'),
    path('ad/genres/<int:pk>/edit/', views.genre_update, name='genre_update'),
    path('ad/genres/<int:pk>/delete/', views.genre_delete, name='genre_delete'),
    path('ad/genres/delete-multiple/', views.genre_delete_multiple, name='genre_delete_multiple'),
    path('ad/movies/new/', views.movie_create, name='movie_create'),
    path('ad/movies/', views.movie_list, name='movie_list'),
    path('ad/movies/<int:pk>/edit/', views.movie_update, name='movie_update'),
    path('ad/movies/<int:pk>/delete/', views.movie_delete, name='movie_delete'),
    path('ad/movies/search/', views.search_movie, name='search_movie'),
    path('list/', views.movie, name='movie'),
    path('detail/<int:id>/', views.movie_detail, name='movie-detail'),
    path('genre/<int:genre_id>/', views.movie_by_genre, name='movie_by_genre'),
    path('genre-list/', views.genre, name='genre-list'),
    path('actor-list/', views.actors, name='actor-list'),
    path('actor/<int:actor_id>/', views.movie_by_actor, name='movie_by_actor'),
    path('ajax/search/', views.ajax_movie_search, name='ajax_movie_search'),
    path('watch-history/', views.watch_history, name='watch_history'),
    path('detete-history/<int:movie_id>/', views.delete_watch_history, name='delete_watch_history'),
]

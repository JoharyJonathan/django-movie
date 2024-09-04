from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('ad/actors/', views.actor_list, name='actor_list'),
    path('ad/actors/new/', views.actor_create, name='actor_create'),
    path('ad/<int:pk>/edit/', views.actor_update, name='actor_update'),
    path('ad/actors/<int:pk>/delete/', views.actor_delete, name='actor_delete'),
    path('ad/genres/new/', views.genre_create, name='genre_create'),
    path('ad/genres/', views.genre_list, name='genre_list'),
    path('ad/genres/<int:pk>/edit/', views.genre_update, name='genre_update'),
    path('ad/genres/<int:pk>/delete/', views.genre_delete, name='genre_delete'),
    path('ad/movies/new/', views.movie_create, name='movie_create'),
    path('ad/movies/', views.movie_list, name='movie_list'),
    path('ad/movies/<int:pk>/edit/', views.movie_update, name='movie_update'),
    path('ad/movies/<int:pk>/delete/', views.movie_delete, name='movie_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

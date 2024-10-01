from django.urls import path
from .views import recommend_movies

urlpatterns = [
    path('recommend/', recommend_movies, name='recommend_movies'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('toggle-favorites/<int:movie_id>/', views.toggle_favorite, name='toggle-favorite'),
]

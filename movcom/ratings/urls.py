from django.urls import path
from . import views

urlpatterns = [
    path('add_rating/<int:movie_id>/', views.add_rating, name='add_rating'),
]

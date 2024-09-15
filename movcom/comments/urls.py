from django.urls import path
from . import views

urlpatterns = [
    path('comments/<int:movie_id>/', views.add_comment, name='add_comment'),
]

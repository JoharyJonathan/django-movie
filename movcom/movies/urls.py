from django.urls import path
from . import views

urlpatterns = [
    path('ad/actors/', views.actor_list, name='actor_list'),
    path('ad/actors/new/', views.actor_create, name='actor_create'),
    path('ad/<int:pk>/edit/', views.actor_update, name='actor_update'),
    path('ad/actors/<int:pk>/delete/', views.actor_delete, name='actor_delete'),
]

from django.urls import path
from .views import user_list, user_detail, add_user

urlpatterns = [
    path('users/', user_list, name='user-list'),
    path('users/detail/<int:user_id>/', user_detail, name='user-detail'),
    path('add-user/', add_user, name='add-user'),
]
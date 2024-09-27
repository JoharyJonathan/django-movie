from django.urls import path
from .views import user_list, user_detail, add_user, delete_user, export_users_to_excel

urlpatterns = [
    path('users/', user_list, name='user-list'),
    path('users/detail/<int:user_id>/', user_detail, name='user-detail'),
    path('add-user/', add_user, name='add-user'),
    path('delete-user/<int:user_id>/', delete_user, name='delete-user'),
    path('export-users/', export_users_to_excel, name='export-users'),
]
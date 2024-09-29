from django.urls import path
from .views import user_list, user_detail, add_user, delete_user, export_users_to_excel, calendar_history, calendar_view, change_user_status, edit_user, admin_comments_view

urlpatterns = [
    path('users/', user_list, name='user-list'),
    path('users/detail/<int:user_id>/', user_detail, name='user-detail'),
    path('add-user/', add_user, name='add-user'),
    path('edit-user/<int:user_id>/', edit_user, name='edit-user'),
    path('delete-user/<int:user_id>/', delete_user, name='delete-user'),
    path('export-users/', export_users_to_excel, name='export-users'),
    path('change-users-status/', change_user_status, name='change-user-status'),
    path('calendar/history/', calendar_history, name='calendar-history'),
    path('calendars/', calendar_view, name='calendars'),
    path('comments/', admin_comments_view, name='admin-comments'),
]
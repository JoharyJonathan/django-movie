from django.urls import path
from .views import admin_signup_view, login_view, logout_view, profile_view, update_profile

urlpatterns = [
    path('adminsign/', admin_signup_view, name='adminsign'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', update_profile, name='profile-update')
]
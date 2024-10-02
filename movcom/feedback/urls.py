from django.urls import path
from .views import submit_feedback

urlpatterns = [
    path('submit-feedback/', submit_feedback, name='feedback'),
]

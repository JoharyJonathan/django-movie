from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback
from django.contrib import messages

# Create your views here.
@login_required
def submit_feedback(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        message = request.POST.get('message')

        # Créer une nouvelle instance de feedback
        Feedback.objects.create(
            user=request.user,
            rating=rating,
            message=message
        )

        # Ajouter un message de succès
        messages.success(request, 'Thank you for your feedback!')
        return redirect('movie')

    return render(request, 'uses.html')
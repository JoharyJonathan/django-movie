from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import AdminSignUpForm, ProfileUpdateForm
from django.conf import settings
from admins.utils import create_admin

def admin_signup_view(request):
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            secret_key = form.cleaned_data.get('secret_key')
            if secret_key == settings.ADMIN_SECRET_KEY:
                # Récupérer les données du formulaire
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                email = form.cleaned_data.get('email')
                role_name = form.cleaned_data.get('role')  # Assuming there's a role field

                # Créer l'utilisateur admin via la fonction create_admin
                create_admin(username, raw_password, email, role_name)

                # Authentifier et connecter l'utilisateur
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                
                return redirect('home')
            else:
                form.add_error('secret_key', 'Clé secrète invalide.')
    else:
        form = AdminSignUpForm()
    return render(request, 'authenticate/signup.html', {'form': form})

def home_view(request):
    if request.user.is_authenticated:
        # Logique si l'utilisateur est connecté
        message = f"Bienvenue, {request.user.username}!"
    else:
        # Logique si l'utilisateur n'est pas connecté
        message = "Bienvenue, visiteur. Veuillez vous connecter."
        
    return render(request, 'authenticate/home.html', {'message': message})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'authenticate/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'authenticate/profile.html', {'user': user})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
        
    return render(request, 'authenticate/update_profile.html', {'form': form})
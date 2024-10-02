from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import make_password
import os
import pandas as pd
from movies.models import WatchHistory, Movie
from comments.models import Comment
from recommendations.models import UserMovieInteraction

# Create your views here.
def user_list(request):
    users = User.objects.all().order_by('id')
    paginator = Paginator(users, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admins/users.html', {'page_obj': page_obj})

def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    return render(request, 'admins/user-detail.html', {'user': user})

@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.FILES.get('first_name')  # Récupérer l'image depuis le champ `first_name`

        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'message': 'Username already exists'})

        # Gestion de l'image
        if image:
            # Créer le nom de fichier : username_nomImage.jpg
            image_extension = os.path.splitext(image.name)[1]  # Récupérer l'extension de l'image
            new_image_name = f"{username}_{image.name}"  # Format: username_nomImage.jpg

            # Chemin de sauvegarde : /media/profile_images/
            media_path = os.path.join('profile_images')  # Chemin relatif sans `media/`
            full_media_path = os.path.join(settings.MEDIA_ROOT, media_path)  # Racine absolue du chemin

            # S'assurer que le dossier existe
            if not os.path.exists(full_media_path):
                os.makedirs(full_media_path)

            # Sauvegarder l'image
            fs = FileSystemStorage(location=full_media_path)
            filename = fs.save(new_image_name, image)
            
            # Construire le chemin relatif à sauvegarder dans la base de données
            uploaded_file_url = os.path.join(media_path, new_image_name)  # profile_images/username_nomImage.jpg
        else:
            uploaded_file_url = None

        # Créer le nouvel utilisateur
        user = User.objects.create(
            username=username,
            first_name=uploaded_file_url,  # Enregistrer le chemin relatif de l'image
            last_name=last_name,
            email=email,
            password=make_password(password)
        )

        return JsonResponse({'success': True, 'message': 'User added successfully!'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.FILES.get('image')

        # Check if username is already taken
        if User.objects.filter(username=username).exclude(id=user.id).exists():
            return JsonResponse({'success': False, 'message': 'Username already exists !'})

        # Manage Image
        if image:
            # Check image extension
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            image_extension = os.path.splitext(image.name)[1]  # extraction de l'extension
            if image_extension.lower() not in allowed_extensions:
                return JsonResponse({'success': False, 'message': 'Invalid image format. Please upload a JPEG, PNG, or GIF image.'})

            new_image_name = f"{username}_{image.name}"

            # Save File
            media_path = os.path.join('profile_images')
            full_media_path = os.path.join(settings.MEDIA_ROOT, media_path)

            # check if folder exists
            if not os.path.exists(full_media_path):
                os.makedirs(full_media_path)

            # Save image
            fs = FileSystemStorage(location=full_media_path)
            filename = fs.save(new_image_name, image)

            # Create file_path
            uploaded_file_url = os.path.join(media_path, new_image_name)
            user.first_name = uploaded_file_url

        # Update profile informations
        user.username = username
        user.last_name = lastname
        user.email = email

        # Change password if provided
        if password:
            user.password = make_password(password)  # Crypt password

        user.save()

        return JsonResponse({'success': True, 'message': 'User profile updated Successfully !'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.delete()
        return JsonResponse({'success': True})  # Réponse en JSON pour AJAX
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def export_users_to_excel(request):
    users = User.objects.all().values('username', 'first_name', 'last_name', 'email', 'date_joined')
        
    df = pd.DataFrame(users)
    
    if 'date_joined' in df.columns:
        df['date_joined'] = pd.to_datetime(df['date_joined']).dt.tz_localize(None)
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Diposition'] = 'attachement; filename=users.xlsx'
    
    df.to_excel(response, index=False)
    
    return response

@csrf_exempt
def change_user_status(request):
    if request.method == 'POST':
        user_id = request.POST.get('userId')
        is_active = request.POST.get('is_active') == 'true'
        
        # Update user status
        user = User.objects.get(id=user_id)
        user.is_active = is_active
        user.save()
        
        return JsonResponse({'success': True, 'message': 'User status updated successfully !'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})

def calendar_history(request):
    history = WatchHistory.objects.select_related('user', 'movie').all()
    
    events = []
    for record in history:
        events.append({
            'title': f"{record.user.username} watched {record.movie.title}",
            'start': record.watched_at.isoformat(),
            'color': '#FF5733',
        })
        
    return JsonResponse(events, safe=False)

def calendar_comments(request):
    comments = Comment.objects.select_related('user', 'movie').all()
    
    events = []
    for record in comments:
        events.append({
            'title': f"{record.user.username} commented {record.movie.title}",
            'start': record.created_at.isoformat(),
            'color': '#039BE5',
        })
        
    return JsonResponse(events, safe=False)

def combined_calendar_events(request):
    # Obtenir l'historique
    history = WatchHistory.objects.select_related('user', 'movie').all()
    events = []

    # Ajouter les événements d'historique
    for record in history:
        events.append({
            'title': f"{record.user.username} watched {record.movie.title}",
            'start': record.watched_at.isoformat(),
            'color': '#FF5733',
        })
        
    # Obtenir les commentaires
    comments = Comment.objects.select_related('user', 'movie').all()

    # Ajouter les événements de commentaires
    for record in comments:
        events.append({
            'title': f"{record.user.username} commented on {record.movie.title}",
            'start': record.created_at.isoformat(),
            'color': '#039BE5',
        })
        
    return JsonResponse(events, safe=False)

def calendar_view(request):
    return render(request, 'admins/calendars.html')

def admin_comments_view(request):
    comment_list = Comment.objects.select_related('movie', 'user').all()
    paginator = Paginator(comment_list, 10)
    
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)
    
    return render(request, 'admins/comments.html', {'comments': comments})

def traffic(request):
    users = User.objects.all().count()
    comments = Comment.objects.all().count()
    movies = Movie.objects.all().count()
    visits = UserMovieInteraction.objects.all().count()
    
    return render(request, 'admins/web-traffic.html', {'users': users, 'comments': comments, 'movies': movies, 'visits': visits})
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
from movies.models import WatchHistory

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

def calendar_view(request):
    return render(request, 'admins/calendars.html')
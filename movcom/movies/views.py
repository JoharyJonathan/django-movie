import os
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from .models import Actor, Genre, Movie, MovieGenres, WatchHistory
from .forms import ActorForm, GenreForm, MovieForm
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from favorites.models import Favorite

# Create your views here.
def actor_create(request):
    if request.method == 'POST':
        form = ActorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('actor_list')
    else:
        form = ActorForm()
        
    return render(request, 'actors/actor_form.html', {'form': form})
    
def actor_list(request):
    actors = Actor.objects.all().order_by('id')
    paginator = Paginator(actors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'actors/actor_list.html', {'actors': page_obj.object_list, 'page_obj': page_obj})

def actor_update(request, pk):
    actor = get_object_or_404(Actor, pk=pk)
    if request.method == 'POST':
        form = ActorForm(request.POST, instance=actor)
        if form.is_valid():
            form.save()
            return redirect('actor_list.html')
    else:
        form = ActorForm(instance=actor)
        
    return render(request, 'actors/actor_form.html', {'form': form})

def actor_delete(request, pk):
    actor = get_object_or_404(Actor, pk=pk)
    if request.method == 'POST':
        actor.delete()
        return redirect('actor_list')
    
    return render(request, 'actors/actor_confirm_delete.html', {'actor': actor})

def actor_delete_multiple(request):
    if request.method == 'POST':
        actor_ids = request.POST.getlist('selected_actors')
        if actor_ids:
            Actor.objects.filter(id__in=actor_ids).delete()
            messages.success(request, 'Actors deleted successfully.')
        else:
            messages.warning(request, 'No actors were selected for deletion.')
        return redirect('actor_list')
    
    return redirect('actor_list')

def genre_create(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('genre_list')
    else:
        form = GenreForm()
        
    return render(request, 'genres/genre_form.html', {'form': form})

def genre_list(request):
    genres = Genre.objects.all().order_by('id')
    paginator = Paginator(genres, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'genres/genre_list.html', {'genres': genres, 'page_obj': page_obj})

def genre_update(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    if request.method == 'POST':
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            return redirect('genre_list')
    else:
        form = GenreForm(instance=genre)
        
    return render(request, 'genres/genre_form.html', {'form': form})

def genre_delete(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    if request.method == 'POST':
        genre.delete()
        return redirect('genre_list')
    
    return render(request, 'genres/genre_confirm_delete.html', {'genre': genre})

def save_uploaded_image(file):
    # destination folder
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'movie_posters')
    os.makedirs(upload_dir, exist_ok=True)
    
    # create the file with date and time
    filename, ext = os.path.splitext(file.name)
    new_filename = f"{timezone.now().strftime('%Y%m%d%H%M%S')}_{filename}{ext}"
    
    # path for save the file
    file_path = os.path.join(upload_dir, new_filename)
    
    # Save the file in disk storage
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
            
    # return the stored path in poster_url field
    return f"movies_posters/{new_filename}"

def genre_delete_multiple(request):
    if request.method == 'POST':
        genre_ids = request.POST.getlist('genres_to_delete[]')
        if genre_ids:
            genres = get_list_or_404(Genre, id__in=genre_ids)
            for genre in genres:
                genre.delete()
                
        return redirect('genre_list')

def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.save()
            
            # Manage actors
            actors = form.cleaned_data.get('actors')
            if actors:
                movie.actors.set(actors)
            
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'movies/movie_form.html', {'form': form})

def movie_list(request):
    movies = Movie.objects.all().order_by('id')
    paginator = Paginator(movies, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'movies/movie_list.html', {'movies': movies, 'page_obj': page_obj})

def search_movie(request):
    query = request.GET.get('query', None)
    if query:
        # Effectue la recherche dans les films
        movies = Movie.objects.filter(title__icontains=query)
        results = [{'title': movie.title} for movie in movies]
        return JsonResponse({'movies': results}, safe=False)
    else:
        return JsonResponse({'movies': []}, safe=False)    

def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        
        if form.is_valid():
            movie = form.save(commit=False)
            
            # Vérifiez si une nouvelle image a été téléchargée
            if 'poster' in request.FILES:
                poster_file = request.FILES['poster']
                movie.poster_url = save_uploaded_image(poster_file)
            
            movie.save()  # Sauvegarder le film
            
            # Manage actors
            actors = form.cleaned_data.get('actors')
            if actors:
                movie.actors.set(actors)

            # Gestion des genres
            # Supprimer les anciennes associations
            MovieGenres.objects.filter(movie=movie).delete()

            # Associer les nouveaux genres
            genres = form.cleaned_data.get('genres')
            if genres:
                for genre in genres:
                    MovieGenres.objects.create(movie=movie, genre=genre)  # Associer chaque genre sélectionné au film
            
            return redirect('movie_list')  # Rediriger vers la liste des films après la mise à jour
        
    else:
        # Préremplir le formulaire avec les genres actuels du film
        initial_data = {
            'genres': movie.movie_genres.values_list('genre', flat=True)  # Pré-remplir avec les genres actuels
        }
        form = MovieForm(instance=movie, initial=initial_data)
    
    return render(request, 'movies/movie_form.html', {'form': form, 'movie': movie})

def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')
    
    return render(request, 'movies/movie_confirm_delete.html', {'movie': movie})

def movie(request):
    movies = Movie.objects.all()
    
    # paginate the view, 6 per pages
    paginator = Paginator(movies, 6)
    
    page_number = request.GET.get('page')
    movies = paginator.get_page(page_number)
    
    return render(request, 'movies/movie.html', {'movies': movies})

def movie_detail(request, id):
    movie = get_object_or_404(Movie, pk=id)
    genres = Genre.objects.all()
    comments = movie.comments.filter(parent__isnull=True)
    
    user_favorite = Favorite.objects.filter(user=request.user, movie=movie).exists()
    
    # Update history
    if request.user.is_authenticated:
        update_watch_history(request.user, movie.id)
    
    return render(request, 'movies/movie_detail.html', {'movie': movie, 'genres': genres ,'comments': comments, 'user_favorite': user_favorite})

def movie_by_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    movies = Movie.objects.filter(movie_genres__genre=genre)
    
    return render(request, 'movies/movies_by_genre.html', {'movies': movies, 'selected_genre': genre})

def genre(request):
    search_query = request.GET.get('search', '')
    genres_list = Genre.objects.all()
    paginator = Paginator(genres_list, 10)
    
    if search_query:
        # Filtrer les genres en fonction du terme de recherche
        genre = Genre.objects.filter(name__icontains=search_query).first()
        if genre:
            # Rediriger vers l'URL avec l'ID du genre
            return redirect('movie_by_genre', genre_id=genre.id)
    
    # Si aucun genre n'est trouvé ou si le terme de recherche est vide
    genres_list = Genre.objects.all()
    paginator = Paginator(genres_list, 10)  # 10 genres par page

    page = request.GET.get('page')
    try:
        genres = paginator.page(page)
    except PageNotAnInteger:
        genres = paginator.page(1)
    except EmptyPage:
        genres = paginator.page(paginator.num_pages)

    return render(request, 'genres/genres.html', {'genre': genres, 'genres_count': paginator.count, 'paginator': paginator, 'search_query': search_query})

def actors(request):
    actors_list = Actor.objects.all()
    search_query = request.GET.get('search', '')
    paginator = Paginator(actors_list, 10)
    
    page = request.GET.get('page')
    try:
        actors = paginator.page(page)
    except PageNotAnInteger:
        actors = paginator.page(1)
    except EmptyPage:
        actors = paginator.page(paginator.num_pages)
        
    return render(request, 'actors/actors.html', {'actor': actors, 'actors_count': paginator.count, 'search_query': search_query})

def movie_by_actor(request, actor_id):
    actor = get_object_or_404(Actor, id=actor_id)
    movies = Movie.objects.all()
    
    return render(request, 'movies/movies_by_actor.html', {'movies': movies, 'actor': actor})

def ajax_movie_search(request):
    query = request.GET.get('q')
    if query:
        movies = Movie.objects.filter(title__icontains=query)
        results = [{'id': movie.id, 'title': movie.title} for movie in movies]
    else:
        results = []
        
    return JsonResponse({'movies': results})

def watch_history(request):
    if request.user.is_authenticated:
        history = WatchHistory.objects.filter(user=request.user).order_by('-watched_at')
        
        return render(request, 'movies/watch_history.html', {'history': history})
    else:
        return redirect('login')
    
def update_watch_history(user, movie_id):
    movie = Movie.objects.get(id=movie_id)
    
    # Check if this movie is already existing in the user history
    existing_history = WatchHistory.objects.filter(user=user, movie=movie)
    
    # if exists then delete it
    if existing_history.exists():
        existing_history.delete()
        
    # Add new entry with updated timestamp
    WatchHistory.objects.create(user=user, movie=movie, watched_at=timezone.now())
    
@login_required
def delete_watch_history(request, movie_id):
    history_item = get_object_or_404(WatchHistory, user=request.user, movie_id=movie_id)
    history_item.delete()
    
    return redirect('watch_history')
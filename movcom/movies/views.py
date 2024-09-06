import os
from django.shortcuts import render, get_object_or_404, redirect
from .models import Actor, Genre, Movie, MovieGenres
from .forms import ActorForm, GenreForm, MovieForm
from django.utils import timezone
from django.conf import settings


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
    actors = Actor.objects.all()
    
    return render(request, 'actors/actor_list.html', {'actors': actors})

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
    genres = Genre.objects.all()
    return render(request, 'genres/genre_list.html', {'genres': genres})

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

def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            
            # Check if a file is uploaded
            if 'poster' in request.FILES:
                poster_file = request.FILES['poster']
                # Save file and get the path
                movie.poster_url = save_uploaded_image(poster_file)
                
            movie.save()
            return redirect('movie_list')
    else:
        form = MovieForm()
        
    return render(request, 'movies/movie_form.html', {'form': form})


def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        
        if form.is_valid():
            movie = form.save(commit=False)
            
            # Vérifiez si une nouvelle image a été téléchargée
            if 'poster' in request.FILES:
                poster_file = request.FILES['poster']
                movie.poster_url = save_uploaded_image(poster_file)
            
            movie.save()  # Sauvegarder le film

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
    
    return render(request, 'movies/movie.html', {'movies': movies})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    
    return render(request, 'movies/movie_detail.html', {'movie': movie})
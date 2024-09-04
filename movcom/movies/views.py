from django.shortcuts import render, get_object_or_404, redirect
from .models import Actor, Genre
from .forms import ActorForm, GenreForm

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
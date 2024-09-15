from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Comment
from movies.models import Movie
from .forms import CommentForm

# Create your views here.
@login_required
def add_comment(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.movie = movie
            new_comment.user = request.user
            new_comment.save()
            
            return redirect('movie-detail', movie_id=movie.id)
    else:
        form = CommentForm()
        
    return render(request, 'movies/movie_detail.html', {'movie': movie, 'form': form})
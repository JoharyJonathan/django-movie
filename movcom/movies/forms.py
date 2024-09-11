from typing import Any
from django import forms
from .models import Actor, Genre, Movie, MovieGenres

class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ['first_name', 'last_name', 'date_of_birth', 'bio']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        
class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name', 'description']
        
class MovieForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Movie
        fields = ['title', 'description', 'synopsys', 'release_year', 'director', 'actors', 'poster', 'rating']

    def save(self, commit=True):
        movie = super().save(commit=False)
        if commit:
            movie.save()
        # Handle genres
        movie_genres = self.cleaned_data['genres']
        MovieGenres.objects.filter(movie=movie).delete()
        for genre in movie_genres:
            MovieGenres.objects.create(movie=movie, genre=genre)
        return movie
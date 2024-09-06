from typing import Any
from django import forms
from .models import Actor, Genre, Movie, MovieGenres

class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ['first_name', 'last_name', 'date_of_birth']
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
        required=True
    )

    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_year', 'director', 'actors', 'rating']

    def save(self, commit=True):
        # Sauvegarder l'instance Movie sans encore toucher aux genres
        movie = super(MovieForm, self).save(commit=False)
        
        if commit:
            movie.save()  # Sauvegarder le film avant d'ajouter les genres
        
        # Supprimer les relations existantes dans MovieGenres
        MovieGenres.objects.filter(movie=movie).delete()
        
        # Créer de nouvelles associations pour les genres sélectionnés
        for genre in self.cleaned_data['genres']:
            MovieGenres.objects.create(movie=movie, genre=genre)
        
        return movie
from django import forms
from .models import Actor, Genre, Movie

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
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_year', 'director', 'actors', 'rating']
from django.contrib import admin
from .models import Actor, Genre, Movie, MovieGenres

# Register your models here.
class ActorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth')
    search_fields = ('first_name', 'last_name')
    
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'director', 'rating')
    search_fields = ('title', 'director')
    
admin.site.register(Actor, ActorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieGenres)
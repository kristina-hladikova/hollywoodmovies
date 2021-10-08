from django.contrib import admin

from hollymovies_app.models import Movie, Genre, Actor


class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', ]

class ActorAdmin(admin.ModelAdmin):
    list_display = ['name', ]

admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Actor, GenreAdmin)
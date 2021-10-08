from django.http import HttpResponse
from django.template.response import TemplateResponse

from hollymovies_app.models import Movie, Genre, Actor, GENRE_NAME_TO_NAME_SHORTCUT_MAPPING


def homepage(request):
    movies_db = Movie.objects.all().order_by('-likes', 'name')
    context = {
        'movies': movies_db,
        'horror_genre': Genre.HORROR,
        'comedy_genre': Genre.COMEDY,
    }
    return TemplateResponse(request, 'homepage.html', context=context)


def movie_detail(request, pk):
    movie = Movie.objects.get(id=pk)

    if request.method == 'POST':
        movie.likes += 1
        movie.save()

    context = {
        'movie': movie,
    }
    return TemplateResponse(request, 'detail/movie_detail.html', context=context)


def genre_detail(request, genre_name):
    genre_name_shortcut = GENRE_NAME_TO_NAME_SHORTCUT_MAPPING[genre_name]
    genre = Genre.objects.get(name=genre_name_shortcut)
    movies = genre.movies.filter(likes__gte=10)
    context = {
        'genre': genre,
        'movies': movies,
        'page_description': {
            'long_description': 'This is long description',
            'short_description': 'This is short description'
        },
        'creators': ['Jan', 'Pepa']
    }
    return TemplateResponse(request, 'detail/genre_detail.html', context=context)



def actor_detail(request, actor_name):
    pk = Actor.objects.get(name=actor_name).id
    actor = Actor.objects.get(id=pk)
    description = actor.description
    movies = actor.movies.all()

    context = {
        'actor': actor,
        'description': description,
        'movies': movies,

    }
    return TemplateResponse(request, 'detail/actor_detail.html', context=context)

def homepage_kristi(request):
    return HttpResponse('<h1>Hollymovies Homepage Kristi</h1>')
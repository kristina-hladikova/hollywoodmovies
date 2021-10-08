from django.urls import path

from hollymovies_app.views import homepage, movie_detail, genre_detail, actor_detail

urlpatterns = [
    path('homepage/', homepage, name='homepage'),
    path('movie/<int:pk>/', movie_detail, name='movie_detail'),
    path('genre/<str:genre_name>/', genre_detail, name='genre_detail'),
    path('actor/<str:actor_name>/', actor_detail, name='actor_detail')
]
from django.urls import path

from hollymovies_app.views import HomepageView, MovieDetailView, ResetMovieLikesView, ContactView, GenreDetailView, \
    ActorDetailView, CreateMovieView, CreateActorView, UpdateMovieView, DeleteMovieView, RegistrationView, LoginView, \
    LogoutView, ChangePasswordView, PremiumPageView

urlpatterns = [
    path('homepage/', HomepageView.as_view(), name='homepage'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('genre/<str:genre_name>/', GenreDetailView.as_view(), name='genre_detail'),
    path('actor/<str:actor_name>/', ActorDetailView.as_view(), name='actor_detail'),
    path('movie/reset-likes/<int:pk>', ResetMovieLikesView.as_view(), name='movie-reset-likes'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('create_movie/', CreateMovieView.as_view(), name='create_movie'),
    # # path('create_genre/', GenreMovieView.as_view(), name='genre_view'),
    path('create_actor/', CreateActorView.as_view(), name='create_actor'),
    path('update_movie/<int:pk>/', UpdateMovieView.as_view(), name='update_movie'),
    path('delete_movie/<int:pk>/', DeleteMovieView.as_view(), name='movie_delete'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('change_password', ChangePasswordView.as_view(), name='change_password'),
    path('premium', PremiumPageView.as_view(), name='premium_page'),
]
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponse
from django.shortcuts import redirect, resolve_url
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import BaseDeleteView, FormMixin
from django.contrib.auth.forms import AuthenticationForm

from hollymovies_app.forms import ContactForm, MovieForm, ActorForm, RegistrationForm
from hollymovies_app.models import Movie, Genre, Actor, GENRE_NAME_TO_NAME_SHORTCUT_MAPPING

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('homepage')


class LoginView(FormMixin, TemplateView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return redirect('login')

        login(request, user)
        return redirect('homepage')

class ChangePasswordView(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('homepage')




class RegistrationView(FormMixin, TemplateView):
    template_name = 'accounts/register.html'
    form_class = RegistrationForm

    def post(self, request, *args, **kwargs):
        bounded_form = self.form_class(request.POST)
        if bounded_form.is_valid():
            bounded_form.save()
            return redirect('homepage')
        else:
            return TemplateResponse(request, 'accounts/register.html', context={'form': bounded_form})

# def homepage(request):
#     movies_db = Movie.objects.all().order_by('-likes', 'name')
#     context = {
#         'movies': movies_db,
#         'horror_genre': Genre.HORROR,
#         'comedy_genre': Genre.COMEDY,
#     }
#     return TemplateResponse(request, 'homepage.html', context=context)

class CurrentTimeMixing:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_time': timezone.now().isoformat()
        })
        return context


class HomepageView(CurrentTimeMixing, TemplateView):
    template_name = 'homepage.html'
    extra_context = {
        'horror_genre': Genre.HORROR,
        'comedy_genre': Genre.COMEDY,
    }

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context.update({
            'movies': Movie.objects.all().order_by('-likes', 'name'),
        })
        return context

# class HomepageView(View):#
# def get(self, request, *ars, **kwargs):
#     movies_db = Movie.objects.all().order_by('-likes', 'name')
#
#     context = {
#         'movies': movies_db,
#         'horror_genre': Genre.HORROR,
#         'comedy_genre': Genre.COMEDY,
#     }
#     return TemplateResponse(request, 'homepage.html', context=context)


# def movie_detail(request, pk):
#     movie = Movie.objects.get(id=pk)
#
#     if request.method == 'POST':
#         movie.likes += 1
#         movie.save()
#
#     context = {
#         'movie': movie,
#     }
#     return TemplateResponse(request, 'detail/movie_detail.html', context=context)


# class MovieDetailView(View):
#     def get(self, request, pk, *ars, **kwargs):
#         movie = Movie.objects.get(id=pk)
#         context = {
#             'movie': movie,
#         }
#         return TemplateResponse(request, 'detail/movie_detail.html', context=context)
#
#     def post(self, request, pk, *ars, **kwargs):
#         movie = Movie.objects.get(id=pk)
#         movie.likes += 1
#         movie.save()
#         return self.get(request, pk, args, kwargs)

class MovieDetailView(CurrentTimeMixing, DetailView):
    template_name = 'detail/movie_detail.html'
    model = Movie
    # def get(self, request, pk, *ars, **kwargs):
    #     movie = Movie.objects.get(id=pk)
    #     context = {
    #         'movie': movie,
    #     }
    #     return TemplateResponse(request, 'detail/movie_detail.html', context=context)
    def post(self, request, pk, *args, **kwargs):
        movie = self.get_object()
        movie.likes += 1
        movie.save()
        return self.get(request, pk, *args, **kwargs)


class ResetMovieLikesView(SingleObjectMixin, View):
    model = Movie

    def post(self, request, pk, *args, **kwargs):
        movie = self.get_object()
        movie.likes = 0
        movie.save()
        return redirect('movie_detail', pk=pk)

# def genre_detail(request, genre_name):
#     genre_name_shortcut = GENRE_NAME_TO_NAME_SHORTCUT_MAPPING[genre_name]
#     genre = Genre.objects.get(name=genre_name_shortcut)
#     movies = genre.movies.filter(likes__gte=1)
#     context = {
#         'genre': genre,
#         'movies': movies,
#         'page_description': {
#             'long_description': 'This is long description',
#             'short_description': 'This is short description'
#         },
#         'creators': ['Jan', 'Pepa']
#     }
#     return TemplateResponse(request, 'detail/genre_detail.html', context=context)

class GenreDetailView(View):

    def get(self, request, genre_name, *args, **kwargs):
        genre_name_shortcut = GENRE_NAME_TO_NAME_SHORTCUT_MAPPING[genre_name]
        genre = Genre.objects.get(name=genre_name_shortcut)
        movies = genre.movies.filter(likes__gte=1)
        context = {
            'genre': genre,
            'movies': movies
        }
        return TemplateResponse(request, 'detail/genre_detail.html', context=context)

# def actor_detail(request, actor_name):
#     pk = Actor.objects.get(name=actor_name).id
#     actor = Actor.objects.get(id=pk)
#     description = actor.description
#     movies = actor.movies.all()
#
#     context = {
#         'actor': actor,
#         'description': description,
#         'movies': movies,
#
#     }
#     return TemplateResponse(request, 'detail/actor_detail.html', context=context)

class ActorDetailView(View):
    def get(self, request, actor_name, *args, **kwargs):
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
    #
    # def patch(self, request, pk, **kwargs):
    #     movie = self.get(pk)
    #     movie.likes += 1
    #     movie.save()
    #     return self.get(request, pk, kwargs)


class ContactView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'contact_form': ContactForm()
        }
        return TemplateResponse(request, 'detail/contact.html', context=context)

    def post(self, request, *args, **kwargs):
        bounded_contact_form = ContactForm(request.POST)

        if not bounded_contact_form.is_valid():
            context = {'form': bounded_contact_form}
            return TemplateResponse(request, 'detail/contact.html', context={context})

        name = bounded_contact_form.cleaned_data['name']
        email = bounded_contact_form.cleaned_data['email']
        subject = bounded_contact_form.cleaned_data['subject']
        description = bounded_contact_form.cleaned_data['description']

        print(name)
        print(email)
        print(subject)
        print(description)

        return redirect('contact')


class EditMovieMixin:
    template_name = 'create_movie.html'
    form_class = MovieForm
    model = Movie

    def get_success_url(self):
        return resolve_url('movie_detail', pk=self.object.id)

class CreateMovieView(EditMovieMixin, CreateView):
    def get_context_data(self, **kwargs):
        context = super(CreateMovieView, self).get_context_data(**kwargs)
        context.update({
            'action_url': resolve_url('create_movie')
        })
        return context


class UpdateMovieView(EditMovieMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super(UpdateMovieView, self).get_context_data(**kwargs)
        context.update({
            'action_url': resolve_url('update_movie', pk=self.object.pk)
        })
        return context


class DeleteMovieView(BaseDeleteView):
    model = Movie

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return resolve_url('homepage')


class CreateActorView(CreateView):
    template_name = 'create_actor.html'
    form_class = ActorForm
    model = Actor

    def get_success_url(self):
        return resolve_url('actor_detail', pk=self.object.id)

# class CreateMovieView(CreateView):
#     template_name = 'create_movie.html'
#     form_class = MovieForm
#     model = Movie
#
#     def get_success_url(self):
#         return resolve_url('movie_detail', pk=self.object.id)


class PremiumPageView(PermissionRequiredMixin, TemplateView):
    template_name = 'premium.html'
    permission_required = 'general_permission.can_view_premium_page'


def homepage_kristi(request):
    return HttpResponse('<h1>Hollymovies Homepage Kristi</h1>')
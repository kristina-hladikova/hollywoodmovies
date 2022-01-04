from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve

from hollymovies_app.forms import MovieForm
from hollymovies_app.models import Movie, Genre
from hollymovies_app.views import HomepageView, GenreDetailView


class TestUrls(SimpleTestCase):

    def test_homepage_url_is_resolved(self):
        url = reverse('homepage')
        self.assertEqual(resolve(url).func.view_class, HomepageView)

    def test_genre_detail_url_is_resolved(self):
        url = reverse('genre_detail', args=['testing_genre'])
        self.assertEqual(resolve(url).func.view_class, GenreDetailView)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.movie = Movie.objects.create(name='Testing Movie')

    @classmethod
    def setUpClass(cls):
        super(TestViews, cls).setUpClass()

    def test_homepage_GET(self):
        url = reverse('homepage')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'homepage.html')

    def test_movie_detail_GET(self):
        url = reverse('movie_detail', args=[9999999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        url = reverse('movie_detail', args=[self.movie.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_movie_detail_POST(self):
        url = reverse('movie_detail', args=[self.movie.id])
        response = self.client.post(url)
        self.movie.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.movie.likes, 1)

class TestModels(TestCase):

    def setUp(self):
        self.horror = Genre.objects.create(name=Genre.HORROR)
        self.horror = Genre.objects.create(name=Genre.COMEDY)

    def test_genre_is_horror(self):
        self.assertEqual(self.horror.is_genre_horror())

    def test_genre_is_comedy(self):
        self.assertEqual(self.comedy.is_genre_horror())




class TestForms(TestCase):

    def test_movie_form_is_valid(self):
        genre = Genre.objects.create(name=Genre.HORROR)
        form = MovieForm(data={
            'name': 'Rambo 1',
            'description': 'Just another Jumbo movie',
            'genres': [genre.id]
        })
        self.assertTrue(form.is_valid())

    def rest_movie_form_is_invalid(self):
        form = MovieForm(data={})
        self.assertFalse(form.is_valid())








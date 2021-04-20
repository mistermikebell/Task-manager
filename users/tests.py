from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from django.test import Client
from django.template.response import TemplateResponse


class AuthenticationTest(TestCase):

    c = Client()

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='1111',
            email='test@test.com')
        self.user.save()

    def test_signup(self):
        response = self.c.post('/users/create/', {'username': 'tester', 'email': 'test@test.com', 'password1': '1Password!', 'password2': '1Password!'})
        self.assertTrue(response.status_code, 200)

    def test_login(self):
        response = self.c.post('/users/login/', {'username': 'test', 'password': '1111'})
        self.assertRedirects(response, '/')


    def test_wrong_username(self):
        response = self.c.post('/users/login/', {'username': 'test', 'password': '2222'})
        self.assertTrue(response.status_code, 200)


    '''def test_wrong_password(self):
        user = authenticate(username='test', password='2222')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_update(self):
        user = get_user_model().objects.get(username='test')
        new_username = 'testtest'
        user.username = new_username
        user.save()
        self.assertTrue(new_username is user.get_username())


class AuthenticationTestFormer(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='1111',
            email='test@test.com')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_login(self):
        user = authenticate(username='test', password='1111')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='not_test', password='1111')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username='test', password='2222')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_update(self):
        user = get_user_model().objects.get(username='test')
        new_username = 'testtest'
        user.username = new_username
        user.save()
        self.assertTrue(new_username is user.get_username())'''

from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate


class AuthenticationTest(TestCase):

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
        self.assertTrue(new_username is user.get_username())

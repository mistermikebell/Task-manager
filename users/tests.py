from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from users.models import UserModel


class UsersTest(TestCase):

    def setUp(self):
        self.test_user = UserModel.objects.create_user(username='test_user',
                                                       password='1Password!')

    def test_signup(self):
        credentials = {'username': 'new_user',
                       'first_name': 'test',
                       'last_name': 'test',
                       'email': 'test@test.com',
                       'password1': '1Password!',
                       'password2': '1Password!'}
        response = self.client.post('/users/create/', credentials, follow=True)
        self.assertRedirects(response, '/login/')
        self.assertEqual(UserModel.objects.get(username='new_user').username,
                         'new_user')

    def test_login(self):
        response = self.client.post('/login/', {'username': 'test_user',
                                                'password': '1Password!'},
                                    follow=True)
        self.assertTrue(response.context['request'].user.is_authenticated)
        self.assertRedirects(response, '/')

    def test_update(self):
        self.client.login(username='test_user', password='1Password!')
        self.client.post(reverse('update', args=str(self.test_user.id)),
                         {'username': 'updated_test_user',
                          'first_name': 'test',
                          'last_name': 'test',
                          'email': 'email@email.com',
                          'password1': '1Password!',
                          'password2': '1Password!'})
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.username, 'updated_test_user')
        self.assertEqual(self.test_user.first_name, 'test')
        self.assertEqual(self.test_user.last_name, 'test')
        self.assertEqual(self.test_user.email, 'email@email.com')

    def test_delete(self):
        self.client.login(username='test_user', password='1Password!')
        test_user_id = self.test_user.id
        self.client.post(reverse('delete', args=str(test_user_id)))
        with self.assertRaises(ObjectDoesNotExist):
            self.test_user.refresh_from_db()

    def test_permission(self):
        self.test_user2 = UserModel.objects.create_user(username='test_user2',
                                                        password='1Password!')
        self.client.login(username='test_user', password='1Password!')
        response = self.client.post(reverse('update',
                                            args=str(self.test_user2.id)),
                                    follow=True)
        self.assertRedirects(response, '/users/')
        response = self.client.post(reverse('delete',
                                            args=str(self.test_user2.id)),
                                    follow=True)
        self.assertRedirects(response, '/users/')

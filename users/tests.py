from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse


class UsersTest(TestCase):

    c = Client()

    def setUp(self):
        self.new_user = {'username': 'new_user',
                         'email': 'test@test.com',
                         'password1': '1Password!',
                         'password2': '1Password!'}
        self.test_user = User.objects.create_user(username='test_user',
                                                  password='1Password!')

    def test_signup(self):
        response = self.c.post('/users/create/', self.new_user, follow=True)
        self.assertRedirects(response, '/login/')

    def test_login(self):
        response = self.c.post('/login/', {'username': 'test_user',
                                           'password': '1Password!'},
                               follow=True)
        self.assertTrue(response.context['request'].user.is_authenticated)
        self.assertRedirects(response, '/')

    def test_update(self):
        self.c.login(username='test_user', password='1Password!')
        self.c.post(reverse('update', args=str(self.test_user.id)),
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
        self.c.login(username='test_user', password='1Password!')
        test_user_id = self.test_user.id
        self.c.post(reverse('delete', args=str(test_user_id)))
        with self.assertRaises(ObjectDoesNotExist):
            self.test_user.refresh_from_db()

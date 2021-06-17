from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from .models import Label
from users.models import UserModel


class LabelsTest(TestCase):

    def setUp(self):
        self.new_label = {'name': 'new_label', 'description': 'testing'}
        self.test_user = UserModel.objects.create_user(username='test_user',
                                                       password='1Password!')
        self.test_label = Label.objects.create(name='test_label',
                                               description='testing',
                                               author=self.test_user)
        self.client.login(username='test_user', password='1Password!')

    def test_creation(self):
        response = self.client.post('/labels/create/',
                                    {'name': 'new_label',
                                     'description': 'testing'},
                                    follow=True)
        self.assertRedirects(response, reverse('labels_list'))
        self.assertEqual('new_label',
                         Label.objects.get(name='new_label').name)

    def test_update(self):
        self.client.post(reverse('label_update', args=str(self.test_label.id)),
                         {'name': 'updated_test_label',
                          'description': 'testing'})
        self.test_label.refresh_from_db()
        self.assertEqual(self.test_label.name, 'updated_test_label')
        self.assertEqual(self.test_label.description, 'testing')

    def test_delete(self):
        test_label_id = self.test_label.id
        self.client.post(reverse('label_delete', args=str(test_label_id)))
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(id=test_label_id)

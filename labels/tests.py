from labels.models import Label
from tasks.models import Task
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse
from users.models import UserModel


class LabelsTest(TestCase):

    c = Client()

    def setUp(self):
        self.new_label = {'name': 'new_label', 'description': 'testing'}
        self.test_user = UserModel.objects.create_user(username='test_user',
                                                       password='1Password!')
        self.test_task = Task.objects.create(name='test_task',
                                             author=self.test_user,
                                             executor=self.test_user)
        self.test_label = Label.objects.create(name='test_label',
                                               description='testing',
                                               author=self.test_user)
        self.c.login(username='test_user', password='1Password!')

    def test_label_creation(self):
        response = self.c.post('/labels/create/', self.new_label,
                               follow=True)
        self.assertRedirects(response, reverse('labels_list'))
        self.assertEqual('new_label',
                         Label.objects.get(name='new_label').name)

    def test_label_update(self):
        self.c.post(reverse('label_update', args=str(self.test_label.id)),
                    {'name': 'updated_test_label', 'description': 'testing'})
        self.test_label.refresh_from_db()
        self.assertEqual(self.test_label.name, 'updated_test_label')
        self.assertEqual(self.test_label.description, 'testing')

    def test_label_delete(self):
        test_label_id = self.test_label.id
        self.c.post(reverse('label_delete', args=str(test_label_id)))
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(id=test_label_id)

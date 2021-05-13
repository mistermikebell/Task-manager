from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse
from statuses.models import Status
from users.models import UserModel


class StatusesTest(TestCase):

    c = Client()

    def setUp(self):
        self.new_status = {'name': 'new_status'}
        self.test_user = UserModel.objects.create_user(username='test_user',
                                                       password='1Password!')
        self.test_status = Status.objects.create(name='test_status',
                                                 author=self.test_user)
        self.c.login(username='test_user', password='1Password!')

    def test_status_creation(self):
        response = self.c.post('/statuses/create/', self.new_status,
                               follow=True)
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertEqual('new_status',
                         Status.objects.get(name='new_status').name)

    def test_status_update(self):
        self.c.post(reverse('status_update', args=str(self.test_status.id)),
                    {'name': 'updated_test_status'})
        self.test_status.refresh_from_db()
        self.assertEqual(self.test_status.name, 'updated_test_status')

    def test_status_delete(self):
        test_status_id = self.test_status.id
        self.c.post(reverse('status_delete', args=str(test_status_id)))
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(id=test_status_id)

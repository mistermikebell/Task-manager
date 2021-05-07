from statuses.models import Status
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse


class StatusesTest(TestCase):

    c = Client()

    def setUp(self):
        self.new_status = {'status': 'new_status'}
        self.test_user = User.objects.create_user(username='test_user',
                                                  password='1Password!')
        self.test_status = Status.objects.create(status='test_status',
                                                 creator=self.test_user,
                                                 editor=self.test_user)
        self.c.login(username='test_user', password='1Password!')

    def test_status_creation(self):
        response = self.c.post('/statuses/create/', self.new_status,
                               follow=True)
        self.assertRedirects(response, reverse('statuses_list'))
        Status.objects.get(status='new_status')

    def test_status_update(self):
        self.c.post(reverse('status_update', args=str(self.test_status.id)),
                    {'status': 'updated_test_status'})
        self.test_status.refresh_from_db()
        self.assertEqual(self.test_status.status, 'updated_test_status')

    def test_status_delete(self):
        test_status_id = self.test_status.id
        self.c.post(reverse('status_delete', args=str(test_status_id)))
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(id=test_status_id)

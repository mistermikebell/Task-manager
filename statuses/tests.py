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

    def tearDown(self):
        self.test_status.delete()
        self.test_user.delete()

    def test_status_creation(self):
        self.c.login(username='test_user', password='1Password!')
        response = self.c.post('/statuses/create/', self.new_status,
                               follow=True)
        self.assertRedirects(response, reverse('statuses_list'))

    def test_update(self):
        self.c.login(username='test_user', password='1Password!')
        print('STATUS', self.test_status.id)
        self.c.post(reverse('status_update', args=str(self.test_status.id)),
                    {'status': 'updated_test_status'})
        self.test_status.refresh_from_db()
        self.assertEqual(self.test_status.status, 'updated_test_status')

    # def test_delete(self):
    #     self.c.login(username='test_user', password='1Password!')
    #     self.c.post(reverse('delete', args=str(self.test_user.id)))
    #     with self.assertRaises(ObjectDoesNotExist):
    #         User.objects.get(id=1)

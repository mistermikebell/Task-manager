from tasks.models import Task
from statuses.models import Status
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse


class TasksTest(TestCase):

    c = Client()

    def setUp(self):
        self.new_task = {'task': 'new_task'}
        self.test_user = User.objects.create_user(username='test_user',
                                                  password='1Password!')
        self.test_status = Status.objects.create(status='test_status',
                                                 creator=self.test_user,
                                                 editor=self.test_user)
        self.test_task = Task.objects.create(task='test_task',
                                             author=self.test_user,
                                             last_editor=self.test_user)
        self.c.login(username='test_user', password='1Password!')

    def tearDown(self):
        self.test_task.delete()
        self.test_status.delete()
        self.test_user.delete()

    def test_task_creation(self):
        response = self.c.post('/tasks/create/', self.new_task,
                               follow=True)
        self.assertRedirects(response, reverse('tasks_list'))
        Task.objects.get(task='new_task').delete()

    def test_task_update(self):
        self.c.post(reverse('task_update', args=str(self.test_task.id)),
                    {'task': 'updated_test_task'})
        self.test_task.refresh_from_db()
        self.assertEqual(self.test_task.task, 'updated_test_task')

    def test_task_delete(self):
        test_task_id = self.test_status.id
        self.c.post(reverse('task_delete', args=str(test_task_id)))
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(id=test_task_id)

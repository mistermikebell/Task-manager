from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from labels.models import Label
from statuses.models import Status
from tasks.models import Task
from users.models import UserModel


class TasksTest(TestCase):

    def setUp(self):
        self.test_user = UserModel.objects.create_user(username='test_user',
                                                       password='1Password!')
        self.test_status = Status.objects.create(name='test_status',
                                                 author=self.test_user)
        self.test_task = Task.objects.create(name='test_task',
                                             author=self.test_user,
                                             status=self.test_status)
        self.test_label = Label.objects.create(name='test_label',
                                               description='label for test',
                                               author=self.test_user)
        self.client.login(username='test_user', password='1Password!')

    def test_creation(self):
        response = self.client.post('/tasks/create/',
                                    {'name': 'new_task',
                                     'status': self.test_status.id,
                                     'description': 'test',
                                     'executor': '',
                                     'labels': []
                                     },
                                    follow=True)
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertEqual('new_task',
                         Task.objects.get(name='new_task').name)

    def test_update(self):
        self.client.post(reverse('task_update', args=str(self.test_task.id)),
                         {'name': 'updated_test_task',
                          'status': self.test_status.id,
                          'labels': [self.test_label.id],
                          'description': 'new test',
                          'executor': self.test_user.id})
        self.test_task.refresh_from_db()
        self.assertEqual(self.test_task.name, 'updated_test_task')
        self.assertEqual(self.test_task.status, self.test_status)
        self.assertEqual(self.test_task.labels.all()[0], self.test_label)
        self.assertEqual(self.test_task.description, 'new test')
        self.assertEqual(self.test_task.executor, self.test_user)

    def test_delete(self):
        test_task_id = self.test_status.id
        self.client.post(reverse('task_delete', args=str(test_task_id)))
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(id=test_task_id)


class TaskFilterTest(TestCase):

    def setUp(self):
        self.user_1 = UserModel.objects.create_user(username='test_user_1',
                                                    password='1Password!')
        self.user_2 = UserModel.objects.create_user(username='test_user_2',
                                                    password='1Password!')
        self.status_1 = Status.objects.create(name='test_status_1',
                                              author=self.user_1)
        self.status_2 = Status.objects.create(name='test_status_2',
                                              author=self.user_1)
        self.label_1 = Label.objects.create(name='test_label',
                                            description='label for test',
                                            author=self.user_1)
        Task.objects.create(name='test_task_1',
                            author=self.user_1,
                            executor=self.user_2,
                            status=self.status_1)
        Task.objects.create(name='test_task_2',
                            author=self.user_2,
                            executor=self.user_1,
                            status=self.status_2)
        self.test_task_3 = Task.objects.create(name='test_task_3',
                                               author=self.user_2,
                                               executor=self.user_2,
                                               status=self.status_1)
        self.test_task_3.labels.set(Label.objects.filter(name='test_label'))
        self.client.login(username='test_user_1', password='1Password!')

    def test_author_filter(self):
        response = self.client.get(reverse('tasks_list'), {'author_tasks': 'on'})
        self.assertQuerysetEqual(
            response.context['object_list'],
            Task.objects.filter(author=self.user_1),
            ordered=False)

    def test_executor_filter(self):
        response = self.client.get(reverse('tasks_list'),
                                   {'executor': self.user_1.id})
        self.assertQuerysetEqual(
            response.context['object_list'],
            Task.objects.filter(executor=self.user_1),
            ordered=False)

    def test_status_filter(self):
        response = self.client.get(reverse('tasks_list'),
                                   {'status': self.status_1.id})
        self.assertQuerysetEqual(
            response.context['object_list'],
            Task.objects.filter(status=self.status_1),
            ordered=False)

    def test_label_filter(self):
        response = self.client.get(reverse('tasks_list'),
                                   {'labels': self.label_1.id})
        self.assertQuerysetEqual(
            response.context['object_list'],
            Task.objects.filter(labels=self.label_1),
            ordered=False)

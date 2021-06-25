from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django_filters.views import FilterView

from statuses.models import Status
from tasks.filters import TasksFilter
from tasks.models import Task
from tasks.mixins import NonAuthorPermissionMixin
from task_manager.mixins import (NoPermissionRedirectMixin,
                                 LoginRequiredMixinRedirect,
                                 DeletionErrorMixin)


class TaskCreateView(NoPermissionRedirectMixin, LoginRequiredMixinRedirect,
                     SuccessMessageMixin, CreateView):
    model = Task
    fields = ['name', 'status', 'labels', 'description', 'executor']
    template_name = 'tasks/task-creation.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('You have created a new task!')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TasksListView(NoPermissionRedirectMixin, LoginRequiredMixinRedirect,
                    FilterView):
    model = Task
    template_name = 'tasks/tasks-list.html'
    filterset_class = TasksFilter


class TaskDetailView(NoPermissionRedirectMixin, LoginRequiredMixinRedirect,
                     generic.DetailView):
    model = Task
    template_name = 'tasks/task-details.html'


class TaskUpdateView(NoPermissionRedirectMixin, LoginRequiredMixinRedirect,
                     SuccessMessageMixin, generic.UpdateView):
    model = Task
    template_name = 'tasks/task-update.html'
    fields = ['name', 'status', 'labels', 'description', 'executor']
    success_message = _('Task has been updated')
    success_url = reverse_lazy('tasks_list')


class TaskDeleteView(NoPermissionRedirectMixin, LoginRequiredMixinRedirect,
                     NonAuthorPermissionMixin, DeletionErrorMixin,
                     generic.DeleteView):
    model = Task
    template_name = 'tasks/task-delete.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('Task has been deleted')


class UserTasksListView(FilterView):
    model = Task
    template_name = 'index.html'
    filterset_fields = ['status']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'statuses': Status.objects.all()})
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Task.objects.filter(executor=self.request.user)

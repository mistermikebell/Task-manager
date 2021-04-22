from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django_filters.views import FilterView
from tasks.models import Task
from tasks.filters import TasksFilter
from django.utils.translation import ugettext_lazy as _


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    fields = ['task', 'status', 'labels', 'content']
    template_name = 'tasks/task-creation.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('You have created a new task!')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.last_editor = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           _('You do not have access to this page'))
        return redirect_to_login(self.request.get_full_path(), 'login/', '')


class TasksListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/tasks-list.html'
    context_object_name = 'tasks_list'
    filterset_class = TasksFilter

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           _('You do not have access to this page'))
        return redirect_to_login(self.request.get_full_path(), 'login/', '')


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Task
    template_name = 'tasks/task-update.html'
    fields = ['task', 'status', 'labels', 'content']
    login_url = 'login'
    success_message = _('Task has been updated')
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        form.instance.last_editor = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           _('You do not have access to this page'))
        return redirect_to_login(self.request.get_full_path(), 'login/', '')


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy('tasks_list')
    template_name = 'tasks/task-delete.html'
    success_message = _('Task has been deleted')

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           _('You do not have access to this page'))
        return redirect_to_login(self.request.get_full_path(), 'login/', '')

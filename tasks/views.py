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
from task_manager.statuces.models import Status
from django.contrib.auth.models import User


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    fields = ['task', 'status', 'labels', 'content']
    template_name = 'task-creation.html'
    success_url = reverse_lazy('home')
    success_message = gettext('You have created a new task!')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.last_editor = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           gettext('You do not have access to this page'))
        return redirect_to_login(self.request.get_full_path(), 'login/', '')


class TasksListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks-list.html'
    context_object_name = 'tasks_list'
    filterset_class = TasksFilter

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           gettext('You do not have access to this page'))
        return redirect_to_login(self.request.get_full_path(), 'login/', '')

    '''def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = TasksFilter(self.request.GET, queryset=self.get_queryset(), request=self.request)
        return context'''


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Task
    template_name = 'task-update.html'
    fields = ['task', 'status', 'labels', 'content']
    login_url = 'login'
    redirect_field_name = 'login'
    permission_denied_message = gettext('You do not have access to this page')
    success_message = gettext('Task has been updated')
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        form.instance.last_editor = self.request.user
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy('statuses_list')
    template_name = 'task-delete.html'
    permission_denied_message = gettext('You do not have access to this page')
    success_message = gettext('Task has been deleted')

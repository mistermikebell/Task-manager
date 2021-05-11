from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django_filters.views import FilterView
from tasks.models import Task
from tasks.filters import TasksFilter
from task_manager.views import LoginRequiredMixinRedirect


class TaskCreateView(LoginRequiredMixinRedirect, SuccessMessageMixin, CreateView):
    model = Task
    fields = ['name', 'status', 'labels', 'description', 'executor']
    template_name = 'tasks/task-creation.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('You have created a new task!')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TasksListView(LoginRequiredMixinRedirect, FilterView):
    model = Task
    template_name = 'tasks/tasks-list.html'
    filterset_class = TasksFilter


class TaskDetailView(LoginRequiredMixinRedirect, generic.DetailView):
    model = Task
    template_name = 'tasks/task-details.html'


class TaskUpdateView(LoginRequiredMixinRedirect, SuccessMessageMixin, generic.UpdateView):
    model = Task
    template_name = 'tasks/task-update.html'
    fields = ['name', 'status', 'labels', 'description', 'executor']
    login_url = 'login'
    success_message = _('Task has been updated')
    success_url = reverse_lazy('tasks_list')

    def get_initial(self):
        return {'description': Task.objects.get(pk=self.kwargs['pk']).description}


class TaskDeleteView(LoginRequiredMixinRedirect, SuccessMessageMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy('tasks_list')
    template_name = 'tasks/task-delete.html'
    success_message = _('Task has been deleted')

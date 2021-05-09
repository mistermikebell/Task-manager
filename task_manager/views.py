from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from tasks.models import Task
from task_manager.filters import MyTasksFilter


class LoginRequiredMixinRedirect(LoginRequiredMixin):
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           _('You do not have access to this page'))
        return redirect_to_login(self.request.get_full_path(), 'user-login', '')


class MyTasksListView(FilterView):
    model = Task
    template_name = 'index.html'
    filterset_class = MyTasksFilter

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Task.objects.filter(executor=self.request.user)

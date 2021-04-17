from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.translation import gettext
from statuses.models import Status


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    fields = ['status_name']
    template_name = 'status-creation.html'
    success_url = reverse_lazy('statuses_list')
    success_message = gettext('You have created a new status!')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.editor = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           gettext('You do not have access to this page'))
        return redirect_to_login(self.request.get_full_path(), 'login/', '')


class StatusesListView(LoginRequiredMixin, generic.ListView):
    model = Status
    template_name = 'statuses.html'
    context_object_name = 'statuses_list'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           gettext('You do not have access to this page'))
        return redirect_to_login(self.request.get_full_path(), 'login/', '')


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Status
    template_name = 'update.html'
    fields = ['status_name']
    login_url = 'login'
    redirect_field_name = 'statuses_list'
    permission_denied_message = gettext('You do not have access to this page')
    success_message = gettext('Status has been updated')
    success_url = reverse_lazy('statuses_list')

    def form_valid(self, form):
        form.instance.editor = self.request.user
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Status
    success_url = reverse_lazy('statuses_list')
    template_name = 'delete.html'
    permission_denied_message = gettext('You do not have access to this page')
    success_message = gettext('Status has been deleted')

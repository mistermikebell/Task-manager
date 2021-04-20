from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from statuses.models import Status


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    fields = ['status']
    template_name = 'statuses/status-creation.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('You have created a new status!')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.editor = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           _('You do not have access to this page'))
        return redirect_to_login(self.request.get_full_path(), 'login/', '')


class StatusesListView(LoginRequiredMixin, generic.ListView):
    model = Status
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses_list'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           _('You do not have access to this page'))
        return redirect_to_login(self.request.get_full_path(), 'login/', '')


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Status
    template_name = 'statuses/update.html'
    fields = ['status_name']
    login_url = 'login'
    success_message = _('Status has been updated')
    success_url = reverse_lazy('statuses_list')

    def form_valid(self, form):
        form.instance.editor = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           _('You do not have access to this page'))
        return redirect_to_login(self.request.get_full_path(), 'login/', '')


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Status
    success_url = reverse_lazy('statuses_list')
    template_name = 'statuses/delete.html'
    success_message = _('Status has been deleted')

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           _('You do not have access to this page'))
        return redirect_to_login(self.request.get_full_path(), 'login/', '')

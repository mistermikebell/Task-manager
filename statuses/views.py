from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from statuses.models import Status
from task_manager.mixins import LoginRequiredMixinRedirect, DeletionErrorMixin


class StatusCreateView(LoginRequiredMixinRedirect, SuccessMessageMixin, CreateView):
    model = Status
    fields = ['name']
    template_name = 'statuses/status-creation.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('You have created a new status!')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class StatusesListView(LoginRequiredMixinRedirect, generic.ListView):
    model = Status
    template_name = 'statuses/statuses-list.html'


class StatusUpdateView(LoginRequiredMixinRedirect, SuccessMessageMixin, generic.UpdateView):
    model = Status
    template_name = 'statuses/status-update.html'
    fields = ['name']
    success_message = _('Status has been updated')
    success_url = reverse_lazy('statuses_list')


class StatusDeleteView(LoginRequiredMixinRedirect, generic.DeleteView,
                       DeletionErrorMixin):
    model = Status
    template_name = 'statuses/status-delete.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Status has been deleted')
    error_message = _('Cannot delete this status, '
                      'because the status is attached to an object!')

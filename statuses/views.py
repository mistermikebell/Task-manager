from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from statuses.models import Status
from task_manager.views import LoginRequiredMixinRedirect


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
    login_url = 'login'
    success_message = _('Status has been updated')
    success_url = reverse_lazy('statuses_list')


class StatusDeleteView(LoginRequiredMixinRedirect, SuccessMessageMixin, generic.DeleteView):
    model = Status
    success_url = reverse_lazy('statuses_list')
    template_name = 'statuses/status-delete.html'
    success_message = _('Status has been deleted')


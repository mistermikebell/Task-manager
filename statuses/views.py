from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
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


class StatusDeleteView(LoginRequiredMixinRedirect, generic.DeleteView):
    model = Status
    success_url = reverse_lazy('statuses_list')
    template_name = 'statuses/status-delete.html'

    def delete(self, request, *args, **kwargs):

        try:
            self.object = self.get_object()
            self.object.delete()
            messages.add_message(request, messages.SUCCESS,
                                 _('Status has been deleted'))
            return HttpResponseRedirect(self.get_success_url())

        except ProtectedError:
            messages.add_message(request, messages.ERROR,
                                 _('Cannot delete this status, because'
                                   ' the status is attached to an object!'))
            return HttpResponseRedirect(reverse_lazy('users_list'))


from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from labels.models import Label
from task_manager.views import LoginRequiredMixinRedirect


class LabelCreateView(LoginRequiredMixinRedirect, SuccessMessageMixin, CreateView):
    model = Label
    fields = ['name', 'description']
    template_name = 'labels/label-creation.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Label has been created successfully')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class LabelListView(LoginRequiredMixinRedirect, generic.ListView):
    model = Label
    template_name = 'labels/labels-list.html'


class LabelUpdateView(LoginRequiredMixinRedirect, SuccessMessageMixin, generic.UpdateView):
    model = Label
    template_name = 'labels/label-update.html'
    fields = ['name', 'description']
    login_url = 'login'
    success_message = _('Label has been updated successfully')
    success_url = reverse_lazy('labels_list')

    def get_initial(self):
        return {'description': Label.objects.get(pk=self.kwargs['pk']).description}


class LabelDeleteView(LoginRequiredMixinRedirect, generic.DeleteView):
    model = Label
    success_url = reverse_lazy('labels_list')
    template_name = 'labels/label-delete.html'

    def delete(self, request, *args, **kwargs):

        try:
            self.object = self.get_object()
            self.object.delete()
            messages.add_message(request, messages.SUCCESS,
                                 _('Label has been deleted successfully'))
            return HttpResponseRedirect(self.get_success_url())

        except ProtectedError:
            messages.add_message(request, messages.ERROR,
                                 _('Cannot delete this label, because'
                                   ' the label is attached to an object!'))
            return HttpResponseRedirect(reverse_lazy('users_list'))

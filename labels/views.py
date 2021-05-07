from django.contrib.messages.views import SuccessMessageMixin
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
    success_url = reverse_lazy('home')
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


class LabelDeleteView(LoginRequiredMixinRedirect, SuccessMessageMixin, generic.DeleteView):
    model = Label
    success_url = reverse_lazy('labels_list')
    template_name = 'labels/label-delete.html'
    success_message = _('Label has been deleted successfully')

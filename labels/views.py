from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from labels.models import Label


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    fields = ['label', 'description']
    template_name = 'labels/label-creation.html'
    success_url = reverse_lazy('home')
    success_message = _('Label has been created successfully')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.last_editor = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           _('You do not have access to this page'))
        return redirect_to_login(self.request.get_full_path(), 'login/', '')


class LabelListView(LoginRequiredMixin, generic.ListView):
    model = Label
    template_name = 'labels/labels-list.html'
    context_object_name = 'labels_list'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           _('You do not have access to this page'))
        return redirect_to_login(self.request.get_full_path(), 'login/', '')


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Label
    template_name = 'labels/label-update.html'
    fields = ['label', 'description']
    login_url = 'login'
    success_message = _('Label has been updated successfully')
    success_url = reverse_lazy('labels_list')

    def form_valid(self, form):
        form.instance.last_editor = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           _('You do not have access to this page'))
        return redirect_to_login(self.request.get_full_path(), 'login/', '')


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Label
    success_url = reverse_lazy('labels_list')
    template_name = 'labels/label-delete.html'
    success_message = _('Label has been deleted successfully')

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           _('You do not have access to this page'))
        return redirect_to_login(self.request.get_full_path(), 'login/', '')

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from users.forms import SignUpForm


class RegisterUserView(SuccessMessageMixin, generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')
    success_message = _('You have been signed up!')


class UsersListView(generic.ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users_list'


class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = User
    template_name = 'registration/update.html'
    fields = ['username', 'email', 'password']
    success_message = _('Your profile has been updated')

    def get_success_url(self):
        return ''

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           _('You do not have access to this page'))
        return redirect_to_login(self.request.get_full_path(), 'login', '')


class DeleteUserView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy('home')
    template_name = 'registration/delete.html'
    success_message = _('Your profile has been deleted')

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           _('You do not have access to this page'))
        return redirect_to_login(self.request.get_full_path(), 'login', '')

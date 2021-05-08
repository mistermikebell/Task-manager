from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.utils.translation import ugettext_lazy as _
from users.forms import SignUpForm
from task_manager.views import LoginRequiredMixinRedirect


class RegisterUserView(SuccessMessageMixin, generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/user-register.html'
    success_url = reverse_lazy('home')
    success_message = _('You have been signed up!')


class UsersListView(generic.ListView):
    model = User
    template_name = 'users/users-list.html'


class UpdateUserView(LoginRequiredMixinRedirect, SuccessMessageMixin, generic.UpdateView):
    model = User
    template_name = 'registration/user-update.html'
    fields = ['username', 'email', 'password']
    success_message = _('Your profile has been updated')

    def get_success_url(self):
        return ''


class DeleteUserView(LoginRequiredMixinRedirect, SuccessMessageMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy('home')
    template_name = 'registration/user-delete.html'
    success_message = _('Your profile has been deleted')

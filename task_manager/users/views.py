from django.views import generic
from task_manager.users.forms import SignUpForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login


class RegisterUser(SuccessMessageMixin, generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')
    success_message = 'You have been signed up!'


class UsersList(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'users_list'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'You do not have access to this page')
        return redirect_to_login(self.request.get_full_path(), 'login/', '')


class UpdateUser(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = User
    template_name = 'registration/update.html'
    fields = ['username', 'email', 'password']
    login_url = 'login/'
    redirect_field_name = ''
    permission_denied_message = 'You do not have access to this page'
    success_message = 'Your profile has been updated'

    def get_success_url(self):
        return ''


class DeleteUser(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy('home')
    template_name = 'registration/delete.html'
    permission_denied_message = 'You do not have access to this page'
    success_message = 'Your profile has been deleted'

from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from task_manager.mixins import LoginRequiredMixinRedirect, DeletionErrorMixin
from users.forms import SignUpForm, UserUpdateForm
from users.models import UserModel


class RegisterUserView(SuccessMessageMixin, generic.CreateView):
    model = UserModel
    form_class = SignUpForm
    template_name = 'users/registration/user-register.html'
    success_url = reverse_lazy('login')
    success_message = _('You have been signed up!')


class LoginUserView(SuccessMessageMixin, LoginView):
    template_name = 'users/registration/user-login.html'
    success_message = _('You are logged in!')


class LogoutUserView(SuccessMessageMixin, LogoutView):

    def dispatch(self, request, *args, **kwargs):
        messages.warning(request, _('You are logged out!'))
        return super().dispatch(request, *args, **kwargs)


class UsersListView(generic.ListView):
    model = UserModel
    template_name = 'users/users-list.html'


class UpdateUserView(LoginRequiredMixinRedirect, SuccessMessageMixin, generic.edit.UpdateView):
    model = UserModel
    template_name = 'users/registration/user-update.html'
    success_message = _('Your profile has been updated')
    success_url = reverse_lazy('users_list')
    form_class = UserUpdateForm

    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        obj = self.get_object()
        if obj.id != self.request.user.id:
            messages.error(request,
                           _('You are not allowed to edit another user profile'))
            return HttpResponseRedirect(reverse_lazy('users_list'))
        return handler


class DeleteUserView(LoginRequiredMixinRedirect, generic.DeleteView,
                     DeletionErrorMixin):
    model = UserModel
    success_url = reverse_lazy('users_list')
    template_name = 'users/registration/user-delete.html'
    deletion_success_url = reverse_lazy('users_list')
    deletion_success_message = _('Your profile has been deleted')
    deletion_error_message = _('Cannot delete this user, '
                               'because the user is attached to an object!')

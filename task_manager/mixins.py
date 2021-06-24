from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.views.generic.edit import DeletionMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _


class RedirectMixin:

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.redirect_url)


class LoginRequiredMixinRedirect(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _('You do not have access to this page')
        self.redirect_url = reverse_lazy('login')
        if not request.user.is_authenticated:
            self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class NoPermissionMixin(UserPassesTestMixin):

    def test_func(self):
        return self.get_object().id == self.request.user.id

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _('I know you were trouble')
        if not self.get_test_func()():
            self.redirect_url = reverse_lazy('users_list')
            self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class AccessValidationMixin(RedirectMixin, LoginRequiredMixinRedirect, NoPermissionMixin):
    pass


class DeletionErrorMixin(DeletionMixin):
    success_url = reverse_lazy('home')
    success_message = _('Object has been deleted')
    error_message = _('Cannot delete this object,'
                      ' because the status is attached to an object!')

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, self.success_message)
            return response
        except ProtectedError:
            messages.error(request, self.error_message)
            return HttpResponseRedirect(self.success_url)

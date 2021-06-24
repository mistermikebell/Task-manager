from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.views.generic.edit import DeletionMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _


class LoginRequiredMixinRedirect(LoginRequiredMixin):
    permission_denied_message = _('You do not have access to this page')

    def dispatch(self, request, *args, **kwargs):
        self.redirect_url = reverse_lazy('login')
        if not request.user.is_authenticated:
            messages.error(self.request, self.permission_denied_message)
            self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class NoPermissionMixin(UserPassesTestMixin):
    permission_denied_message = _('You do not have access to this page')

    def test_func(self):
        return self.get_object().id == self.request.user.id

    def dispatch(self, request, *args, **kwargs):
        self.redirect_url = reverse_lazy('users_list')
        if not self.get_test_func()():
            messages.error(self.request, self.permission_denied_message)
            self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class RedirectMixin(LoginRequiredMixinRedirect, NoPermissionMixin):
    def handle_no_permission(self):
        return HttpResponseRedirect(self.redirect_url)


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

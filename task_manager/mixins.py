from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.views.generic.edit import DeletionMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginRequiredMixinRedirect(LoginRequiredMixin):
    error_message = _('You do not have access to this page')
    redirect_url = reverse_lazy('login')

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, self.error_message)
        return self.redirect_url


class DeletionErrorMixin(DeletionMixin):
    deletion_success_url = reverse_lazy('home')
    deletion_success_message = _('Object has been deleted')
    deletion_error_message = _('Cannot delete this object,'
                               ' because the status is attached to an object!')

    def delete(self, request, *args, **kwargs):
        try:
            messages.success(request, self.deletion_success_message)
            return super().delete(request, *args, **kwargs)

        except ProtectedError:
            messages.error(request, self.deletion_error_message)
            return HttpResponseRedirect(self.deletion_success_url)

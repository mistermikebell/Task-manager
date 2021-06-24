from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.views.generic.edit import DeletionMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _


class LoginRequiredMixinRedirect(LoginRequiredMixin):
    permission_denied_message = _('You do not have access to this page')

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return HttpResponseRedirect(reverse_lazy('login'))


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

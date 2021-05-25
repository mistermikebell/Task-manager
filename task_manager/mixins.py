from django.contrib import messages
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

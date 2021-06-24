from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _


class NoPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    permission_denied_message = _('You do not have access to this page')

    def test_func(self):
        return self.get_object().id == self.request.user.id

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, self.permission_denied_message)
            return HttpResponseRedirect(reverse_lazy('login'))
        if not self.get_test_func()():
            messages.error(self.request, self.permission_denied_message)
            return HttpResponseRedirect(reverse_lazy('users_list'))
        return super().dispatch(request, *args, **kwargs)

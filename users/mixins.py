from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _


class NoPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().id == self.request.user.id

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _('You do not have access to this page')
        self.redirect_url = reverse_lazy('users_list')
        return super().dispatch(request, *args, **kwargs)

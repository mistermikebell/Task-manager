from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _


class NonAuthorPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author.id == self.request.user.id

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _('A task can be deleted by its author only')
        self.redirect_url = reverse_lazy('tasks_list')
        return super().dispatch(request, *args, **kwargs)

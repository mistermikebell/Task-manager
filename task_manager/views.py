from django.shortcuts import render
from django.utils.translation import gettext
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    context = {
        'title': gettext('Task manager')
    }
    return render(request, 'index.html', context)


class LoginRequiredMixinRedirect(LoginRequiredMixin):
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           _('You do not have access to this page'))
        return redirect_to_login(self.request.get_full_path(), 'login', '')

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from .models import UserModel


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True, label=_('First name'))
    last_name = forms.CharField(required=True, label=_('Last name'))

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class UserUpdateForm(UserCreationForm):

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

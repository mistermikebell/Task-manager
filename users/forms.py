from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label=_('Password'))
    password2 = forms.CharField(widget=forms.PasswordInput(), label=_('Password confirmation'))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

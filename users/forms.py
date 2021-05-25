from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import ugettext_lazy as _


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(), label=_('Password confirmation'))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        user = super().save(commit=commit)
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('password_mismatch')
        user.set_password(password1)
        user.save()
        return user

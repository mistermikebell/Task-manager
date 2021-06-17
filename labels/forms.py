from django import forms

from .models import Label


class UpdateLabelForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = ['name', 'description']

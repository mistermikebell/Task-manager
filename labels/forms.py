from django import forms
from labels.models import Label


class UpdateLabelForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = ['name', 'description']

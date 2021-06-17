from django import forms

from odels import Label


class UpdateLabelForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = ['name', 'description']

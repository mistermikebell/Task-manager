from django import forms
from django.forms import Form


class CreateStatusForm(Form):
    name = forms.CharField()

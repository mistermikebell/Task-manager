from django import forms
from tasks.models import Task


class UpdateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'status', 'labels', 'description', 'executor']

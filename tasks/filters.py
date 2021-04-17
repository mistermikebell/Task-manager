import django_filters

from django import forms
from django.db import models
from tasks.models import Task


class TasksFilter(django_filters.FilterSet):
    author = django_filters.BooleanFilter(
        field_name='author', label='Show only my tasks',
        widget=forms.CheckboxInput, method='filter_last_editor')

    class Meta:
        model = Task
        fields = ['status', 'labels']

    def filter_last_editor(self, queryset, name, value):
        if value:
            queryset = queryset.filter(author=self.request.user)
            return queryset
        return queryset

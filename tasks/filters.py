import django_filters

from django import forms
from tasks.models import Task
from django.utils.translation import ugettext_lazy as _


class TasksFilter(django_filters.FilterSet):
    author = django_filters.BooleanFilter(
        field_name='author', label=_('Show only my tasks'),
        widget=forms.CheckboxInput, method='filter_last_editor')
    status = django_filters.ChoiceFilter(field_name='status', label=_('Status'))

    class Meta:
        model = Task
        fields = ['status', 'labels']

    def filter_last_editor(self, queryset, name, value):
        if value:
            queryset = queryset.filter(author=self.request.user)
            return queryset
        return queryset


class MyTasksFilter(django_filters.FilterSet):
    author = django_filters.BooleanFilter(
        field_name='author', label=_('Show only my tasks'),
        widget=forms.CheckboxInput, method='filter_last_editor')
    status = django_filters.ChoiceFilter(field_name='status', label=_('Status'))

    class Meta:
        model = Task
        fields = ['status', 'labels']

    def filter_last_editor(self, queryset, name, value):
        if value:
            queryset = queryset.filter(author=self.request.user)
            return queryset
        return queryset

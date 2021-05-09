import django_filters

from django import forms
from tasks.models import Task
from django.utils.translation import ugettext_lazy as _


class MyTasksFilter(django_filters.FilterSet):
    executor = django_filters.BooleanFilter(
        field_name='executor', label=_('Show only my tasks'),
        widget=forms.CheckboxInput, method='filter_executor')
    status = django_filters.AllValuesFilter(
        field_name='status',
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Task
        fields = ['status', 'labels']

    def filter_executor(self, queryset, name, value):
        if value:
            queryset = queryset.filter(executor=self.request.user)
            return queryset
        return queryset

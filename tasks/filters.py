import django_filters

from django import forms
from tasks.models import Task
from django.utils.translation import ugettext_lazy as _
from labels.models import Label
from django.contrib.auth.models import User


class TasksFilter(django_filters.FilterSet):
    boolean_executor = django_filters.BooleanFilter(
        field_name='executor', label=_('Show only my tasks'),
        widget=forms.CheckboxInput, method='filter_executor')
    labels = django_filters.ModelChoiceFilter(queryset=Label.objects.all(), label=_('Label'))
    executor = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label=_('Executor'))

    class Meta:
        model = Task
        fields = ['status', 'labels', 'executor']

    def filter_executor(self, queryset, name, value):
        if value:
            queryset = queryset.filter(executor=self.request.user)
            return queryset
        return queryset

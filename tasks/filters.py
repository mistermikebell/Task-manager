import django_filters

from django import forms
from tasks.models import Task
from django.utils.translation import ugettext_lazy as _
from labels.models import Label
from django.contrib.auth.models import User
from tasks.models import UserModel


class TasksFilter(django_filters.FilterSet):
    boolean_author = django_filters.BooleanFilter(
        field_name='author', label=_('Show only my tasks'),
        widget=forms.CheckboxInput, method='filter_author')
    labels = django_filters.ModelChoiceFilter(queryset=Label.objects.all(), label=_('Label'))
    executor = django_filters.ModelChoiceFilter(queryset=UserModel.objects.all(), label=_('Executor'))

    class Meta:
        model = Task
        fields = ['status', 'labels', 'executor']

    def filter_author(self, queryset, name, value):
        if value:
            queryset = queryset.filter(author=self.request.user)
            return queryset
        return queryset

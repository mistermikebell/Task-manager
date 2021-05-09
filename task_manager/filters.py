import django_filters

from django import forms
from statuses.models import Status
from tasks.models import Task
from django.utils.translation import ugettext_lazy as _


class MyTasksFilter(django_filters.FilterSet):
    # status = django_filters.ModelMultipleChoiceFilter(queryset=Status.objects.all())
    status = django_filters.AllValuesMultipleFilter(field_name='status')
    class Meta:
        model = Task
        fields = ['status', 'labels']

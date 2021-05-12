import django_filters

from django import forms
from django.utils.translation import ugettext_lazy as _
from labels.models import Label
from tasks.models import UserModel
from statuses.models import Status


class TasksFilter(django_filters.FilterSet):
    boolean_author = django_filters.BooleanFilter(
        field_name='author', label=_('Show only my tasks'),
        widget=forms.CheckboxInput, method='filter_author')
    labels = django_filters.ModelChoiceFilter(queryset=Label.objects.all())
    executor = django_filters.ModelChoiceFilter(queryset=UserModel.objects.all())
    status = django_filters.ModelChoiceFilter(queryset=Status.objects.all())

    def filter_author(self, queryset, name, value):
        if value:
            queryset = queryset.filter(author=self.request.user)
            return queryset
        return queryset

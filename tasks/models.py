from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from labels.models import Label
from statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                               verbose_name=_('Status'), blank=True, null=True)
    labels = models.ManyToManyField(Label, through='LabelsTask',
                                    verbose_name=_('Labels'),
                                    blank=True)
    description = models.TextField(blank=True, null=True,
                                   verbose_name=_('Description'))
    created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name='tasks_author',
                               on_delete=models.CASCADE)
    executor = models.ForeignKey(User, related_name='tasks_executor',
                                 on_delete=models.PROTECT, blank=True, null=True,
                                 verbose_name=_('Executor'))

    def __str__(self):
        return self.name


class LabelsTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT, blank=True, null=True)

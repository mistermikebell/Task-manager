from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from labels.models import Label
from statuses.models import Status


class Task(models.Model):
    task = models.CharField(max_length=40)
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                               verbose_name=_('Status'), blank=True, null=True)
    labels = models.ManyToManyField(Label, verbose_name=_('Labels'),
                                    blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name='author',
                               on_delete=models.PROTECT)
    date_updated = models.DateTimeField(default=timezone.now)
    last_editor = models.ForeignKey(User, related_name='last_editor',
                                    on_delete=models.PROTECT)

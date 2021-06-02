from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from users.models import UserModel


class Status(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(UserModel, related_name='statuses', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

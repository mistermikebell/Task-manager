from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Status(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'), unique=True)
    created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='statuses', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

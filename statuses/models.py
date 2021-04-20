from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Status(models.Model):
    status = models.CharField(max_length=200)
    date_updated = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    editor = models.ForeignKey(User, related_name='editor', on_delete=models.CASCADE)

    def __str__(self):
        return self.status

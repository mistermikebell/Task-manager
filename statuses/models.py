from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Status(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name='statuses', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

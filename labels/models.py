from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Label(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name='labels', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

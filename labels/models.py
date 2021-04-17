from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Label(models.Model):
    label = models.CharField(max_length=40)
    description = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name='label_author', on_delete=models.CASCADE)
    date_updated = models.DateTimeField(default=timezone.now)
    last_editor = models.ForeignKey(User, related_name='label_last_editor', on_delete=models.CASCADE)

    def __str__(self):
        return self.label

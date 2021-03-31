from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Task(models.Model):
    status = models.CharField(max_length=40)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

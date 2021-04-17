from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from task_manager.statuces.models import Status
from labels.models import Label


class Task(models.Model):
    task = models.CharField(max_length=40)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    labels = models.ManyToManyField(Label, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    date_updated = models.DateTimeField(default=timezone.now)
    last_editor = models.ForeignKey(User, related_name='last_editor', on_delete=models.CASCADE)

from django.contrib import admin
from tasks.models import Task


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Task, AuthorAdmin)

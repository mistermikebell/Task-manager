from django.contrib import admin
from task_manager.statuces.models import Status


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Status, AuthorAdmin)

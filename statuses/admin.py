from django.contrib import admin
from statuses.models import Status


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Status, AuthorAdmin)

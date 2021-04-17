from django.contrib import admin
from labels.models import Label


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Label, AuthorAdmin)

from django.contrib import admin

from .models import AccessGroup


class AccessGroupAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(AccessGroup, AccessGroupAdmin)

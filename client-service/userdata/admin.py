from django.contrib import admin

# Register your models here.
from .models import AccessGroup


class AccessGroupAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(AccessGroup, AccessGroupAdmin)

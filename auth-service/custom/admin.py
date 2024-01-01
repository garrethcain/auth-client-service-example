from django.contrib import admin

from .models import CustomUserField


class CustomUserFieldAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(CustomUserField, CustomUserFieldAdmin)

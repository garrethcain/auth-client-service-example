from rest_framework import permissions


class CustomAccessPermission(permissions.BasePermission):
    message = "You do not have permission to this service"

    def has_object_permission(self, request, view, obj):
        return request.user is not None

    def has_permission(self, request, view):
        return request.user.customuserfield.field1 == "field1 value"

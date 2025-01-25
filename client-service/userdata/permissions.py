from rest_framework import permissions


class AccessGroupPermission(permissions.BasePermission):
    message = "You do not have permission to access this service"

    def has_object_permission(self, request, view, obj):
        return request.user is not None

    def has_permission(self, request, view):
        return not request.user.is_anonymous and view.access_level.startswith(
            request.user.accessgroup.access_level
        )

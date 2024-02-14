from rest_framework.permissions import BasePermission


class UserViewPermission(BasePermission):
    def has_permission(self, request, view):
        # Anyone can create an account but only the Superuser can see all of them
        if request.method in ('POST', 'PUT'):
            return True
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        # Normal users can only update their own account
        # Superusers can do anything
        return obj.id == request.user.id or request.user.is_superuser

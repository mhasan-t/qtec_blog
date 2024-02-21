from rest_framework.permissions import BasePermission


class UserViewPermission(BasePermission):
    def has_permission(self, request, view):
        # Anyone can create an account
        if request.method == 'POST':
            return True

        # Users can only GET, UPDATE, DELETE their own information
        if request.method in ('GET', 'DELETE', 'PATCH') and view.kwargs.get('pk') and request.user.id == int(view.kwargs.get('pk')):
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # Normal users can only update their own account
        return obj.id == request.user.id

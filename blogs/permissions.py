from rest_framework.permissions import BasePermission, SAFE_METHODS

from blogs.models import Blog


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 1

    def has_object_permission(self, request, view, obj):
        return False


class IsOwnerOfBlog(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.creator


class IsOwnerOfPostBlog(BasePermission):
    def has_permission(self, request, view):
        blog_id = view.kwargs.get('blog_id', None)
        blog_instance = Blog.objects.get(pk=blog_id)

        return request.user.id == blog_instance.creator

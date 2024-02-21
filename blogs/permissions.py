from rest_framework.permissions import BasePermission, SAFE_METHODS

from blogs.models import Blog


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class ReadOnlyIfAuthenticated(BasePermission):
    def has_permission(self, request, view):

        return request.method in SAFE_METHODS and request.user.is_authenticated


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 1

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.id == obj.creator.id


class IsOwnerOfPostBlog(BasePermission):
    def has_permission(self, request, view):
        blog_id = request.POST.get('blog_id', None)
        blog_instance = Blog.objects.get(pk=blog_id)
        return request.user.is_authenticated and request.user.id == blog_instance.creator.id

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.id == obj.blog.creator.id

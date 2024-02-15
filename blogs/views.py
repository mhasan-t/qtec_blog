# Create your views here.
from http import HTTPStatus

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Blog, Post
from .permissions import IsAuthor, ReadOnly, IsOwnerOfBlog, IsOwnerOfPostBlog
from .serializers import CategorySerializer, BlogSerializer, PostSerializer


class CategoryViews(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser | ReadOnly]


class BlogViews(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAdminUser | IsOwnerOfBlog | IsAuthor | ReadOnly]

    @action(detail=False, methods=['GET'])
    def search(self, request):
        search_query = request.GET.get("q")
        if not search_query:
            return Response({
                "details": "Search query must be a string of length > 0"
            }, status=HTTPStatus.BAD_REQUEST)

        results = Blog.objects.extra(
            where=[
                "MATCH(title, description) AGAINST (%s IN NATURAL LANGUAGE MODE)"],
            params=[search_query]
        )

        serialized = BlogSerializer(results, many=True, context={'request': request})
        return Response(serialized.data, status=HTTPStatus.OK)


class PostViews(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser | IsOwnerOfPostBlog | ReadOnly]

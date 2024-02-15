# Create your views here.
from rest_framework import viewsets, permissions

from .models import Category, Blog, Post
from .permissions import IsAuthor, ReadOnly
from .serializers import CategorySerializer, BlogSerializer, PostSerializer


class CategoryViews(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser | ReadOnly]


class BlogViews(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAdminUser | IsAuthor | ReadOnly]


class PostViews(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser | IsAuthor | ReadOnly]

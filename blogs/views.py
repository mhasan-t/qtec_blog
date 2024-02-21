# Create your views here.
from http import HTTPStatus

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from silk.profiling.profiler import silk_profile

from utils.views import GetBaseModelViewSet
from .models import Category, Blog, Post
from .permissions import IsAuthor, ReadOnlyIfAuthenticated, IsOwnerOfPostBlog
from .serializers import CategorySerializer, BlogSerializer, PostSerializer
from .utils import autocorrect_string

BaseModelViewSet_category = GetBaseModelViewSet("category")
BaseModelViewSet_blog = GetBaseModelViewSet("blog")
BaseModelViewSet_post = GetBaseModelViewSet("post")


class CategoryViews(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser | ReadOnlyIfAuthenticated]


class BlogViews(BaseModelViewSet_blog):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAdminUser | IsAuthor | ReadOnlyIfAuthenticated]

    @action(detail=False, methods=['GET'])
    @silk_profile(name='search_blogs')
    def search(self, request):
        # get search query param
        search_query = request.GET.get("q")
        if not search_query:
            return Response({
                "details": "Search query must be a string of length > 0"
            }, status=HTTPStatus.BAD_REQUEST)

        # autocorrect spelling
        corrected_query = autocorrect_string(search_query)

        # search the database on full text index
        results = Blog.objects.extra(
            where=[
                "MATCH(title, description) AGAINST (%s IN NATURAL LANGUAGE MODE)"],
            params=[corrected_query]
        )

        serialized = BlogSerializer(results, many=True, context={'request': request})
        return Response(serialized.data, status=HTTPStatus.OK)

    @action(detail=True, methods=['GET'])
    @silk_profile(name='get_posts_by_blog')
    def posts(self, request, pk=None):
        blog = self.get_object()
        posts = Post.objects.filter(blog=blog)

        serialized = PostSerializer(posts, many=True, context={'request': request})
        return Response(serialized.data, status=HTTPStatus.OK)


class PostViews(BaseModelViewSet_post):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser | IsOwnerOfPostBlog | ReadOnlyIfAuthenticated]

# Create your views here.
from http import HTTPStatus

from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from silk.profiling.profiler import silk_profile

from utils.views import SilkyModelViewset
from .models import Category, Blog, Post
from .permissions import IsAuthor, ReadOnly, IsOwnerOfBlog, IsOwnerOfPostBlog
from .serializers import CategorySerializer, BlogSerializer, PostSerializer
from .utils import autocorrect_string


class CategoryViews(SilkyModelViewset):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser | ReadOnly]


class BlogViews(SilkyModelViewset):
    view_name = "blogs"  # for silky profile name

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAdminUser | IsOwnerOfBlog | IsAuthor | ReadOnly]

    @action(detail=False, methods=['GET'])
    @silk_profile(name='search_blog')
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


class PostViews(SilkyModelViewset):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser | IsOwnerOfPostBlog | ReadOnly]

from rest_framework import serializers

from accounts.models import User
from accounts.serializers import UserSerializer
from .models import Category, Blog, Post


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BlogSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Blog
        fields = ["category_id", "title", "banner", "details", "category"]

    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        category_instance = Category.objects.get(id=category_id)

        blog_instance = Blog.objects.create(category=category_instance, **validated_data)
        return blog_instance


class PostSerializer(serializers.HyperlinkedModelSerializer):
    blog = BlogSerializer(read_only=True)
    blog_id = serializers.IntegerField(write_only=True)

    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["title", "post_text", "blog", "author", "blog_id"]

    def create(self, validated_data):
        blog_id = validated_data.pop('blog_id')
        blog_instance = Blog.objects.get(id=blog_id)

        request = self.context.get('request')
        author_id = request.user.id
        author_instance = User.objects.get(id=author_id)

        post_instance = Post.objects.create(blog=blog_instance, author=author_instance, **validated_data)
        return post_instance

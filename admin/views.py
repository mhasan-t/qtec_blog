from http import HTTPStatus

from django.core.paginator import Paginator
from django.db.models import Count
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView

from blogs.models import Blog, Category, Post


class AdminDashboardView(View):
    def get(self, request):
        total_blogs_count = Blog.objects.all().count()
        total_posts_count = Post.objects.all().count()
        total_categories_count = Category.objects.all().count()

        context = {
            'total_blogs_count': total_blogs_count,
            'total_posts_count': total_posts_count,
            'total_categories_count': total_categories_count
        }

        return render(request, "dashboard.html", context)


class AdminDashboardChartData(View):
    def get(self, request):
        category_counts = Category.objects.annotate(num_of_blogs=Count("blogs")).values()
        category_counts_list = [dict(elem) for elem in category_counts]

        return JsonResponse(category_counts_list, status=HTTPStatus.OK, safe=False)


class AdminBlogListView(View):
    def get(self, request):
        blogs = Blog.objects.all()
        categories = Category.objects.all()

        # Filter by category
        category = request.GET.get("category")
        if category:
            category_instance = Category.objects.get(title=category)
            blogs = blogs.filter(category=category_instance)

        # Filter by author name
        author = request.GET.get("author")
        if author:
            print(author)
            blogs = blogs.filter(creator__full_name__icontains=author)

        # Pagination
        paginator = Paginator(blogs, 5)
        page_number = request.GET.get("page")
        blogs_page = paginator.get_page(page_number)

        context = {
            'blogs': blogs_page,
            'categories': categories
        }
        return render(request, "blogs.html", context)


class AdminBlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blog_confirm_delete.html'  # Template for confirmation page
    success_url = reverse_lazy('admin:dashboard')

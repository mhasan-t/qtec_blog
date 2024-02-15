from http import HTTPStatus

from django.db.models import Count
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View

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
        return HttpResponse("blogs")

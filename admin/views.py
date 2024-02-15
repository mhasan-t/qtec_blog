from django.shortcuts import render
from django.views import View


class AdminDashboardView(View):
    def get(self, request):
        return render(request, template_name="dashboard.html")

from django.urls import path

from .views import AdminDashboardView, AdminDashboardChartData, AdminBlogListView

app_name = 'admin'

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='dashboard'),
    path('dashboard_data', AdminDashboardChartData.as_view(), name='dashboard-data'),
    path('blogs/', AdminBlogListView.as_view(), name='blogs'),
]

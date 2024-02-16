from django.urls import path

from .views import AdminDashboardView, AdminDashboardChartData, AdminBlogListView, AdminBlogDeleteView, LoginView, \
    logout_view

app_name = 'admin'

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='dashboard'),
    path('dashboard_data', AdminDashboardChartData.as_view(), name='dashboard-data'),
    path('blogs/', AdminBlogListView.as_view(), name='blogs'),
    path('blogs/<int:pk>/delete', AdminBlogDeleteView.as_view(), name='blog-delete'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]

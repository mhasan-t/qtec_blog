from django.urls import path

from .views import AdminDashboardView

app_name = 'admin'

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='dashboard'),
    path('blogs/', AdminDashboardView.as_view(), name='blogs'),
]

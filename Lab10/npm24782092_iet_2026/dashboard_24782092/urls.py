from django.urls import path
from .views import DashboardView
from .views import dashboard_view
from .views import report_stats

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('stats/', report_stats, name='report_stats'),
    path('', dashboard_view, name='dashboard'),
    path('stats/', report_stats, name='report_stats'),
]
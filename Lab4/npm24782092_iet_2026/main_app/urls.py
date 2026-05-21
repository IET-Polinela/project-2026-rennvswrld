from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', ReportListView.as_view(), name='home'),
    path('add/', ReportCreateView.as_view(), name='add_report'),
    path('edit/<int:pk>/', ReportUpdateView.as_view(), name='edit_report'),
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='delete_report'),
    path('detail/<int:pk>/', ReportDetailView.as_view(), name='detail_report'),
    path('update-status/<int:pk>/', ReportUpdateStatusView.as_view(), name='update_status'),
    path('verify/<int:pk>/', views.verify_report, name='verify'),
    path('process/<int:pk>/', views.process_report, name='process'),
    path('resolve/<int:pk>/', views.resolve_report, name='resolve'),
]
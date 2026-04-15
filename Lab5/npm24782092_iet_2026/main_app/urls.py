from django.urls import path
from .views import (
    ReportListView,
    ReportCreateView,
    ReportUpdateView,
    ReportDeleteView,
    ReportDetailView,
    update_status,
    verify_report,
    process_report,
    resolve_report
)

urlpatterns = [
    path('', ReportListView.as_view(), name='home'),

    # CRUD
    path('add/', ReportCreateView.as_view(), name='add_report'),
    path('edit/<int:pk>/', ReportUpdateView.as_view(), name='edit_report'),
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='delete_report'),
    path('detail/<int:pk>/', ReportDetailView.as_view(), name='detail_report'),

    # STATUS (INI YANG PENTING)
    path('update-status/<int:pk>/', update_status, name='update_status'),

    # OPTIONAL (boleh ada / tidak dipakai)
    path('verify/<int:pk>/', verify_report, name='verify'),
    path('process/<int:pk>/', process_report, name='process'),
    path('resolve/<int:pk>/', resolve_report, name='resolve'),

    # HALAMAN REPORTS
    path('reports/', ReportListView.as_view(), name='reports'),
]